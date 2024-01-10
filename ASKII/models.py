from django.contrib.auth.models import User, UserManager
from django.db import models
from django.db.models import Count, Sum


# Create your models here.


class TagQuerySet(models.QuerySet):
    def tag_info(self):
        return self.annotate(
            question_count=Count('questions')
        )


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def top_tags(self):
        return self.get_queryset().tag_info().order_by('-question_count')[:5]


class Tag(models.Model):
    title = models.CharField(max_length=30)
    objects = TagManager()

    def __str__(self):
        return self.title


class QuestionQuerySet(models.QuerySet):
    def question_info(self):
        return self.annotate(
            num_likes=Count('likes')
        )


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self.db)

    def new_questions(self):
        return self.get_queryset().question_info().order_by('-creation_data')

    def hot_questions(self):
        return self.get_queryset().question_info().order_by('-num_likes')[:10]

    def questions_info(self):
        return self.get_queryset().question_info()

    def tag_questions(self, tag_name):
        return self.get_queryset().question_info().filter(tag__title=tag_name)

    def profile_questions(self, profile_id):
        return self.get_queryset().question_info().filter(author__user_id=profile_id)


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=300)
    author = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='questions')
    creation_data = models.DateField()
    tag = models.ManyToManyField(Tag, related_name='questions')
    objects = QuestionManager()

    def __str__(self):
        return f'{self.author.user.last_name} {self.author.user.first_name}: {self.title}'


class ProfileManager(models.Manager):
    def top_users(self):
        return self.get_queryset().annotate(total_likes=Count('questions__likes')).order_by('-total_likes')[:5]


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True, default='Hombre.png', upload_to='avatar/')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.first_name}  {self.user.last_name}'


class AnswerQuerySet(models.QuerySet):
    def answer_info(self):
        return self.annotate(
            num_likes=Count('likes'),
        )


class AnswerManager(models.Manager):
    def get_queryset(self):
        return AnswerQuerySet(self.model, using=self.db)

    def answer_info(self, question_id):
        return self.get_queryset().answer_info().filter(question__id=question_id)


class Answer(models.Model):
    correct = models.BooleanField(default=False)
    text = models.CharField(max_length=300)
    author = models.ForeignKey('Profile', on_delete=models.PROTECT)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    objects = AnswerManager()

    def __str__(self):
        return f'{self.author.user.last_name} {self.author.user.first_name}: {self.text}'


class QuestionLike(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('author', 'question')

    def __str__(self):
        return f'{self.author.user.last_name} {self.author.user.first_name}: {self.question.title}'


class AnswerLike(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('author', 'answer')

    def __str__(self):
        return f'{self.author.user.last_name} {self.author.user.first_name}: {self.answer.text}'
