"""Task entity for the Todo application.

This module defines the Task class representing a single todo item.
"""

from datetime import date


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
    """

    VALID_PRIORITIES = {'high', 'medium', 'low'}

    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        completed: bool = False,
        priority: str = 'medium',
        tags: list[str] | None = None,
        due_date: date | None = None
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

    def __repr__(self) -> str:
        """Return string representation of the Task."""
        status = "Completed" if self.completed else "Pending"
        tags_str = f", tags={self.tags}" if self.tags else ""
        due_str = f", due={self.due_date.isoformat()}" if self.due_date else ""
        return f"Task(id={self.id}, title='{self.title}', status={status}, priority={self.priority}{tags_str}{due_str})"
