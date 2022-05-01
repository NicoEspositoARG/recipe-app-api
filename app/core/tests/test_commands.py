from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # overrride the behaviour  of the manager
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 1)

    # the same as above, but the mock obj is an arg called, ts in this case
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        # is using this to overwrite the time.sleep of the command being test!
        # so, during testing it dosn't wait
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # adds a side effect to the mocking obj.
            gi.side_effect = [OperationalError] * 5 + [True]
            # the first 5 times will raise the error,
            # the sixth will return True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
