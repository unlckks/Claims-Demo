import csv, json
from pathlib import Path
from django.core.management.base import BaseCommand
from claims.models import Claim, ClaimDetail
from django.db import transaction

class Command(BaseCommand):
    help = "Load claim list & detail CSV/JSON into SQLite"

    def add_arguments(self, parser):
        parser.add_argument('--list', required=True, help='Path to claim_list_data.(csv|json)')
        parser.add_argument('--detail', required=True, help='Path to claim_detail_data.(csv|json)')
        parser.add_argument('--mode', choices=['append','overwrite'], default='append')

    def handle(self, *args, **opts):
        list_path = Path(opts['list'])
        det_path  = Path(opts['detail'])
        mode      = opts['mode']

        if mode == 'overwrite':
            self.stdout.write('Overwriting existing data…')
            ClaimDetail.objects.all().delete()
            Claim.objects.all().delete()

        with transaction.atomic():

            if list_path.suffix.lower() == '.csv':
                with list_path.open(encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
            else:
                rows = json.loads(list_path.read_text(encoding='utf-8'))

            for r in rows:

                c, _ = Claim.objects.get_or_create(
                    claim_id=int(r['id']),
                    defaults=dict(
                        patient_name=r['patient_name'],
                        billed_amount=r['billed_amount'],
                        paid_amount=r.get('paid_amount',0) or 0,
                        status=r['status'],
                        insurer_name=r['insurer_name'],
                        discharge_date=r['discharge_date'],
                    )
                )



            if det_path.suffix.lower() == '.csv':
                with det_path.open(encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    det_rows = list(reader)
            else:
                det_rows = json.loads(det_path.read_text(encoding='utf-8'))

            for d in det_rows:
                claim = Claim.objects.filter(claim_id=int(d['claim_id'])).first()
                if not claim:
                    continue
                ClaimDetail.objects.update_or_create(
                    claim=claim,
                    defaults=dict(
                        cpt_codes=d.get('cpt_codes',''),
                        denial_reason=d.get('denial_reason',''),
                    )
                )
        self.stdout.write(self.style.SUCCESS('Import done'))
