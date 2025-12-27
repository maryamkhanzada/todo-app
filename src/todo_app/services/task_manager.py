"""TaskManager service for managing tasks.

This module provides the TaskManager class for CRUD operations on tasks.
"""

from typing import List, Optional
from ..models.task import Task


class TaskManager:
    """Manages tasks with in-memory storage.

    Attributes:
        tasks (List[Task]): List of all tasks stored in memory.
        next_id (int): Counter for generating unique task IDs.
    """

    def __init__(self):
        """Initialize TaskManager with empty task list and ID counter starting at 1."""
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: str) -> Task:
        """Add a new task with auto-incremented ID and default Pending status.

        Args:
            title: Short summary of the task.
            description: Detailed description of the task.

        Returns:
            The newly created Task object.
        """
        task = Task(id=self.next_id, title=title, description=description, completed=False)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all Task objects.
        """
        return self.tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID.

        Args:
            task_id: The ID of the task to find.

        Returns:
            The Task object if found, None otherwise.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def toggle_task_completion(self, task_id: int) -> bool:
        """Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            True if task was found and toggled, False otherwise.
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = not task.completed
            return True
        return False

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title for the task, or None to keep current.
            description: New description for the task, or None to keep current.

        Returns:
            True if task was found and updated, False otherwise.
        """
        task = self.get_task_by_id(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if task was found and deleted, False otherwise.
        """
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
