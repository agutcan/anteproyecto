from .models import Notification


def notification_counts(request):
    """Context processor that adds unread notifications count for the current user."""
    unread = 0
    try:
        if request.user and request.user.is_authenticated:
            unread = Notification.objects.filter(user=request.user, read_at__isnull=True).count()
    except Exception:
        unread = 0
    return {"notification_unread_count": unread}
