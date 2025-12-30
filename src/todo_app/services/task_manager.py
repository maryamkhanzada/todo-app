"""TaskManager service for managing tasks.

This module provides the TaskManager class for CRUD operations on tasks.
"""

import threading
from datetime import date, datetime, timedelta
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
        self.lock = threading.Lock()  # Thread-safe access for reminder service

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
        due_date: date | None = None,
        due_time: str | None = None,
        recurrence: dict | None = None,
        parent_recurrence_id: int | None = None,
        reminders: list[dict] | None = None
    ) -> Task:
        """Add a new task with auto-incremented ID and default Pending status.

        Args:
            title: Short summary of the task.
            description: Detailed description of the task.
            priority: Priority level (default: 'medium')
            tags: List of tags (default: empty list)
            due_date: Optional due date
            due_time: Optional time in HH:MM format (24-hour)
            recurrence: Recurrence pattern dict (default: {"type": "none", "interval": 1})
            parent_recurrence_id: Parent task ID for recurring occurrences
            reminders: List of reminder dicts (default: empty list)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is empty or priority/recurrence is invalid
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
            due_date=due_date,
            due_time=due_time,
            recurrence=recurrence,
            parent_recurrence_id=parent_recurrence_id,
            reminders=reminders if reminders is not None else []
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

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """Toggle the completion status of a task.

        For recurring tasks, generates next occurrence when marked as complete.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            New task occurrence if recurring task was completed, None otherwise.
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        # Toggle completion status
        was_completed = task.completed
        task.completed = not task.completed

        # If marking as complete and task has recurrence, create next occurrence
        if not was_completed and task.completed:
            if task.recurrence and task.recurrence.get("type") != "none":
                next_occurrence = self.create_next_occurrence(task)
                return next_occurrence

        return None

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[list[str]] = None,
        due_date: Optional[date] = None,
        due_time: Optional[str] = None,
        recurrence: Optional[dict] = None
    ) -> bool:
        """Update a task's title, description, priority, tags, due_date, due_time, and/or recurrence.

        Args:
            task_id: The ID of the task to update.
            title: New title for the task, or None to keep current.
            description: New description for the task, or None to keep current.
            priority: New priority for the task, or None to keep current.
            tags: New tags list for the task, or None to keep current.
            due_date: New due date for the task, or None to keep current.
            due_time: New time for the task, or None to keep current.
            recurrence: New recurrence pattern, or None to keep current.

        Returns:
            True if task was found and updated, False otherwise.

        Raises:
            ValueError: If task not found or invalid priority/time/recurrence
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
            if due_date is not None:
                task.due_date = due_date
            if due_time is not None:
                task.due_time = task._validate_due_time(due_time)
            if recurrence is not None:
                task.recurrence = task._validate_recurrence(recurrence)
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
            # Sort by due datetime (combines date + time, None values last)
            return sorted(
                self.tasks,
                key=lambda t: (t.get_due_datetime() is None, t.get_due_datetime() if t.get_due_datetime() else datetime.max)
            )
        elif sort_by == 'priority':
            # Sort by priority (high > medium > low)
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            return sorted(self.tasks, key=lambda t: priority_order.get(t.priority, 3))
        elif sort_by == 'alphabetical':
            # Sort alphabetically by title (case-insensitive)
            return sorted(self.tasks, key=lambda t: t.title.lower())

        return self.tasks

    def _get_recurrence_interval(self, recurrence: dict) -> int:
        """Get interval in days from recurrence pattern.

        Args:
            recurrence: Recurrence dict with type and interval

        Returns:
            Number of days between occurrences
        """
        rec_type = recurrence.get("type", "none")
        if rec_type == "daily":
            return 1
        elif rec_type == "weekly":
            return 7
        elif rec_type == "custom":
            return recurrence.get("interval", 1)
        return 0  # "none" type

    def _calculate_next_due_date(self, task: Task) -> datetime:
        """Calculate next occurrence due datetime from original due date.

        Args:
            task: The task with recurrence pattern

        Returns:
            datetime for next occurrence
        """
        if not task.due_date:
            # No due date: use current time + interval
            interval = self._get_recurrence_interval(task.recurrence)
            return datetime.now() + timedelta(days=interval)

        # Start from original due datetime
        next_dt = task.get_due_datetime()
        interval = self._get_recurrence_interval(task.recurrence)

        # Skip forward until future date
        now = datetime.now()
        while next_dt <= now:
            next_dt += timedelta(days=interval)

        return next_dt

    def create_next_occurrence(self, completed_task: Task) -> Task:
        """Create next occurrence of a recurring task.

        Args:
            completed_task: The completed recurring task

        Returns:
            New task instance for next occurrence
        """
        next_dt = self._calculate_next_due_date(completed_task)

        # Copy reminders with sent=False (reset for next occurrence)
        next_reminders = []
        if completed_task.reminders:
            for reminder in completed_task.reminders:
                next_reminders.append({
                    'offset_value': reminder['offset_value'],
                    'offset_unit': reminder['offset_unit'],
                    'sent': False,
                    'sent_at': None
                })

        # Create new task with same attributes
        next_task = self.add_task(
            title=completed_task.title,
            description=completed_task.description,
            priority=completed_task.priority,
            tags=completed_task.tags.copy() if completed_task.tags else [],
            due_date=next_dt.date(),
            due_time=next_dt.strftime("%H:%M"),
            recurrence=completed_task.recurrence.copy(),
            parent_recurrence_id=completed_task.parent_recurrence_id if completed_task.parent_recurrence_id else completed_task.id,
            reminders=next_reminders
        )

        return next_task

    def get_occurrence_history(self, task: Task) -> list[Task]:
        """Get all occurrences of a recurring task.

        Args:
            task: The recurring task

        Returns:
            List of all task occurrences (including original)
        """
        # Determine root task ID
        root_id = task.parent_recurrence_id if task.parent_recurrence_id else task.id

        # Get all tasks with matching parent_recurrence_id or root task itself
        occurrences = [t for t in self.tasks if t.id == root_id or t.parent_recurrence_id == root_id]

        # Sort by due date/time
        return sorted(occurrences, key=lambda t: t.get_due_datetime() if t.get_due_datetime() else datetime.min)
