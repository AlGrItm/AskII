from ASKII.models import Tag, Profile


def tags(request):
    return {'tags': Tag.objects.top_tags()}


def profiles(request):
    return {'profiles': Profile.objects.top_users()}
