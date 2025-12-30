"""TaskManager service for managing tasks.

This module provides the TaskManager class for CRUD operations on tasks.
"""

from datetime import date
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

    @staticmethod
    def parse_tags(tag_input: str) -> list[str]:
        """Parse comma-separated tag input into list of normalized tags.

        Args:
            tag_input: Comma-separated string of tags

        Returns:
            List of lowercase, trimmed tag strings
        """
        if not tag_input or not tag_input.strip():
            return []
        return [tag.strip().lower() for tag in tag_input.split(',') if tag.strip()]

    def add_task(
        self,
        title: str,
        description: str,
        priority: str = 'medium',
        tags: list[str] | None = None,
        due_date: date | None = None
    ) -> Task:
        """Add a new task with auto-incremented ID and default Pending status.

        Args:
            title: Short summary of the task.
            description: Detailed description of the task.
            priority: Priority level (default: 'medium')
            tags: List of tags (default: empty list)
            due_date: Optional due date

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is empty or priority is invalid
        """
        if not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description.strip(),
            completed=False,
            priority=priority,
            tags=tags if tags is not None else [],
            due_date=due_date
        )
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

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[list[str]] = None
    ) -> bool:
        """Update a task's title, description, priority, and/or tags.

        Args:
            task_id: The ID of the task to update.
            title: New title for the task, or None to keep current.
            description: New description for the task, or None to keep current.
            priority: New priority for the task, or None to keep current.
            tags: New tags list for the task, or None to keep current.

        Returns:
            True if task was found and updated, False otherwise.

        Raises:
            ValueError: If task not found or invalid priority
        """
        task = self.get_task_by_id(task_id)
        if task:
            if title is not None:
                task.title = title.strip()
            if description is not None:
                task.description = description.strip()
            if priority is not None:
                task.priority = task._validate_priority(priority)
            if tags is not None:
                task.tags = tags
            return True
        return False

    def search_tasks(self, keyword: str) -> list[Task]:
        """Search for tasks containing keyword in title or description.

        Args:
            keyword: Search keyword (case-insensitive)

        Returns:
            List of tasks matching the keyword

        Raises:
            ValueError: If keyword is empty
        """
        if not keyword.strip():
            raise ValueError("Search keyword cannot be empty")

        keyword_lower = keyword.lower()
        return [
            task for task in self.tasks
            if keyword_lower in task.title.lower() or keyword_lower in task.description.lower()
        ]

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

    def filter_tasks(
        self,
        status: Optional[bool] = None,
        priority: Optional[str] = None,
        due_date_op: Optional[str] = None,
        due_date_value: Optional[date] = None
    ) -> list[Task]:
        """Filter tasks by status, priority, and/or due date.

        Args:
            status: Filter by completion status (True=completed, False=pending, None=all)
            priority: Filter by priority level ('high', 'medium', 'low', None=all)
            due_date_op: Due date operator ('before', 'after', 'on', None=no filter)
            due_date_value: Date value to compare against (required if due_date_op is set)

        Returns:
            List of tasks matching all filter criteria (AND logic)

        Raises:
            ValueError: If due_date_op is provided without due_date_value, or invalid operator
        """
        # Validate due date filter parameters
        if due_date_op and not due_date_value:
            raise ValueError("due_date_value is required when due_date_op is specified")
        if due_date_op and due_date_op not in ['before', 'after', 'on']:
            raise ValueError("due_date_op must be 'before', 'after', or 'on'")

        # Normalize priority if provided
        if priority:
            priority = priority.lower()
            if priority not in Task.VALID_PRIORITIES:
                valid_options = ', '.join(sorted(Task.VALID_PRIORITIES))
                raise ValueError(f"Invalid priority. Must be one of: {valid_options}")

        # Apply filters using AND logic
        results = self.tasks

        # Filter by status
        if status is not None:
            results = [task for task in results if task.completed == status]

        # Filter by priority
        if priority is not None:
            results = [task for task in results if task.priority == priority]

        # Filter by due date
        if due_date_op and due_date_value:
            if due_date_op == 'before':
                results = [task for task in results if task.due_date and task.due_date < due_date_value]
            elif due_date_op == 'after':
                results = [task for task in results if task.due_date and task.due_date > due_date_value]
            elif due_date_op == 'on':
                results = [task for task in results if task.due_date and task.due_date == due_date_value]

        return results

    def sort_tasks(self, sort_by: str) -> list[Task]:
        """Sort tasks by due date, priority, or alphabetically.

        Args:
            sort_by: Sort criterion ('due_date', 'priority', 'alphabetical')

        Returns:
            Sorted list of tasks

        Raises:
            ValueError: If sort_by is invalid
        """
        if sort_by not in ['due_date', 'priority', 'alphabetical']:
            raise ValueError("sort_by must be 'due_date', 'priority', or 'alphabetical'")

        if sort_by == 'due_date':
            # Sort by due date (None values last)
            # Use a tuple for sorting: (has_due_date, due_date_value)
            return sorted(
                self.tasks,
                key=lambda t: (t.due_date is None, t.due_date if t.due_date else date.max)
            )
        elif sort_by == 'priority':
            # Sort by priority (high > medium > low)
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            return sorted(self.tasks, key=lambda t: priority_order.get(t.priority, 3))
        elif sort_by == 'alphabetical':
            # Sort alphabetically by title (case-insensitive)
            return sorted(self.tasks, key=lambda t: t.title.lower())

        return self.tasks
