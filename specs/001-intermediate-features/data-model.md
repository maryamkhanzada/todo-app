# Data Model: Intermediate Level

**Feature**: 001-intermediate-features
**Date**: 2025-12-30
**Phase**: 1 - Design & Contracts

## Overview

This document defines the enhanced Task entity data model for Intermediate Level, extending the Basic Level Task with organization and usability attributes.

## Entity: Task (Enhanced)

### Description

Represents a todo item with title, description, completion status, and new organizational attributes (priority, tags, due date).

### Attributes

| Attribute | Type | Required | Default | Description | Constraints |
|-----------|------|----------|---------|-------------|-------------|
| `id` | `int` | Yes | Auto-assigned | Unique identifier for the task | Positive integer, auto-incremented |
| `title` | `str` | Yes | N/A | Short summary of the task | Non-empty string |
| `description` | `str` | Yes | N/A | Detailed description of the task | Can be empty string |
| `completed` | `bool` | Yes | `False` | Completion status | `True` = Completed, `False` = Pending |
| `priority` | `str` | Yes | `'medium'` | Priority level of the task | Must be one of: `'high'`, `'medium'`, `'low'` (case-insensitive, stored as lowercase) |
| `tags` | `list[str]` | Yes | `[]` | List of category tags | List of lowercase strings, no duplicates, whitespace trimmed |
| `due_date` | `date \| None` | Yes | `None` | Optional due date for the task | ISO format (YYYY-MM-DD) or None |

### Validation Rules

#### Priority Validation (FR-001, FR-006)

```
VALID_PRIORITIES = {'high', 'medium', 'low'}

Rule: priority.lower() must be in VALID_PRIORITIES
Error: "Invalid priority. Must be one of: high, medium, low"
```

#### Tag Validation (FR-007, FR-012, FR-013)

```
Rule: Each tag must be a non-empty string after whitespace trimming
Rule: Tags are normalized to lowercase for case-insensitive matching
Rule: Duplicate tags are allowed (will be stored as entered)
Process: Input string split by comma, each tag trimmed and lowercased
```

#### Due Date Validation (FR-037)

```
Rule: Must be valid ISO format date (YYYY-MM-DD) or None
Rule: Date parsing uses datetime.date.fromisoformat()
Error: "Invalid date format. Use YYYY-MM-DD (e.g., 2025-12-31)"
```

### State Transitions

#### Completion Status

```
Pending (completed=False) <--toggle--> Completed (completed=True)
```

#### Priority Changes

```
Any priority --> Any other priority (user-driven, no automatic transitions)
```

#### Tags

```
Empty list --> Add tags --> Non-empty list
Non-empty list --> Modify/Remove tags --> Any state
```

#### Due Date

```
None --> Set due date --> date object
date object --> Clear due date --> None
date object --> Update due date --> different date object
```

### Business Rules

1. **Default Priority (FR-004)**: All tasks created without explicit priority are assigned `'medium'`
2. **Priority Immutability**: Priority does not change automatically; only user action changes priority
3. **Tag Order**: Tags are stored in the order entered (insertion order preserved)
4. **Case Normalization**: All priorities and tags are stored in lowercase for consistent matching
5. **Optional Attributes**: Tags list can be empty; due_date can be None (both are optional)
6. **Backward Compatibility**: Existing Basic Level tasks are treated as having priority='medium', tags=[], due_date=None

### Relationships

No relationships to other entities. Task is a standalone entity with no foreign keys or associations.

## Data Structures

### In-Memory Storage

Tasks are stored in a Python list maintained by TaskManager:

```python
# In TaskManager class
self._tasks: list[Task] = []
self._next_id: int = 1
```

### Indexing Strategy

No indexes required for Intermediate Level:
- Linear scans sufficient for <1000 tasks
- Search, filter, sort operations are O(n) and meet <1s performance requirement

Future optimization opportunity for Advanced Level: Consider dict-based indexes by priority or tags if performance becomes an issue.

## Example Task Instances

### Minimal Task (Basic Level compatibility)

```python
Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread",
    completed=False
    # priority defaults to 'medium'
    # tags defaults to []
    # due_date defaults to None
)
```

### Task with Priority

```python
Task(
    id=2,
    title="Finish project report",
    description="Q4 financial analysis",
    completed=False,
    priority='high'
)
```

### Task with Tags

```python
Task(
    id=3,
    title="Doctor appointment",
    description="Annual checkup at 2pm",
    completed=False,
    priority='medium',
    tags=['personal', 'health']
)
```

### Task with Due Date

```python
Task(
    id=4,
    title="Submit tax return",
    description="Federal and state taxes",
    completed=False,
    priority='high',
    tags=['personal', 'finance'],
    due_date=date(2025, 4, 15)
)
```

### Completed Task with All Attributes

```python
Task(
    id=5,
    title="Team meeting notes",
    description="Sprint retrospective - captured action items",
    completed=True,
    priority='low',
    tags=['work', 'meetings'],
    due_date=date(2025, 12, 20)
)
```

## Migration Considerations

### Backward Compatibility

**Existing Tasks**: No data migration needed (in-memory only). If tasks were persisted:
- Add `priority='medium'` to all existing tasks
- Add `tags=[]` to all existing tasks
- Add `due_date=None` to all existing tasks

**Code Compatibility**: All Basic Level operations work unchanged because new attributes have default values.

### Forward Compatibility

Design supports Advanced Level evolution:
- `due_date` attribute ready for time-of-day enhancement (change to `datetime.datetime`)
- Structure supports adding `recurrence_rule` attribute for recurring tasks
- Tag structure supports tag-based filtering and organization

## Constraints Summary

| Constraint | Rule | Error Message |
|------------|------|---------------|
| Priority values | Must be 'high', 'medium', or 'low' | "Invalid priority. Must be one of: high, medium, low" |
| Tag format | Non-empty after trimming, comma-separated input | "Tags must be comma-separated text" |
| Due date format | ISO YYYY-MM-DD or None | "Invalid date format. Use YYYY-MM-DD (e.g., 2025-12-31)" |
| Title required | Non-empty string | "Title cannot be empty" |
| ID uniqueness | Auto-incremented, never reused | N/A (system-enforced) |

## Performance Characteristics

| Operation | Complexity | Expected Time (1000 tasks) |
|-----------|------------|---------------------------|
| Create task | O(1) | <1ms |
| Read task by ID | O(n) | <1ms |
| Update task | O(n) | <1ms |
| Delete task | O(n) | <1ms |
| Search tasks | O(n * m) | <1s (m = avg field length) |
| Filter tasks | O(n) | <1s |
| Sort tasks | O(n log n) | <1s |

All operations meet success criteria performance requirements (SC-003, SC-004, SC-005).
