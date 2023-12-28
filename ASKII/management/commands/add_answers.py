from django.core.management.base import BaseCommand
from ASKII.models import Answer, Profile, Question
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Fill the database with sample Answer data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        profiles = Profile.objects.all()
        questions = Question.objects.all()

        answers_to_create = []
        for _ in range(100000):
            answer = Answer(
                correct=random.choice([True, False]),
                text=fake.text(),
                author=random.choice(profiles),
                question=random.choice(questions)
            )
            answers_to_create.append(answer)

        Answer.objects.bulk_create(answers_to_create)

        self.stdout.write(self.style.SUCCESS('Answers have been added successfully'))
