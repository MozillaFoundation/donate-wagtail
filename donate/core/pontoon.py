import django_rq
from redlock import RedLock, RedLockError

from wagtail_localize_pontoon.sync import SyncManager


def _sync_task():
    CustomSyncManager().sync()


class CustomSyncManager(SyncManager):
    """
    Implements sync/trigger/is_queued/is_running.

    These are called from various parts of wagtail-localize-pontoon package.
    """

    def __init__(self):
        super().__init__()

        self.queue = django_rq.get_queue('wagtail_localize_pontoon.sync')

    def sync(self):
        """
        Performs the synchronisation

        Called directly from the sync_pontoon command
        """
        try:
            with RedLock("wagtail_localize_pontoon.sync"):
                super().sync()

        except RedLockError:
            self.logger.warning("Failed to acquire lock. The task is probably already running.")

    def trigger(self):
        """
        Enqueues a job to perform synchronisation in the background

        Called by Django view when "Force sync" is pressed
        """
        # Make sure there is only one job in the queue at a time
        self.queue.delete()
        self.queue.enqueue(_sync_task)

    def is_queued(self):
        """
        Returns True if a synchronisation job is already in the queue
        """
        return bool(self.queue.get_jobs())

    def is_running(self):
        """
        Returns True if a synchronisation job is running right now
        """
        return RedLock("wagtail_localize_pontoon.sync").locked()
