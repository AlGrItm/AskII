import os
import random
from django.core.management.base import BaseCommand
from ASKII.models import Profile


class Command(BaseCommand):
    help = 'Fill missing avatars in Profiles with random images from folder'

    def handle(self, *args, **kwargs):
        avatar_folder = 'static/Images'

        profiles = Profile.objects.filter(avatar='None')

        if profiles.exists():
            avatar_files = os.listdir(avatar_folder)
            for profile in profiles:
                if avatar_files:
                    random_avatar = random.choice(avatar_files)
                    avatar_path = os.path.join(avatar_folder, random_avatar)

                    profile.avatar = avatar_path
                    profile.save()

                    avatar_files.remove(random_avatar)

            self.stdout.write(self.style.SUCCESS('Profiles have been updated with avatars'))
        else:
            self.stdout.write(self.style.NOTICE('No Profiles without avatars found'))
