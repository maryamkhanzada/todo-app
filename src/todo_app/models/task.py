"""Task entity for the Todo application.

This module defines the Task class representing a single todo item.
"""


class Task:
    """Represents a todo task with id, title, description, and completion status.

    Attributes:
        id (int): Unique identifier for the task (auto-assigned).
        title (str): Short summary of the task.
        description (str): Detailed description of the task.
        completed (bool): Completion status (False = Pending, True = Completed).
    """

    def __init__(self, id: int, title: str, description: str, completed: bool = False):
        """Initialize a new Task.

        Args:
            id: Unique identifier for the task.
            title: Short summary of the task.
            description: Detailed description of the task.
            completed: Completion status, defaults to False (Pending).
        """
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

    def __repr__(self) -> str:
        """Return string representation of the Task."""
        status = "Completed" if self.completed else "Pending"
        return f"Task(id={self.id}, title='{self.title}', status={status})"
