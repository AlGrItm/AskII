from django.core.management.base import BaseCommand
from ASKII.models import Tag, Question, Profile
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Fill the database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        tags_to_create = [Tag(title=fake.word()) for _ in range(10)]
        created_tags = Tag.objects.bulk_create(tags_to_create)

        profiles = Profile.objects.all()

        for _ in range(1000000):
            #tag_title = fake.word()
            #tag = Tag.objects.create(title=tag_title)

            question = Question.objects.create(
                title=fake.sentence(),
                text=fake.text(),
                author=random.choice(profiles),
                creation_data=fake.date_time()
            )
            # Связываем вопросы с несколькими случайными тегами
            random_tags = random.sample(list(created_tags), k=random.randint(1, 3))
            question.tag.add(*random_tags)

        self.stdout.write(self.style.SUCCESS('Tags and questions have been added successfully'))
