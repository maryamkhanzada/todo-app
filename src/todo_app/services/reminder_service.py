"""ReminderService for checking and triggering reminders.

This module provides the ReminderService class that runs a background daemon thread
to check for due reminders and trigger console notifications.
"""

import threading
import time
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task_manager import TaskManager


class ReminderService:
    """Background service for checking and triggering reminders.

    Attributes:
        task_manager (TaskManager): Reference to the task manager
        check_interval (int): Seconds between reminder checks (default: 60)
        running (bool): Whether the service is currently running
        thread (threading.Thread): Background daemon thread
    """

    def __init__(self, task_manager: 'TaskManager', check_interval: int = 60):
        """Initialize ReminderService.

        Args:
            task_manager: TaskManager instance to check tasks from
            check_interval: Seconds between checks (default: 60)
        """
        self.task_manager = task_manager
        self.check_interval = check_interval
        self.running = False
        self.thread = None

    def start(self):
        """Start the background reminder checking thread.

        Creates and starts a daemon thread that runs the check loop.
        """
        if self.running:
            print("[ReminderService] Already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._check_loop, daemon=True)
        self.thread.start()
        print(f"[ReminderService] Started (checking every {self.check_interval}s)")

    def stop(self):
        """Stop the background reminder checking thread gracefully.

        Sets running flag to False and waits for thread to finish.
        """
        if not self.running:
            return

        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        print("[ReminderService] Stopped")

    def _check_loop(self):
        """Main loop that runs in background thread.

        Periodically calls _check_all_reminders and sleeps between checks.
        """
        while self.running:
            try:
                self._check_all_reminders()
            except Exception as e:
                print(f"[ReminderService] Error in check loop: {e}")

            # Sleep in small intervals to allow quick shutdown
            for _ in range(self.check_interval):
                if not self.running:
                    break
                time.sleep(1)

    def _check_all_reminders(self):
        """Check all tasks for due reminders and trigger them.

        Thread-safe: Acquires lock before accessing task list.
        """
        now = datetime.now()

        # Thread-safe access to task list
        with self.task_manager.lock:
            tasks = list(self.task_manager.tasks)  # Create copy to release lock quickly

        for task in tasks:
            # Skip completed tasks
            if task.completed:
                continue

            # Check each reminder for this task
            for reminder in task.reminders:
                # Skip already-sent reminders
                if reminder.get('sent', False):
                    continue

                # Calculate trigger time
                trigger_time = task.get_reminder_trigger_time(reminder)
                if not trigger_time:
                    continue

                # Check if reminder is due
                if now >= trigger_time:
                    self._trigger_reminder(task, reminder)

    def _trigger_reminder(self, task, reminder):
        """Trigger a reminder notification.

        Args:
            task: The task with the reminder
            reminder: The reminder dict to trigger
        """
        # Mark reminder as sent
        reminder['sent'] = True
        reminder['sent_at'] = datetime.now()

        # Display console notification
        print("\n" + "=" * 60)
        print("⏰ REMINDER NOTIFICATION")
        print("=" * 60)
        print(f"Task: {task.title}")
        print(f"Description: {task.description}")

        # Format reminder offset
        offset_value = reminder.get('offset_value', 0)
        offset_unit = reminder.get('offset_unit', 'minutes')
        unit_display = offset_unit.rstrip('s') if offset_value == 1 else offset_unit
        print(f"Reminder: {offset_value} {unit_display} before due time")

        # Display due time
        if task.due_date:
            time_display = task.due_time if task.due_time else "23:59"
            print(f"Due: {task.due_date.isoformat()} {time_display}")

        print("=" * 60 + "\n")
