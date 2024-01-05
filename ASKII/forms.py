from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from ASKII import models


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4)
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrongpass':
            raise ValidationError("Wrong password.")
        has_uppercase = any(char.isupper() for char in data)
        if not has_uppercase:
            raise ValidationError("Password must contain at least one uppercase letter.")
        return data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=4, widget=forms.PasswordInput, help_text="Minimum size: 4 letters.")
    password_check = forms.CharField(min_length=4, widget=forms.PasswordInput)
    username = forms.CharField(min_length=4)
    last_name = forms.CharField(required=False, help_text="Optional field")
    first_name = forms.CharField(required=False, help_text="Optional field")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_check', 'last_name', 'first_name']

    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password != password_check:
            raise ValidationError("Passwords do not match")

        has_uppercase = any(char.isupper() for char in password)
        if not has_uppercase:
            raise ValidationError("Password must contain at least one uppercase letter.")

    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        return User.objects.create_user(**self.cleaned_data)


class SettingsForm(forms.ModelForm):
    password = forms.CharField(min_length=4, widget=forms.PasswordInput, help_text="Minimum size: 4 letters.", required=False)
    password_check = forms.CharField(min_length=4, widget=forms.PasswordInput, required=False)
    username = forms.CharField(min_length=4, required=False)
    last_name = forms.CharField(required=False, help_text="Optional field")
    first_name = forms.CharField(required=False, help_text="Optional field")
    avatar = forms.ImageField(required=False)

    class Meta:
        model = models.Profile
        fields = ['username', 'password', 'password_check', 'last_name', 'first_name', 'avatar']

    def clean_username(self):
        new_username = self.cleaned_data['username']
        existing_user = User.objects.filter(username=new_username).exclude(pk=self.instance.user.pk).first()
        if existing_user:
            raise forms.ValidationError("This username is already in use. Please choose a different one.")
        return new_username

    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if password != password_check:
            raise ValidationError("Passwords do not match")

    def save(self, user, **kwargs):
        for field in self.Meta.fields:
            field_value = self.cleaned_data.get(field)
            if field_value:
                setattr(user, field, field_value)
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            profile, created = models.Profile.objects.get_or_create(user=user)
            profile.avatar = avatar
            profile.save()
        user.save()
        return user


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
