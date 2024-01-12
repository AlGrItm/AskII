from django.core.management.base import BaseCommand
from ASKII.models import AnswerLike, QuestionLike, Profile, Answer, Question
import random

class Command(BaseCommand):
    help = 'Fill the database with sample AnswerLike and QuestionLike data'

    def handle(self, *args, **kwargs):
        profiles = Profile.objects.all()
        answers = Answer.objects.all()
        questions = Question.objects.all()

        answer_likes_to_create = []
        question_likes_to_create = []

        for _ in range(10000):
            author = random.choice(profiles)
            answer = random.choice(answers)
            question = random.choice(questions)

            # Check if the like already exists
            if not AnswerLike.objects.filter(author=author, answer=answer).exists():
                answer_like = AnswerLike(author=author, answer=answer)
                answer_likes_to_create.append(answer_like)

            # Check if the like already exists
            if not QuestionLike.objects.filter(author=author, question=question).exists():
                question_like = QuestionLike(author=author, question=question)
                question_likes_to_create.append(question_like)

        AnswerLike.objects.bulk_create(answer_likes_to_create)
        QuestionLike.objects.bulk_create(question_likes_to_create)

        self.stdout.write(self.style.SUCCESS('Likes have been added successfully'))
