from django.core.management import call_command
from django.conf import settings
from datetime import datetime, timedelta
from time import sleep
import threading
import logging
import atexit
import os

logger = logging.getLogger(__name__)

shutdown_flag = threading.Event()
lock_file_path = 'lockfile.lock'


def schedule_email():
    # 60 seconds buffer
    buffer_time = 60

    while not shutdown_flag.is_set():
        try:
            now = datetime.now()
            logger.info(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            next_execution = now.replace(
                hour=settings.EMAIL_SCHEDULER_HOUR, minute=settings.EMAIL_SCHEDULER_MINUTES, second=0, microsecond=0)

            time_diff = (next_execution - now).total_seconds()
            if time_diff < 0 or time_diff < buffer_time:
                logger.info("Adjusting next execution to the following day.")
                next_execution += timedelta(days=1)

            sleep_duration = (next_execution - now).total_seconds()

            logger.info(
                f"Calculated next execution time: {next_execution.strftime('%Y-%m-%d %H:%M:%S')}")

            shutdown_flag.wait(sleep_duration)

            if not shutdown_flag.is_set():
                call_command('send_daily_word')
        except Exception as e:
            logger.exception("An error occurred in schedule_email")


def start_background_task():
    if not os.path.exists(lock_file_path):
        with open(lock_file_path, 'w') as lock_file:
            lock_file.write('')

        thread = threading.Thread(target=schedule_email)
        thread.daemon = True
        thread.start()

        atexit.register(stop_background_task)
        logger.info("Background task started successfully.")
    else:
        logger.warning('Background task already running.')


def stop_background_task():
    shutdown_flag.set()
    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)
    logger.info("Background task stopped.")
