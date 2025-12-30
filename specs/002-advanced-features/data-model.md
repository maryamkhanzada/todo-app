# Data Model: Advanced Level Extensions

**Feature**: Advanced Level - Intelligent Task Management
**Date**: 2025-12-30
**Purpose**: Define entity extensions and relationships for time-aware task management

## Overview

This document specifies the data model changes required to support recurring tasks, time-aware due dates, and reminders. All changes extend the existing Task entity while maintaining backward compatibility with Basic and Intermediate level features.

---

## Entity: Task (Extended)

**Purpose**: Represents a todo item with scheduling intelligence (recurrence, precise timing, reminders)

### Existing Attributes (Unchanged)

From Basic Level (Phase I):
- `id: int` - Unique identifier (auto-incremented)
- `title: str` - Short summary of the task
- `description: str` - Detailed description
- `completed: bool` - Completion status (False = Pending, True = Completed)

From Intermediate Level (Phase II):
- `priority: str` - Priority level ("high", "medium", "low")
- `tags: list[str]` - Category tags (normalized to lowercase)
- `due_date: date | None` - Due date (date only, no time component)

### New Attributes (Advanced Level - Phase III)

#### due_time: str | None

**Purpose**: Time component for due dates, enabling time-of-day precision

**Format**: "HH:MM" (24-hour clock, e.g., "14:30", "09:00", "23:59")

**Default Value**:
- If `due_date` is set and `due_time` is None: defaults to "23:59" (end of day)
- If `due_date` is None: `due_time` is ignored (no meaning without date)

**Validation Rules**:
- Must match regex: `^([01][0-9]|2[0-3]):[0-5][0-9]$`
- Hour: 00-23, Minute: 00-59
- Reject invalid times: "25:00", "13:75", "9:30" (must be zero-padded)

**Backward Compatibility**:
- Existing tasks without `due_time` get "23:59" when accessed via `get_due_datetime()`
- No breaking changes to existing code

**Example Values**:
```python
task.due_date = date(2026, 1, 15)
task.due_time = "14:30"  # Due at 2:30 PM

task.due_date = date(2026, 1, 15)
task.due_time = None  # Defaults to "23:59" internally

task.due_date = None
task.due_time = "14:30"  # Ignored (no date to attach time to)
```

---

#### recurrence: dict

**Purpose**: Configuration for automatic task rescheduling on completion

**Structure**:
```python
{
    "type": str,    # "none" | "daily" | "weekly" | "custom"
    "interval": int # Days between occurrences (1 for daily, 7 for weekly, N for custom)
}
```

**Default Value**: `{"type": "none", "interval": 1}`

**Type Values**:
- **"none"**: No recurrence (default for all non-recurring tasks)
- **"daily"**: Task repeats every day (interval ignored, always 1)
- **"weekly"**: Task repeats every 7 days (interval ignored, always 7)
- **"custom"**: Task repeats every N days (interval specifies N, range: 1-365)

**Validation Rules**:
- `type` must be one of: "none", "daily", "weekly", "custom"
- `interval` must be integer in range 1-365 (only used for "custom" type)
- For "daily": interval internally set to 1
- For "weekly": interval internally set to 7
- For "none": interval value ignored

**Behavior**:
- When task marked complete, if `recurrence.type != "none"`, generate next occurrence
- Next occurrence due date calculated from original due_date + interval days
- If calculated date is in past, skip forward until future date found

**Example Values**:
```python
# Daily recurrence
task.recurrence = {"type": "daily", "interval": 1}

# Weekly recurrence
task.recurrence = {"type": "weekly", "interval": 7}

# Every 3 days (custom)
task.recurrence = {"type": "custom", "interval": 3}

# No recurrence (default)
task.recurrence = {"type": "none", "interval": 1}
```

---

#### reminders: list[dict]

**Purpose**: Scheduled notifications before task due date/time

**Structure**: List of reminder objects
```python
[
    {
        "offset_value": int,       # Numeric value (15, 60, 1440)
        "offset_unit": str,        # "minutes" | "hours" | "days"
        "sent": bool,              # Has notification been triggered?
        "sent_at": datetime | None # When notification was sent (None if not sent)
    }
]
```

**Default Value**: `[]` (empty list - no reminders)

**Validation Rules**:
- `offset_value` must be positive integer (1-999999)
- `offset_unit` must be one of: "minutes", "hours", "days"
- `sent` boolean (defaults to False when reminder created)
- `sent_at` nullable datetime (None until reminder triggers)

**Behavior**:
- Reminders trigger when `current_time >= (due_datetime - offset)`
- Offset examples:
  - `{"offset_value": 15, "offset_unit": "minutes"}` → 15 minutes before due time
  - `{"offset_value": 1, "offset_unit": "hours"}` → 1 hour before due time
  - `{"offset_value": 1, "offset_unit": "days"}` → 1 day (24 hours) before due time
- When triggered: `sent = True`, `sent_at = current_datetime`
- If task completed before reminder triggers: reminder cancelled (not triggered)
- If reminder time in past when created: warning displayed, reminder not triggered

**Multiple Reminders**:
- Task can have 0-N reminders
- Each reminder triggers independently
- Example: `[{...15 min...}, {...1 hour...}, {...1 day...}]` → 3 separate notifications

**Example Values**:
```python
# Single reminder: 15 minutes before
task.reminders = [
    {"offset_value": 15, "offset_unit": "minutes", "sent": False, "sent_at": None}
]

# Multiple reminders
task.reminders = [
    {"offset_value": 1, "offset_unit": "days", "sent": False, "sent_at": None},
    {"offset_value": 1, "offset_unit": "hours", "sent": False, "sent_at": None},
    {"offset_value": 15, "offset_unit": "minutes", "sent": False, "sent_at": None}
]

# No reminders (default)
task.reminders = []
```

---

#### parent_recurrence_id: int | None

**Purpose**: Links recurring task occurrences for history tracking

**Default Value**: `None` (for non-recurring tasks and first occurrence of recurring tasks)

**Behavior**:
- **Root task** (first occurrence): `parent_recurrence_id = None`
- **Generated occurrences**: `parent_recurrence_id = root_task.id`
- All occurrences of same recurring task share same `parent_recurrence_id` value

**Usage**:
- Query occurrence history: `[t for t in tasks if t.parent_recurrence_id == root_id]`
- Distinguish root from occurrence: `task.parent_recurrence_id is None` → root task
- Count completions: `len([t for t in tasks if t.parent_recurrence_id == X and t.completed])`

**Example**:
```python
# Original recurring task
original_task = Task(id=1, title="Weekly Report", recurrence={"type": "weekly", "interval": 7})
original_task.parent_recurrence_id = None  # Root task

# First completion generates occurrence
original_task.completed = True

# New occurrence created
occurrence_1 = Task(id=2, title="Weekly Report", recurrence={"type": "weekly", "interval": 7})
occurrence_1.parent_recurrence_id = 1  # Links to original

# Second completion generates another occurrence
occurrence_1.completed = True

# New occurrence created
occurrence_2 = Task(id=3, title="Weekly Report", recurrence={"type": "weekly", "interval": 7})
occurrence_2.parent_recurrence_id = 1  # Also links to original

# Query: Get all occurrences of original task
occurrences = [t for t in tasks if t.parent_recurrence_id == 1]  # [occurrence_1, occurrence_2]
```

---

## Helper Methods

### Task.get_due_datetime() -> datetime | None

**Purpose**: Combine `due_date` and `due_time` into single datetime for comparisons and sorting

**Implementation**:
```python
from datetime import datetime

def get_due_datetime(self) -> datetime | None:
    """Combine due_date and due_time into datetime object."""
    if not self.due_date:
        return None

    time_str = self.due_time if self.due_time else "23:59"
    hour, minute = map(int, time_str.split(':'))

    return datetime.combine(
        self.due_date,
        datetime.min.time().replace(hour=hour, minute=minute)
    )
```

**Returns**:
- `datetime` object combining date and time
- `None` if task has no due_date

**Usage**:
```python
# Sorting tasks by due datetime
tasks_sorted = sorted(tasks, key=lambda t: t.get_due_datetime() or datetime.max)

# Comparing due times
if task.get_due_datetime() < datetime.now():
    print("Task is overdue")
```

---

### Task.get_reminder_trigger_time(reminder: dict) -> datetime | None

**Purpose**: Calculate absolute time when reminder should trigger

**Implementation**:
```python
from datetime import datetime, timedelta

def get_reminder_trigger_time(self, reminder: dict) -> datetime | None:
    """Calculate when reminder should trigger."""
    due_dt = self.get_due_datetime()
    if not due_dt:
        return None

    offset_value = reminder['offset_value']
    offset_unit = reminder['offset_unit']

    # Convert offset to timedelta
    if offset_unit == 'minutes':
        delta = timedelta(minutes=offset_value)
    elif offset_unit == 'hours':
        delta = timedelta(hours=offset_value)
    elif offset_unit == 'days':
        delta = timedelta(days=offset_value)
    else:
        return None

    return due_dt - delta
```

**Returns**:
- `datetime` when reminder should trigger
- `None` if task has no due date/time

---

## Entity: ReminderService (New)

**Purpose**: Background service for checking and triggering reminders

**Not a data model entity** (service, not stored data), but included here for completeness.

**Responsibilities**:
- Run background thread checking for due reminders
- Trigger console notifications when reminder time reached
- Update reminder `sent` status and `sent_at` timestamp
- Thread-safe access to task list

**Key Methods**:
- `start()`: Start background polling thread (daemon mode)
- `stop()`: Stop background thread gracefully
- `_check_loop()`: 60-second polling loop (internal)
- `_check_all_reminders()`: Check all tasks for due reminders (internal)
- `_trigger_reminder(task, reminder)`: Display console notification (internal)

**See**: `contracts/cli-operations.md` for detailed method signatures

---

## Backward Compatibility

**Critical Requirement**: All existing Basic and Intermediate level features must continue working without modification.

### Compatibility Strategy

1. **New fields have sensible defaults**:
   - `due_time`: Defaults to "23:59" if `due_date` set (end of day)
   - `recurrence`: Defaults to `{"type": "none", "interval": 1}` (no recurrence)
   - `reminders`: Defaults to `[]` (no reminders)
   - `parent_recurrence_id`: Defaults to `None` (not a recurring occurrence)

2. **Existing fields unchanged**:
   - `due_date` remains `datetime.date` type (not replaced with datetime)
   - All Basic/Intermediate attributes retain same types and behavior

3. **Existing operations continue working**:
   - `add_task()` without time/recurrence/reminders creates Basic-level task
   - `update_task()` without time/recurrence/reminders works as before
   - `filter_tasks()`, `sort_tasks()`, `search_tasks()` work on new tasks

4. **Display compatibility**:
   - Tasks without `due_time` display date only (existing behavior)
   - Tasks without recurrence show no recurrence indicator
   - Tasks without reminders show no reminder status

### Migration Path

**No migration needed** - All existing tasks automatically compatible:
- Old tasks: `due_date = date(2026, 1, 15)`, no `due_time` → displays as "2026-01-15" (time hidden)
- New tasks: `due_date = date(2026, 1, 15)`, `due_time = "14:30"` → displays as "2026-01-15 14:30"

---

## Validation Summary

| Field | Required | Type | Validation |
|-------|----------|------|------------|
| `due_time` | No | `str | None` | Regex: `^([01][0-9]|2[0-3]):[0-5][0-9]$` |
| `recurrence.type` | Yes | `str` | Must be "none", "daily", "weekly", "custom" |
| `recurrence.interval` | Yes | `int` | Range: 1-365 (only used for "custom") |
| `reminders[].offset_value` | Yes | `int` | Range: 1-999999 |
| `reminders[].offset_unit` | Yes | `str` | Must be "minutes", "hours", "days" |
| `reminders[].sent` | Yes | `bool` | Defaults to False |
| `reminders[].sent_at` | No | `datetime | None` | None until triggered |
| `parent_recurrence_id` | No | `int | None` | Must reference existing task ID or None |

---

## Example: Complete Task Instance

```python
from datetime import date, datetime

# Advanced task with all features
task = Task(
    id=42,
    title="Weekly Team Meeting",
    description="Discuss project progress and blockers",
    completed=False,
    priority="high",
    tags=["work", "meeting"],
    due_date=date(2026, 1, 15),
    due_time="14:30",
    recurrence={"type": "weekly", "interval": 7},
    reminders=[
        {"offset_value": 1, "offset_unit": "days", "sent": False, "sent_at": None},
        {"offset_value": 15, "offset_unit": "minutes", "sent": False, "sent_at": None}
    ],
    parent_recurrence_id=None  # Root task
)

# Combining date + time
due_dt = task.get_due_datetime()  # datetime(2026, 1, 15, 14, 30)

# Reminder trigger times
reminder_1_time = task.get_reminder_trigger_time(task.reminders[0])  # 2026-01-14 14:30 (1 day before)
reminder_2_time = task.get_reminder_trigger_time(task.reminders[1])  # 2026-01-15 14:15 (15 min before)
```

---

## References

- **Specification**: specs/002-advanced-features/spec.md (Functional Requirements FR-029 to FR-032)
- **Research**: specs/002-advanced-features/research.md (Design decisions 1, 5, 8)
- **Contracts**: specs/002-advanced-features/contracts/cli-operations.md (Operation signatures)
