"""Task entity for the Todo application.

This module defines the Task class representing a single todo item.
"""

from datetime import date, datetime


class Task:
    """Represents a todo task with id, title, description, and completion status.

    Attributes:
        id (int): Unique identifier for the task (auto-assigned).
        title (str): Short summary of the task.
        description (str): Detailed description of the task.
        completed (bool): Completion status (False = Pending, True = Completed).
        priority (str): Priority level (high, medium, low).
        tags (list[str]): List of category tags.
        due_date (date | None): Optional due date for the task.
        due_time (str | None): Optional time component in HH:MM format (defaults to "23:59" if due_date set).
        recurrence (dict): Recurrence pattern with type ("none", "daily", "weekly", "custom") and interval (days).
        parent_recurrence_id (int | None): ID of parent task if this is a recurring occurrence.
        reminders (list[dict]): List of reminder dicts with offset_value, offset_unit, sent, sent_at.
    """

    VALID_PRIORITIES = {'high', 'medium', 'low'}
    VALID_RECURRENCE_TYPES = {'none', 'daily', 'weekly', 'custom'}

    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        completed: bool = False,
        priority: str = 'medium',
        tags: list[str] | None = None,
        due_date: date | None = None,
        due_time: str | None = None,
        recurrence: dict | None = None,
        parent_recurrence_id: int | None = None,
        reminders: list[dict] | None = None
    ):
        """Initialize a new Task.

        Args:
            id: Unique identifier for the task.
            title: Short summary of the task.
            description: Detailed description of the task.
            completed: Completion status, defaults to False (Pending).
            priority: Priority level, defaults to 'medium'.
            tags: List of tags, defaults to empty list.
            due_date: Optional due date.
            due_time: Optional time in HH:MM format (24-hour).
            recurrence: Recurrence pattern dict, defaults to {"type": "none", "interval": 1}.
            parent_recurrence_id: Parent task ID for recurring occurrences.
            reminders: List of reminder dicts, defaults to empty list.
        """
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

        # Validate and set priority
        self.priority = self._validate_priority(priority)

        # Initialize tags (empty list if None)
        self.tags = tags if tags is not None else []

        # Set due date
        self.due_date = due_date

        # Validate and set due time
        self.due_time = self._validate_due_time(due_time)

        # Validate and set recurrence
        self.recurrence = self._validate_recurrence(recurrence)

        # Set parent recurrence ID (for tracking recurring task occurrences)
        self.parent_recurrence_id = parent_recurrence_id

        # Initialize reminders (empty list if None)
        self.reminders = reminders if reminders is not None else []

    @classmethod
    def _validate_priority(cls, priority: str) -> str:
        """Validate priority value and return normalized (lowercase) version.

        Args:
            priority: Priority level to validate

        Returns:
            Validated priority in lowercase

        Raises:
            ValueError: If priority is not one of the valid values
        """
        priority_lower = priority.lower()
        if priority_lower not in cls.VALID_PRIORITIES:
            valid_options = ', '.join(sorted(cls.VALID_PRIORITIES))
            raise ValueError(f"Invalid priority. Must be one of: {valid_options}")
        return priority_lower

    def _validate_due_time(self, due_time: str | None) -> str | None:
        """Validate due_time format and return normalized value.

        Args:
            due_time: Time string in HH:MM format or None

        Returns:
            Validated time string or None

        Raises:
            ValueError: If time format is invalid
        """
        if due_time is None:
            return None

        # Import here to avoid circular dependency
        from ..utils.time_utils import validate_time

        if not validate_time(due_time):
            raise ValueError(f"Invalid time format: '{due_time}'. Must be HH:MM in 24-hour format (e.g., '14:30', '09:00')")

        return due_time

    def _validate_recurrence(self, recurrence: dict | None) -> dict:
        """Validate recurrence pattern and return normalized value.

        Args:
            recurrence: Recurrence pattern dict or None

        Returns:
            Validated recurrence dict with type and interval

        Raises:
            ValueError: If recurrence pattern is invalid
        """
        if recurrence is None:
            return {"type": "none", "interval": 1}

        # Validate recurrence type
        rec_type = recurrence.get("type", "none").lower()
        if rec_type not in self.VALID_RECURRENCE_TYPES:
            valid_options = ', '.join(sorted(self.VALID_RECURRENCE_TYPES))
            raise ValueError(f"Invalid recurrence type: '{rec_type}'. Must be one of: {valid_options}")

        # Set interval based on type
        if rec_type == "daily":
            interval = 1
        elif rec_type == "weekly":
            interval = 7
        elif rec_type == "custom":
            interval = recurrence.get("interval", 1)
            if not isinstance(interval, int) or interval < 1 or interval > 365:
                raise ValueError(f"Custom recurrence interval must be between 1 and 365 days, got: {interval}")
        else:  # "none"
            interval = 1

        return {"type": rec_type, "interval": interval}

    def get_due_datetime(self) -> datetime | None:
        """Combine due_date and due_time into datetime object.

        Returns:
            datetime combining date and time, or None if no due_date.
            If due_time is not set, defaults to 23:59 (end of day).
        """
        if not self.due_date:
            return None

        time_str = self.due_time if self.due_time else "23:59"
        hour, minute = map(int, time_str.split(':'))

        return datetime.combine(
            self.due_date,
            datetime.min.time().replace(hour=hour, minute=minute)
        )

    def get_reminder_trigger_time(self, reminder: dict) -> datetime | None:
        """Calculate absolute time when reminder should trigger.

        Args:
            reminder: Reminder dict with offset_value and offset_unit

        Returns:
            datetime when reminder should trigger, or None if no due date
        """
        # Import here to avoid circular dependency
        from ..utils.time_utils import calculate_reminder_trigger_time

        due_datetime = self.get_due_datetime()
        if not due_datetime:
            return None

        return calculate_reminder_trigger_time(due_datetime, reminder)

    def __repr__(self) -> str:
        """Return string representation of the Task."""
        status = "Completed" if self.completed else "Pending"
        tags_str = f", tags={self.tags}" if self.tags else ""

        # Format due date and time
        if self.due_date:
            if self.due_time:
                due_str = f", due={self.due_date.isoformat()} {self.due_time}"
            else:
                due_str = f", due={self.due_date.isoformat()}"
        else:
            due_str = ""

        # Format recurrence
        if self.recurrence and self.recurrence.get("type") != "none":
            rec_type = self.recurrence["type"]
            if rec_type == "daily":
                rec_str = ", recurrence=daily"
            elif rec_type == "weekly":
                rec_str = ", recurrence=weekly"
            elif rec_type == "custom":
                interval = self.recurrence.get("interval", 1)
                rec_str = f", recurrence=every {interval} days"
            else:
                rec_str = ""
        else:
            rec_str = ""

        # Format reminders count
        if self.reminders and len(self.reminders) > 0:
            reminders_str = f", reminders={len(self.reminders)}"
        else:
            reminders_str = ""

        return f"Task(id={self.id}, title='{self.title}', status={status}, priority={self.priority}{tags_str}{due_str}{rec_str}{reminders_str})"
