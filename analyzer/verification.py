"""Light heuristic verification for crowdsourced salary submissions."""

from django.db.models import Q

from .models import SalarySubmission


def _median(values):
    if not values:
        return None
    sorted_vals = sorted(values)
    return sorted_vals[len(sorted_vals) // 2]


def _role_filter(role):
    """Match similar roles via first significant word."""
    token = role.strip().split()[0] if role.strip() else role
    if len(token) < 3:
        return Q(role__iexact=role)
    return Q(role__icontains=token)


def _peer_queryset(submission):
    return SalarySubmission.objects.filter(
        verification_status="verified",
        company_type=submission.company_type,
        city__iexact=submission.city,
    ).filter(_role_filter(submission.role)).exclude(pk=submission.pk)


def apply_light_verification(submission, confirmed_payslip=False):
    """
    Set verification_status based on peer CTC comparison.
    Syncs is_verified on the model via save().
    """
    peers = _peer_queryset(submission)
    peer_ctcs = list(peers.values_list("ctc", flat=True))
    median_ctc = _median(peer_ctcs)

    if median_ctc:
        ratio = submission.ctc / median_ctc
        if ratio < 0.4 or ratio > 2.5:
            submission.verification_status = "flagged"
        elif len(peer_ctcs) >= 3 and 0.6 <= ratio <= 1.6:
            submission.verification_status = "verified"
        elif confirmed_payslip and len(peer_ctcs) >= 1 and 0.8 <= ratio <= 1.25:
            submission.verification_status = "verified"
        else:
            submission.verification_status = "pending"
    else:
        submission.verification_status = "pending"

    submission.save(update_fields=["verification_status", "is_verified"])
