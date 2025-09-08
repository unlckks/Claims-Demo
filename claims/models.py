import json
from django.db import models
from django.contrib.auth.models import User


class Claim(models.Model):
    # Claim record (main insurance claim information)

    STATUS_CHOICES = [
        ('Denied', 'Denied'),
        ('Paid', 'Paid'),
        ('Under Review', 'Under Review'),
    ]

    claim_id = models.IntegerField(unique=True)   # Unique claim number
    patient_name = models.CharField(max_length=200)   # Patient’s name
    billed_amount = models.DecimalField(max_digits=12, decimal_places=2)   # Amount billed
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)   # Amount paid
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)   # Claim status
    insurer_name = models.CharField(max_length=200)   # Insurance company name
    discharge_date = models.DateField()   # Date of discharge

    flagged = models.BooleanField(default=False)   # Mark claim as flagged for review
    category = models.CharField(max_length=50, default='default', blank=True)   # Optional category

    class Meta:
        # Add database indexes for faster filtering
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['insurer_name']),
            models.Index(fields=['discharge_date']),
        ]

    @property
    def underpayment(self):
        # Calculate difference between billed and paid amounts
        diff = self.billed_amount - self.paid_amount
        return diff if diff > 0 else 0

    def __str__(self):
        return f'Claim {self.claim_id} - {self.patient_name}'


class ClaimDetail(models.Model):
    # Extra details linked to each claim (1-to-1 relation)
    claim = models.OneToOneField(Claim, on_delete=models.CASCADE, related_name='detail')
    cpt_codes = models.CharField(max_length=255, blank=True)   # Procedure codes (as JSON or comma-separated string)
    denial_reason = models.TextField(blank=True)   # Reason for denial (if any)

    @property
    def cpt_list(self):
        # Return CPT codes as a list (support JSON format or comma-separated string)
        raw = (self.cpt_codes or "").strip()
        if not raw:
            return []
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return [str(x).strip() for x in data if x]
        except Exception:
            pass
        return [c.strip() for c in raw.split(",") if c.strip()]

    def __str__(self):
        return f'Detail for {self.claim.claim_id}'


class Flag(models.Model):
    # Flag raised for a claim (by user, with reason)
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='flags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, blank=True)   # Optional reason text
    created_at = models.DateTimeField(auto_now_add=True)   # Timestamp
    active = models.BooleanField(default=True)   # Whether the flag is active

    def __str__(self):
        return f'Flag({self.claim.claim_id}) by {self.user.username}'


class Note(models.Model):
    # User notes linked to a claim
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()   # Note text
    created_at = models.DateTimeField(auto_now_add=True)   # Timestamp

    def __str__(self):
        return f'Note({self.claim.claim_id})'
