from functools import wraps

from django.shortcuts import redirect


def pro_required(view_func):
    """
    Decorator that ensures the user is authenticated AND has an active
    Pro or Team subscription.  Redirects to pricing page otherwise.
    """

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.conf import settings
            login_url = getattr(settings, "LOGIN_URL", "/accounts/login/")
            return redirect(f"{login_url}?next={request.path}")

        try:
            profile = request.user.profile
        except Exception:
            return redirect("payments:pricing")

        if not profile.is_pro:
            return redirect("payments:pricing")

        return view_func(request, *args, **kwargs)

    return _wrapped
