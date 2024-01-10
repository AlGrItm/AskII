import os
import random
from django.core.management.base import BaseCommand
from ASKII.models import Profile


class Command(BaseCommand):
    help = 'Set random avatar for profiles with avatar=None'

    def handle(self, *args, **kwargs):
        default_avatar_directory = 'avatar/'  # Папка с аватарками

        # Получаем список всех файлов в папке с аватарками
        avatar_directory = os.path.join('media', default_avatar_directory)
        avatars = [os.path.join(default_avatar_directory, f) for f in os.listdir(avatar_directory) if
                   os.path.isfile(os.path.join(avatar_directory, f))]

        profiles_without_avatar = Profile.objects.filter(avatar="None")
        print(profiles_without_avatar.count())
        for profile in profiles_without_avatar:
            if avatars:
                random_avatar = random.choice(avatars)
                profile.avatar.name = random_avatar
                profile.save()

        self.stdout.write(self.style.SUCCESS('Random avatar set for profiles without avatar'))