import time
from typing import Any, Optional
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                # Django check as python manage.py check
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!!'))
