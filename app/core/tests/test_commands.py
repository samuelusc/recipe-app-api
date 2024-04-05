"""
Module to test custom Django management commands.
"""
# Import necessary testing utilities and mock functionality
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# Patching the Command.check method used in wait_for_db command


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """
    Test suite for the custom Django management command wait_for_db
    It simulates different database availability scenarios to ensure
    the command handles them appropriately.
    """

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        # Execute the command to be tested
        call_command('wait_for_db')

        # Ensure the mocked check method was called
        # only once with expected arguments
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # Check if the mocked check method was called 6 times in total
        self.assertEqual(patched_check.call_count, 6)
        # Ensure the final call was with the expected arguments
        patched_check.assert_called_with(databases=['default'])
