from unittest.mock import patch
from ..services.scheduler_service import schedule_email, start_background_task, stop_background_task, shutdown_flag, lock_file_path
import unittest
import os


class BackgroundTaskTests(unittest.TestCase):

    def setUp(self):
        # clear the shutdown flag before each test
        shutdown_flag.clear()

        # ensure the lock file does not exist at the start of each test
        if os.path.exists(lock_file_path):
            os.remove(lock_file_path)

    def tearDown(self):
        shutdown_flag.set()
        if os.path.exists(lock_file_path):
            os.remove(lock_file_path)

    # start background task with no lock file
    @patch('word_manager.services.scheduler_service.threading.Thread')
    def test_start_background_task_without_lock_file(self, mock_thread):
        start_background_task()
        mock_thread.assert_called_once()
        self.assertTrue(os.path.exists(lock_file_path))

    # don't start new thread if lock file exists
    @patch('word_manager.services.scheduler_service.threading.Thread')
    def test_start_background_task_with_lock_file(self, mock_thread):
        with open(lock_file_path, 'w') as lock_file:
            lock_file.write('')
        start_background_task()
        mock_thread.assert_not_called()

    # background task stops
    def test_stop_background_task(self):
        with open(lock_file_path, 'w') as lock_file:
            lock_file.write('')
        stop_background_task()
        self.assertFalse(os.path.exists(lock_file_path))
        self.assertTrue(shutdown_flag.is_set())
