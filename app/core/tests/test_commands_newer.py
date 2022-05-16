from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# .check method is defined in BaseCommand class.
@patch('core.management.commands.new_wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands, new code version."""

    def test_new_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready"""
        patched_check.return_value = True

        call_command('new_wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])
        # ensure that the mock obj, is called with this parameters.

    @patch('time.sleep')
    def test_new_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        # is raising an exception with side effect. if you pass an exception
        # it will be raised.
        # the first two times, the mocked method is called,
        # it raises the Pyscop error.
        # then the next three times raises OperationError,
        # and then, the sixth time returns true
        call_command('new_wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
