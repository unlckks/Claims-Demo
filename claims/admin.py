from django.contrib import admin
from .models import Claim, ClaimDetail, Note, Flag


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_id','patient_name','billed_amount','paid_amount','status','insurer_name','discharge_date','flagged')
    search_fields = ('patient_name','insurer_name','status','claim_id')

admin.site.register(ClaimDetail)
admin.site.register(Note)
admin.site.register(Flag)
