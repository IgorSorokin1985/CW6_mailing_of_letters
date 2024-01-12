from django.core.management.base import BaseCommand
from mailing.utils import send_ready_mailings


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_ready_mailings()
