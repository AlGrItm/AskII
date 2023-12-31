import os
import random
import string

from django.core.management.base import BaseCommand
from ASKII.models import Profile
from django.contrib.auth.models import User
from faker import Faker


def generate_random_string():
    length = random.randint(6, 20)
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


class Command(BaseCommand):
    help = 'Fill the database with sample Profile data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        avatar_folder = 'static/Images'
        profiles_to_create = []
        avatar_files = os.listdir(avatar_folder)

        for _ in range(8000):

            user = User.objects.create(
                username=generate_random_string(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email()
            )
            random_avatar = random.choice(avatar_files)
            avatar_path = os.path.join(avatar_folder, random_avatar)
            profile = Profile(user=user, avatar=avatar_path)
            profiles_to_create.append(profile)

        Profile.objects.bulk_create(profiles_to_create)

        self.stdout.write(self.style.SUCCESS('Profiles have been added successfully'))
