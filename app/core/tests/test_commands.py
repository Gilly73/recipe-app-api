"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# patch goes to dir core.management.commands.wait_for_db and runs the Command
# class - check method from BaseCommand
# anything patch is mocked
# patched_check
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database command when database is ready."""
        # mocking the check method to return True
        patched_check.return_value = True

        call_command('wait_for_db')
        # databases=['default'] is the parameter passed to check method
        patched_check.assert_called_once_with(databases=['default'])

    # adding a patch to sleep method
    # patched_sleep - replaces the built in sleep function with a
    # magic mock sleep function
    # overriding value of sleep function to avoid actually waiting
    @patch('time.sleep')
    # test when db is isn't ready
    # args for patch from the inside out
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # mocking to raise some exceptions - use side_effect
        # first two calls raise Psycopg2OpError (Postgres,
        # the application itself hasn't even started yet,
        # so it's not ready to accept any connections.),
        # next three raise OperationalError db isn't ready yet
        # last call returns True
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')
        # expect the check method to be called 6 times
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
