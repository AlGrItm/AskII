import os
import random
import string

from django.core.management.base import BaseCommand
from ASKII.models import Profile
from django.contrib.auth.models import User
from faker import Faker
from django.db.utils import IntegrityError


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

        existing_user_ids = set(User.objects.values_list('id', flat=True))

        for _ in range(1000):
            username = generate_random_string()
            email = fake.email()

            # Проверяем, существует ли пользователь с таким username или email
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                user = User.objects.create(
                    username=username,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=email
                )

                # Проверяем, существует ли user_id в existing_user_ids
                if user.id not in existing_user_ids:
                    random_avatar = random.choice(avatar_files)
                    avatar_path = os.path.join(avatar_folder, random_avatar)
                    profile = Profile(user=user, avatar=avatar_path)
                    profiles_to_create.append(profile)
                else:
                    # Если пользователь существует, пропускаем итерацию
                    user.delete()
                    continue
            else:
                # Если пользователь существует, пропускаем итерацию
                continue

        # Попробуем сохранить профили. Если возникает IntegrityError, выводим сообщение
        try:
            Profile.objects.bulk_create(profiles_to_create)
            self.stdout.write(self.style.SUCCESS('Profiles have been added successfully'))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Error while adding profiles: {str(e)}'))
