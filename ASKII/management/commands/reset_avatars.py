from django.core.management.base import BaseCommand
from ASKII.models import Profile


class Command(BaseCommand):
    help = 'Reset all avatars to null'

    def handle(self, *args, **kwargs):
        profiles = Profile.objects.all()
        for profile in profiles:
            profile.avatar = None

        Profile.objects.bulk_update(profiles, ['avatar'])
        self.stdout.write(self.style.SUCCESS('Avatars reset to null for all profiles'))
