import os
import random

from django.core.management.base import BaseCommand
from ASKII.models import Profile
from django.contrib.auth.models import User
from faker import Faker


class Command(BaseCommand):
    help = 'Fill the database with sample Profile data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        avatar_folder = 'static/Images'
        profiles_to_create = []
        avatar_files = os.listdir(avatar_folder)

        for _ in range(10000):
            user = User.objects.create(
                username=fake.user_name(),
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
