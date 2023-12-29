from django.core.management.base import BaseCommand
from ...utils import check_libreoffice


class Command(BaseCommand):
    help = "Install libreoffice if it's not already installed in linux."

    def handle(self, *args, **options):
        check_libreoffice()
