from django import forms
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from ASKII import models


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4)
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        has_uppercase = any(char.isupper() for char in data)
        if not has_uppercase:
            raise ValidationError("Password must contain at least one uppercase letter.")
        return data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)
    password_check = forms.CharField(min_length=4, widget=forms.PasswordInput)
    username = forms.CharField(min_length=4)
    last_name = forms.CharField(min_length=2, required=False)
    first_name = forms.CharField(min_length=2, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_check', 'last_name', 'first_name']

    def clean_password_check(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password != password_check:
            raise ValidationError("Passwords do not match")

        has_uppercase = any(char.isupper() for char in password)
        if not has_uppercase:
            raise ValidationError("Password must contain at least one uppercase letter.")
        return password

    def clean_username(self):
        new_username = self.cleaned_data['username']
        existing_user = User.objects.filter(username=new_username)
        if existing_user:
            raise forms.ValidationError("This username is already in use. Please choose a different one.")
        return new_username

    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        return User.objects.create_user(**self.cleaned_data)


class SettingsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password_check = forms.CharField(widget=forms.PasswordInput, required=False)
    username = forms.CharField(min_length=4, required=False)
    last_name = forms.CharField(min_length=2, required=False)
    first_name = forms.CharField(min_length=2, required=False)

    class Meta:
        model = models.User
        fields = ['username', 'email', 'password', 'password_check', 'last_name', 'first_name']

    def clean_username(self):
        new_username = self.cleaned_data['username']
        existing_user = User.objects.filter(username=new_username).exclude(pk=self.instance.user.pk).first()
        if existing_user:
            raise forms.ValidationError("This username is already in use. Please choose a different one.")
        return new_username

    def clean_password_check(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if password != password_check:
            raise ValidationError("Passwords do not match")
        if password:
            has_uppercase = any(char.isupper() for char in password)
            if not has_uppercase:
                raise ValidationError("Password must contain at least one uppercase letter.")
        return password

    def save(self, user, request=None, **kwargs):
        for field in self.Meta.fields:
            field_value = self.cleaned_data.get(field)
            if field_value:
                if field == 'password':
                    user.set_password(field_value)
                else:
                    setattr(user, field, field_value)
        user.save()
        if request:
            update_session_auth_hash(request, user)
        return user


class ProfileSettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = models.Profile
        fields = ['avatar']

    def save(self, profile, **kwargs):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            profile.avatar = avatar
            profile.save()
            return profile


class AskForm(forms.ModelForm):
    tags = forms.CharField(max_length=100)
    class Meta:
        model = models.Question
        fields = ['title', 'text']

    def save(self, request, commit=True):
        question = super().save(commit=False)
        tags_input = self.cleaned_data.get('tags')
        tag_list = [tag.strip() for tag in tags_input.split(' ') if tag.strip()]
        tag_objects = []
        for tag_name in tag_list:
            tag, created = models.Tag.objects.get_or_create(title=tag_name)
            tag_objects.append(tag)
        question.author = request.user.profile
        question.creation_data = timezone.now()
        question.save()
        question.tag.set(tag_objects)
        if commit:
            question.save()
        return question


class AnswerForm(forms.ModelForm):
    question_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = models.Answer
        fields = ['text']

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        if self.question:
            self.fields['question_id'].initial = self.question.id

    def save(self, request, commit=True):
        answer = super().save(commit=False)
        answer.author = request.user.profile
        answer.question = self.question
        if commit:
            answer.save()
        return answer
