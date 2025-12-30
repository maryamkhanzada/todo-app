# Quickstart Guide: Intermediate Level Features

**Feature**: 001-intermediate-features
**Date**: 2025-12-30
**Audience**: Developers implementing Intermediate Level

## Overview

This guide provides step-by-step instructions for implementing Intermediate Level features (priorities, tags, search, filter, sort) in the Todo CLI application.

## Prerequisites

- Python 3.13 or higher installed
- UV package manager installed
- Basic Level (Phase I) implementation complete and working
- Familiarity with existing codebase structure:
  - `src/todo_app/models/task.py` - Task entity
  - `src/todo_app/services/task_manager.py` - Business logic
  - `src/todo_app/cli/main.py` - CLI interface

## Implementation Roadmap

Implementation follows user story priority order for incremental delivery:

```
P1: Priorities → P2: Tags → P3: Search → P4: Filter → P5: Sort
```

Each phase can be implemented, tested, and deployed independently.

---

## Phase 1: Extend Task Model (P1 Foundation)

**Goal**: Add priority, tags, and due_date attributes to Task entity

**File**: `src/todo_app/models/task.py`

### Changes Required

1. Add new attributes to `__init__()` method with defaults
2. Update `__repr__()` to display new attributes
3. Add validation methods for priority

### Implementation Steps

**Step 1.1**: Import datetime module

```python
from datetime import date
```

**Step 1.2**: Add class-level constants

```python
class Task:
    """Represents a todo task with organizational attributes."""

    VALID_PRIORITIES = {'high', 'medium', 'low'}
```

**Step 1.3**: Extend constructor signature

```python
def __init__(
    self,
    id: int,
    title: str,
    description: str,
    completed: bool = False,
    priority: str = 'medium',           # NEW
    tags: list[str] | None = None,      # NEW
    due_date: date | None = None        # NEW
):
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
```

**Step 1.4**: Add validation method

```python
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
```

**Step 1.5**: Update `__repr__()` method

```python
def __repr__(self) -> str:
    """Return string representation of the Task."""
    status = "Completed" if self.completed else "Pending"
    tags_str = f", tags={self.tags}" if self.tags else ""
    due_str = f", due={self.due_date.isoformat()}" if self.due_date else ""
    return f"Task(id={self.id}, title='{self.title}', status={status}, priority={self.priority}{tags_str}{due_str})"
```

---

## Phase 2: Update TaskManager Service (P1-P5)

**Goal**: Add search, filter, and sort methods to TaskManager

**File**: `src/todo_app/services/task_manager.py`

### Changes Required

1. Add tag parsing helper method
2. Add search_tasks() method
3. Add filter_tasks() method with support for status, priority, due date
4. Add sort_tasks() method with multiple sort keys
5. Update add_task() and update_task() to handle new attributes

### Implementation Steps

**Step 2.1**: Add tag parsing helper

```python
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
```

**Step 2.2**: Update add_task() method

```python
def add_task(
    self,
    title: str,
    description: str,
    priority: str = 'medium',
    tags: list[str] | None = None,
    due_date: date | None = None
) -> Task:
    """Add a new task with organizational attributes.

    Args:
        title: Task title
        description: Task description
        priority: Priority level (default: 'medium')
        tags: List of tags (default: empty list)
        due_date: Optional due date

    Returns:
        The newly created Task

    Raises:
        ValueError: If title is empty or priority is invalid
    """
    if not title.strip():
        raise ValueError("Task title cannot be empty")

    task = Task(
        id=self._next_id,
        title=title.strip(),
        description=description.strip(),
        priority=priority,
        tags=tags if tags is not None else [],
        due_date=due_date
    )
    self._tasks.append(task)
    self._next_id += 1
    return task
```

**Step 2.3**: Add search_tasks() method

```python
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
        task for task in self._tasks
        if keyword_lower in task.title.lower() or keyword_lower in task.description.lower()
    ]
```

**Step 2.4**: Add filter_tasks() method

```python
def filter_tasks(
    self,
    status: str | None = None,
    priority: str | None = None,
    due_date_op: str | None = None,
    due_date_value: date | None = None
) -> list[Task]:
    """Filter tasks by status, priority, and/or due date.

    Args:
        status: 'completed' or 'pending' (optional)
        priority: 'high', 'medium', or 'low' (optional)
        due_date_op: 'before', 'after', or 'on' (optional)
        due_date_value: Date to compare against (required if due_date_op provided)

    Returns:
        List of tasks matching all active filter criteria (AND logic)
    """
    filtered = self._tasks

    # Filter by status
    if status == 'completed':
        filtered = [t for t in filtered if t.completed]
    elif status == 'pending':
        filtered = [t for t in filtered if not t.completed]

    # Filter by priority
    if priority:
        filtered = [t for t in filtered if t.priority == priority.lower()]

    # Filter by due date
    if due_date_op and due_date_value:
        if due_date_op == 'before':
            filtered = [t for t in filtered if t.due_date and t.due_date < due_date_value]
        elif due_date_op == 'after':
            filtered = [t for t in filtered if t.due_date and t.due_date > due_date_value]
        elif due_date_op == 'on':
            filtered = [t for t in filtered if t.due_date == due_date_value]

    return filtered
```

**Step 2.5**: Add sort_tasks() method

```python
def sort_tasks(self, sort_by: str) -> list[Task]:
    """Sort tasks by specified criteria.

    Args:
        sort_by: 'due_date', 'priority', or 'alphabetical'

    Returns:
        New list of tasks in sorted order (original list unchanged)

    Raises:
        ValueError: If sort_by is not a valid option
    """
    if sort_by == 'due_date':
        # None values last, then sort by date
        return sorted(
            self._tasks,
            key=lambda t: (t.due_date is None, t.due_date if t.due_date else date.max)
        )
    elif sort_by == 'priority':
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        return sorted(self._tasks, key=lambda t: priority_order[t.priority])
    elif sort_by == 'alphabetical':
        return sorted(self._tasks, key=lambda t: t.title.lower())
    else:
        raise ValueError(f"Invalid sort option: {sort_by}")
```

**Step 2.6**: Update update_task() method

```python
def update_task(
    self,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    tags: list[str] | None = None
) -> Task:
    """Update an existing task's attributes.

    Args:
        task_id: ID of task to update
        title: New title (optional, None = no change)
        description: New description (optional, None = no change)
        priority: New priority (optional, None = no change)
        tags: New tags list (optional, None = no change)

    Returns:
        The updated Task

    Raises:
        ValueError: If task not found or invalid priority
    """
    task = self.get_task_by_id(task_id)
    if not task:
        raise ValueError(f"Task with ID {task_id} not found")

    if title is not None:
        task.title = title.strip()
    if description is not None:
        task.description = description.strip()
    if priority is not None:
        task.priority = task._validate_priority(priority)
    if tags is not None:
        task.tags = tags

    return task
```

---

## Phase 3: Update CLI Interface (P1-P5)

**Goal**: Add menu options and handlers for new features

**File**: `src/todo_app/cli/main.py`

### Changes Required

1. Add menu options 6-8 (Search, Filter, Sort)
2. Renumber Exit to option 9
3. Update add_task_handler() to prompt for priority and tags
4. Update update_task_handler() to prompt for priority and tags
5. Update view_tasks_handler() to display new attributes
6. Add search_handler()
7. Add filter_handler() with sub-menu
8. Add sort_handler() with sub-menu
9. Add filter/sort state management

### Implementation Highlights

**Main Menu**:
```python
def display_menu():
    print("\n=== Todo Application ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("6. Search Tasks")           # NEW
    print("7. Filter Tasks")            # NEW
    print("8. Sort Tasks")              # NEW
    print("9. Exit")                    # RENUMBERED
```

**Add Task Handler** (excerpt showing new prompts):
```python
priority_input = input("Enter priority (high/medium/low) or press Enter for default [medium]: ").strip()
priority = priority_input if priority_input else 'medium'

tags_input = input("Enter tags (comma-separated) or press Enter to skip: ").strip()
tags = task_manager.parse_tags(tags_input)

# Optional: due date prompt
due_date = None  # Intermediate level: due date setting in Advanced level
```

**View Tasks Handler** (enhanced display):
```python
def display_task(task):
    priority_display = task.priority.upper()
    tags_display = f"[{', '.join(task.tags)}]" if task.tags else ""
    due_display = task.due_date.isoformat() if task.due_date else "None"
    status = "Completed" if task.completed else "Pending"

    print(f"\n[{task.id}] {task.title} [{priority_display}] {tags_display}")
    print(f"    Description: {task.description}")
    print(f"    Status: {status}")
    print(f"    Due: {due_display}")
```

**Search Handler**:
```python
def search_handler(task_manager):
    keyword = input("\nEnter search keyword: ").strip()
    try:
        results = task_manager.search_tasks(keyword)
        if results:
            print(f"\n=== Search Results for '{keyword}' ===")
            for task in results:
                display_task(task)
            print(f"\nFound {len(results)} task(s)")
        else:
            print(f"No tasks found matching '{keyword}'.")
    except ValueError as e:
        print(f"Error: {e}")
```

**Filter/Sort State** (global or in main function scope):
```python
# State tracking
active_filters = {'status': None, 'priority': None, 'due_date': None}
active_sort = None
```

---

## Testing Checklist

### Manual Testing Scenarios

**P1 - Priorities**:
- [ ] Create task with high priority
- [ ] Create task with medium priority (default)
- [ ] Create task with low priority
- [ ] Update task priority
- [ ] Reject invalid priority
- [ ] View tasks shows priority

**P2 - Tags**:
- [ ] Create task with single tag
- [ ] Create task with multiple tags
- [ ] Create task with no tags
- [ ] Update task tags
- [ ] Tags stored lowercase
- [ ] View tasks shows tags

**P3 - Search**:
- [ ] Search finds tasks in title
- [ ] Search finds tasks in description
- [ ] Search is case-insensitive
- [ ] Partial word matching works
- [ ] No results message
- [ ] Empty keyword rejected

**P4 - Filter**:
- [ ] Filter by completed status
- [ ] Filter by pending status
- [ ] Filter by priority (each level)
- [ ] Filter by due date (before/after/on)
- [ ] Multiple filters use AND logic
- [ ] Clear filters works

**P5 - Sort**:
- [ ] Sort by due date (earliest first, None last)
- [ ] Sort by priority (high > medium > low)
- [ ] Sort alphabetically (A-Z, case-insensitive)
- [ ] Stable sort preserves order
- [ ] Clear sort works

**Backward Compatibility**:
- [ ] All Basic Level operations still work
- [ ] Existing tasks display with defaults
- [ ] No breaking changes to CRUD operations

---

## Performance Validation

Run with 1000 tasks to verify:
- [ ] Search completes in <1 second
- [ ] Filter completes in <1 second
- [ ] Sort completes in <1 second
- [ ] Add/Update completes in <2 seconds

---

## Deployment Steps

1. **Verify Basic Level is working**: Run application, test CRUD operations
2. **Create feature branch**: `git checkout -b 001-intermediate-features`
3. **Implement changes**: Follow phases 1-3 above
4. **Test incrementally**: After each phase, verify functionality
5. **Final testing**: Complete testing checklist
6. **Performance check**: Validate with 1000 tasks
7. **Merge to main**: After all tests pass

---

## Troubleshooting

### Common Issues

**Issue**: `ValueError: Invalid priority`
- **Cause**: Priority not one of valid values
- **Fix**: Ensure priority is 'high', 'medium', or 'low' (case-insensitive)

**Issue**: Tags not displaying
- **Cause**: Tags list is empty
- **Fix**: Check tag parsing logic, ensure comma-separated input

**Issue**: Sort not working
- **Cause**: Invalid sort key
- **Fix**: Use 'due_date', 'priority', or 'alphabetical' exactly

**Issue**: Filter returns empty list
- **Cause**: No tasks match all active filters (AND logic)
- **Fix**: Clear some filters or check task attributes

---

## Next Steps

After Intermediate Level is complete:
- Generate tasks.md using `/sp.tasks`
- Implement tasks in priority order
- Test each user story independently
- Prepare for Advanced Level (recurring tasks, reminders)

---

## Reference Documentation

- [Specification](./spec.md) - Feature requirements
- [Data Model](./data-model.md) - Task entity details
- [CLI Contracts](./contracts/cli-operations.md) - Operation specifications
- [Research](./research.md) - Technology decisions
