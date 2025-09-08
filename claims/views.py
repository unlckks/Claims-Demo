import json, ast, re
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Claim, Note, Flag


def lazypaste_redirect_home(request):
    # Redirect "/" (or this route) to the claims list page
    return redirect('claims_list')


@login_required
def lazypaste_list(request):
    """
    Render the main claims list page.
    - On normal request: return full template 'claims/list.html'
    - On HTMX request: return only the list fragment 'claims/_list.html'
      so the list can be replaced live without a full page reload.
    """
    q = (request.GET.get('q') or '').strip()
    status = request.GET.get('status') or ''
    insurer = request.GET.get('insurer') or ''

    # Base queryset ordered by latest discharge date
    qs = Claim.objects.all().order_by('-discharge_date')

    # Text search across patient, insurer, and status; also allow numeric claim_id
    if q:
        cond = (Q(patient_name__icontains=q) |
                Q(insurer_name__icontains=q) |
                Q(status__icontains=q))
        if q.isdigit():
            cond |= Q(claim_id=int(q))
        qs = qs.filter(cond)

    # Optional filters
    if status:
        qs = qs.filter(status=status)
    if insurer:
        qs = qs.filter(insurer_name__icontains=insurer)

    ctx = {
        'claims': qs[:200],  # safety cap
        'status_choices': Claim.STATUS_CHOICES,
        'q': q, 'status': status, 'insurer': insurer,
    }

    # If this came from HTMX, return only the list partial
    if request.headers.get('HX-Request'):
        return render(request, 'claims/_list.html', ctx)

    # Otherwise return the full page
    return render(request, 'claims/list.html', ctx)


@login_required
def lazypaste_detail(request, pk):
    """
    Render the right-side detail panel for a single claim.
    Ensures ClaimDetail exists. Also parses CPT codes into a clean list for display.
    """
    claim = get_object_or_404(Claim, pk=pk)
    if not hasattr(claim, 'detail'):
        from .models import ClaimDetail
        ClaimDetail.objects.get_or_create(claim=claim)

    cpt_codes = _parse_cpt_list(getattr(claim.detail, 'cpt_codes', ''))
    return render(request, 'claims/_detail.html', {'claim': claim, 'cpt_codes': cpt_codes})


@login_required
def lazypaste_row(request, pk):
    """
    Return the single row partial for a claim (used to refresh just that row in the list).
    """
    c = get_object_or_404(Claim, pk=pk)
    return render(request, 'claims/_row.html', {'c': c})


@login_required
def lazypaste_toggle_flag(request, pk):
    """
    Toggle the 'flagged' state on a claim.
    - Records a Flag entry when turning ON (for audit).
    - If called via HTMX, respond with HX-Refresh to reload the page (simple & reliable).
      (You could also return a row/detail partial if you prefer partial updates.)
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('POST only')

    claim = get_object_or_404(Claim, pk=pk)
    claim.flagged = not claim.flagged
    claim.save()

    # Audit entry only when enabling the flag
    if claim.flagged:
        Flag.objects.create(
            claim=claim, user=request.user,
            reason=(request.POST.get('reason') or '').strip()
        )

    # HTMX path: ask the browser to reload (keeps UI in sync on both list & detail)
    if request.headers.get('HX-Request'):
        resp = HttpResponse(status=204)   # No content
        resp['HX-Refresh'] = 'true'       # htmx will do location.reload()
        return resp

    # Non-HTMX fallback
    return redirect('claims_list')


@login_required
def lazypaste_add_note(request, pk):
    """
    Add a note to a claim.
    - On success, return only the notes block partial so the notes area updates live.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('POST only')

    text = (request.POST.get('text') or '').strip()
    if not text:
        return HttpResponseBadRequest('注释不能为空')

    claim = get_object_or_404(Claim, pk=pk)
    Note.objects.create(claim=claim, user=request.user, text=text)

    # Return the updated notes fragment (HTMX will swap this into the page)
    resp = render(request, 'claims/_notes_block.html', {'claim': claim})
    return resp


# ---------- utils ----------
def _parse_cpt_list(value):
    """
    Normalize CPT/HCPCS codes into a list for display or processing.
    Supports:
      - JSON arrays: e.g. '["99213","99214-25"]'
      - Python literal lists/tuples: e.g. "['A0427','A0425-59']"
    De-duplicates while preserving order.
    """
    if not value:
        return []
    s = str(value).strip()

    # 1) JSON array
    try:
        data = json.loads(s)
        if isinstance(data, list):
            return [str(x).strip() for x in data if str(x).strip()]
    except Exception:
        pass

    # 2) Python literal list/tuple
    try:
        data = ast.literal_eval(s)
        if isinstance(data, (list, tuple)):
            return [str(x).strip() for x in data if str(x).strip()]
    except Exception:
        pass

    # 3) Regex extraction (supports ',' and Chinese '，')
    s = s.replace("，", ",")
    tokens = re.findall(r'(?:\d{5}|[A-Z]\d{4})(?:-\d{2})?', s, flags=re.I)

    # Deduplicate while keeping original order
    out, seen = [], set()
    for t in tokens:
        k = t.upper()
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out
