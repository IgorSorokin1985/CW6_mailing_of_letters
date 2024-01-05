import datetime
import logging
import pytz

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from mailing.models import Mailing
from mailing.utils import mailing_execution

logger = logging.getLogger(__name__)


def send_ready_mailings():
    utc = pytz.UTC

    now = datetime.datetime.now().replace(tzinfo=utc)

    mailings = Mailing.objects.filter(status='Ready').all()

    for mailing in mailings:
        datetime_mailing = mailing.data_mailing.replace(tzinfo=utc)
        if now > datetime_mailing:
            mailing_execution(mailing.pk)
    print('apscheduler work again')


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('apscheduler work')
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_ready_mailings,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="send_ready_mailings",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
