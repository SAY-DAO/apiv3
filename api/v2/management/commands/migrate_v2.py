from django.core.management.base import BaseCommand

from authentication.models import OTPValidation
from users.models import User


class Command(BaseCommand):
    help = 'Migrate database v2 to new one'

    def handle(self, *args, **options):
        User.import_from_v2()
        OTPValidation.import_from_v2()
