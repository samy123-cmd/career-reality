"""Give-to-get salary unlock credits and free preview gating."""

from django.utils import timezone

FREE_PREVIEW_LIMIT = 3
CREDITS_PER_SUBMISSION = 3


def _authenticated_user(request):
    user = getattr(request, "user", None)
    if user is None or not getattr(user, "is_authenticated", False):
        return None
    return user


def _session(request):
    return getattr(request, "session", None)


def _current_month():
    return timezone.now().strftime("%Y-%m")


def is_pro_user(request):
    user = _authenticated_user(request)
    if user is not None:
        try:
            return user.profile.is_pro
        except Exception:
            return False
    return False


def get_balance(request):
    user = _authenticated_user(request)
    if user is not None:
        try:
            return user.profile.salary_credits
        except Exception:
            return 0
    session = _session(request)
    if session is None:
        return 0
    return session.get("salary_unlocks", 0)


def get_unlocked_ids(request):
    session = _session(request)
    if session is None:
        return set()
    return set(session.get("unlocked_salary_ids", []))


def is_salary_unlocked(request, submission_id):
    if is_pro_user(request):
        return True
    return submission_id in get_unlocked_ids(request)


def _reset_monthly_previews_if_needed(request):
    """Persist a month rollover. Only call on write paths (consume), never on read-only context."""
    month = _current_month()
    user = _authenticated_user(request)
    if user is not None:
        profile = user.profile
        if profile.salary_previews_month != month:
            profile.salary_previews_used = 0
            profile.salary_previews_month = month
            profile.save(update_fields=["salary_previews_used", "salary_previews_month"])
        return
    session = _session(request)
    if session is None:
        return
    if session.get("salary_previews_month") != month:
        session["salary_previews_used"] = 0
        session["salary_previews_month"] = month


def _anonymous_previews_used(request) -> int:
    """Read preview usage without creating/mutating the session cookie."""
    session = _session(request)
    if session is None:
        return 0
    month = _current_month()
    if session.get("salary_previews_month") != month:
        return 0
    return int(session.get("salary_previews_used", 0) or 0)


def get_free_previews_remaining(request):
    if is_pro_user(request):
        return FREE_PREVIEW_LIMIT
    user = _authenticated_user(request)
    if user is not None:
        # Authenticated reads may persist a month rollover on the profile row.
        _reset_monthly_previews_if_needed(request)
        used = user.profile.salary_previews_used
    else:
        # Do NOT write the anonymous session here — this runs from a global
        # context processor and was forcing Set-Cookie on every public page,
        # which busts CDN cache and wastes Google crawl budget.
        used = _anonymous_previews_used(request)
    return max(0, FREE_PREVIEW_LIMIT - used)


def consume_credit(request):
    user = _authenticated_user(request)
    if user is not None:
        profile = user.profile
        if profile.salary_credits <= 0:
            return False
        profile.salary_credits -= 1
        profile.save(update_fields=["salary_credits"])
        return True
    session = _session(request)
    if session is None:
        return False
    unlocks = session.get("salary_unlocks", 0)
    if unlocks <= 0:
        return False
    session["salary_unlocks"] = unlocks - 1
    return True


def consume_free_preview(request):
    if is_pro_user(request):
        return True
    if get_free_previews_remaining(request) <= 0:
        return False
    _reset_monthly_previews_if_needed(request)
    user = _authenticated_user(request)
    if user is not None:
        profile = user.profile
        profile.salary_previews_used += 1
        profile.save(update_fields=["salary_previews_used"])
        return True
    session = _session(request)
    if session is None:
        return False
    session["salary_previews_used"] = session.get("salary_previews_used", 0) + 1
    return True


def _mark_unlocked(request, submission_id):
    session = _session(request)
    if session is None:
        return
    unlocked = list(session.get("unlocked_salary_ids", []))
    if submission_id not in unlocked:
        unlocked.append(submission_id)
        session["unlocked_salary_ids"] = unlocked


def unlock_salary_row(request, submission_id):
    """Try to unlock a salary row. Returns (success, reason)."""
    if is_salary_unlocked(request, submission_id):
        return True, "already_unlocked"

    if is_pro_user(request):
        _mark_unlocked(request, submission_id)
        return True, "pro"

    if get_balance(request) > 0 and consume_credit(request):
        _mark_unlocked(request, submission_id)
        return True, "credit"

    if get_free_previews_remaining(request) > 0 and consume_free_preview(request):
        _mark_unlocked(request, submission_id)
        return True, "preview"

    return False, "no_access"
