from django.core.management.base import BaseCommand
from ASKII.models import Tag
import random
import string


class Command(BaseCommand):
    help = 'Create random tags'

    def handle(self, *args, **kwargs):
        num_tags = 1000  # Количество случайных тегов для создания

        tags_to_create = []
        for _ in range(num_tags):
            tag_length = random.randint(2, 10)  # Случайная длина тега от 2 до 10 символов
            tag_title = ''.join(random.choices(string.ascii_lowercase, k=tag_length))
            tag, created = Tag.objects.get_or_create(title=tag_title)
            if created:
                tags_to_create.append(tag)

        if tags_to_create:
            Tag.objects.bulk_create(tags_to_create)
            self.stdout.write(self.style.SUCCESS(f'{num_tags} tags have been added successfully'))
        else:
            self.stdout.write(self.style.WARNING('No tags were created'))