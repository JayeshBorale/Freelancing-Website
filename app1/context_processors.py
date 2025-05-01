from .models import Profile

def Base(request):
    if request.user.is_authenticated:
        try:
            lp = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            lp = None
        return {'lp': lp}
    return {}
