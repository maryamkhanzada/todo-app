# Research: Intermediate Level Implementation

**Feature**: 001-intermediate-features
**Date**: 2025-12-30
**Phase**: 0 - Research & Technology Selection

## Overview

This document captures research decisions and best practices for implementing Intermediate Level features (priorities, tags, search, filter, sort) in the Todo CLI application.

## Technology Decisions

### 1. Python Standard Library Only

**Decision**: Use only Python 3.13+ standard library, no external dependencies

**Rationale**:
- Aligns with Basic Level approach (no dependencies used)
- All required functionality available in stdlib:
  - `dataclasses` or plain classes for data modeling
  - `datetime` for due date handling (ISO format)
  - `enum` for priority enumeration
  - Built-in list comprehensions for filtering
  - `sorted()` with custom key functions for sorting
  - `str.lower()` and `in` operator for case-insensitive search

**Alternatives Considered**:
- **Pydantic**: Rejected - adds external dependency for validation, overkill for in-memory CLI
- **attrs**: Rejected - adds external dependency, Python dataclasses sufficient
- **fuzzywuzzy**: Rejected - exact/partial substring matching sufficient per spec

**Impact**: Zero dependency overhead, fast startup, simple deployment

---

### 2. Priority Enum Pattern

**Decision**: Use string-based enum with validation in Task class

**Rationale**:
- Specification requires exactly three values: "high", "medium", "low"
- Python `enum.Enum` provides type safety and clear constants
- Alternative: plain strings with validation - simpler, more flexible for CLI input
- **Choice**: Plain strings with validation method (lighter weight, easier CLI integration)

**Implementation Pattern**:
```python
# In Task class
VALID_PRIORITIES = {'high', 'medium', 'low'}

def validate_priority(priority: str) -> str:
    if priority.lower() not in VALID_PRIORITIES:
        raise ValueError(f"Invalid priority. Must be one of: {', '.join(VALID_PRIORITIES)}")
    return priority.lower()
```

**Alternatives Considered**:
- **Python Enum**: Rejected - adds complexity for CLI string parsing, minimal benefit
- **Integer encoding (1-3)**: Rejected - less readable, spec specifies string values

**Impact**: Simple validation, clear error messages, easy CLI integration

---

### 3. Tag Storage & Normalization

**Decision**: Store tags as list of lowercase strings, normalize on input

**Rationale**:
- Specification requires case-insensitive matching (FR-012)
- Specification requires trimming whitespace (FR-013)
- Specification allows comma-separated input (FR-009)
- Storage as `list[str]` enables multiple tags per task (FR-008)

**Implementation Pattern**:
```python
# Parsing comma-separated input
def parse_tags(tag_input: str) -> list[str]:
    if not tag_input.strip():
        return []
    return [tag.strip().lower() for tag in tag_input.split(',') if tag.strip()]
```

**Alternatives Considered**:
- **Set storage**: Rejected - preserves insertion order less predictable, list sufficient
- **Preserve original case**: Rejected - violates spec requirement for case-insensitive storage

**Impact**: Consistent tag matching, prevents duplicates via normalization, simple CLI workflow

---

### 4. Due Date Format

**Decision**: Store as `datetime.date` object or None, display/input as ISO format (YYYY-MM-DD)

**Rationale**:
- Specification assumes ISO format for consistency (spec assumptions section)
- `datetime.date` enables proper date comparison for filtering and sorting
- Optional attribute (None when not set) per spec (FR-037)
- Python `datetime.strptime()` and `isoformat()` handle parsing and formatting

**Implementation Pattern**:
```python
from datetime import date

# In Task class
def parse_due_date(date_str: str | None) -> date | None:
    if not date_str or date_str.strip() == '':
        return None
    return date.fromisoformat(date_str)  # Raises ValueError if invalid format
```

**Alternatives Considered**:
- **String storage**: Rejected - complicates sorting and comparison
- **Unix timestamp**: Rejected - less readable, ISO format spec requirement
- **datetime.datetime**: Rejected - time component not needed for Intermediate level

**Impact**: Proper date sorting, clear display format, future-ready for Advanced Level time features

---

### 5. Search Algorithm

**Decision**: Case-insensitive substring matching using Python `in` operator

**Rationale**:
- Specification requires partial word matching (FR-021): "test" matches "testing"
- Specification requires case-insensitive matching (FR-016)
- Specification requires searching both title and description (FR-015)
- Python `in` operator with `.lower()` is O(n) for each field, efficient for <1000 tasks

**Implementation Pattern**:
```python
def search_tasks(keyword: str) -> list[Task]:
    keyword_lower = keyword.lower()
    return [
        task for task in tasks
        if keyword_lower in task.title.lower() or keyword_lower in task.description.lower()
    ]
```

**Alternatives Considered**:
- **Regular expressions**: Rejected - overkill for simple substring matching
- **Fuzzy matching**: Rejected - not required by spec, adds complexity
- **Full-text index**: Rejected - unnecessary for in-memory <1000 task limit

**Impact**: Simple, fast (<1s for 1000 tasks per SC-003), meets all spec requirements

---

### 6. Filter Implementation

**Decision**: Separate filter methods with AND logic for multiple filters

**Rationale**:
- Specification requires three filter types: status, priority, due date (FR-022, FR-023, FR-024)
- Specification assumes AND logic when multiple filters active (spec assumptions)
- Stateless filtering: apply filters dynamically, don't modify task list

**Implementation Pattern**:
```python
def filter_tasks(
    tasks: list[Task],
    status: str | None = None,  # 'completed' or 'pending'
    priority: str | None = None,  # 'high', 'medium', 'low'
    due_date_filter: dict | None = None  # {'op': 'before'/'after'/'on', 'date': date}
) -> list[Task]:
    filtered = tasks
    if status == 'completed':
        filtered = [t for t in filtered if t.completed]
    elif status == 'pending':
        filtered = [t for t in filtered if not t.completed]
    if priority:
        filtered = [t for t in filtered if t.priority == priority]
    if due_date_filter:
        # Apply date comparison based on operator
        filtered = apply_date_filter(filtered, due_date_filter)
    return filtered
```

**Alternatives Considered**:
- **Filter chain pattern**: Rejected - more complex than needed for three filter types
- **OR logic**: Rejected - spec assumes AND logic

**Impact**: Flexible filtering, clear semantics, easy to combine filters

---

### 7. Sort Implementation

**Decision**: Use Python `sorted()` with custom key functions, stable sort

**Rationale**:
- Specification requires three sort modes: due date, priority, alphabetical (FR-028, FR-029, FR-030)
- Specification requires stable sort (FR-034): preserve order for equal values
- Python `sorted()` is guaranteed stable sort
- Tasks without due dates go last when sorting by date (FR-031)

**Implementation Pattern**:
```python
def sort_tasks(tasks: list[Task], sort_by: str) -> list[Task]:
    if sort_by == 'due_date':
        # None values last, then sort by date
        return sorted(tasks, key=lambda t: (t.due_date is None, t.due_date or date.max))
    elif sort_by == 'priority':
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        return sorted(tasks, key=lambda t: priority_order[t.priority])
    elif sort_by == 'alphabetical':
        return sorted(tasks, key=lambda t: t.title.lower())
    return tasks
```

**Alternatives Considered**:
- **In-place sort**: Rejected - modifies original list, less predictable
- **Multi-key sort**: Rejected - spec requires single sort criterion at a time

**Impact**: Predictable sorting, meets <1s performance for 1000 tasks (SC-005)

---

### 8. Backward Compatibility Strategy

**Decision**: Add new attributes with default values, extend (don't replace) existing methods

**Rationale**:
- Specification requires Basic Level features remain fully functional (FR-038, SC-008)
- Existing tasks have no priority, tags, or due_date
- Default priority to "medium" (FR-004) for backward compatibility

**Implementation Pattern**:
```python
# Task class constructor
def __init__(
    self,
    id: int,
    title: str,
    description: str,
    completed: bool = False,
    priority: str = 'medium',  # NEW: default value
    tags: list[str] | None = None,  # NEW: optional
    due_date: date | None = None  # NEW: optional
):
    # ... existing initialization
    self.priority = priority
    self.tags = tags if tags is not None else []
    self.due_date = due_date
```

**Alternatives Considered**:
- **Migration pattern**: Rejected - in-memory only, no persisted data to migrate
- **Separate Task classes**: Rejected - violates single responsibility, complicates code

**Impact**: Seamless upgrade path, existing code continues working, new features opt-in

---

## Best Practices Applied

### CLI Interaction Patterns

1. **Menu-driven navigation**: Add new menu options for Search (6), Filter (7), Sort (8)
2. **Input validation**: Validate all user inputs with helpful error messages
3. **Confirmation prompts**: Not required for filters/sorts (non-destructive operations)
4. **Clear feedback**: Show count of results after search/filter operations

### Error Handling

1. **Invalid priority**: Show valid options (high, medium, low)
2. **Empty search**: Prompt for valid keyword
3. **No results**: Display friendly "no tasks found" message
4. **Invalid date format**: Show expected format (YYYY-MM-DD) and example

### Performance Considerations

1. **Linear scans acceptable**: <1000 tasks means O(n) operations complete in <1s
2. **No caching needed**: In-memory operations fast enough
3. **Lazy evaluation**: Apply filters/sorts only when requested, don't pre-compute

---

## Integration Points

### Changes Required

1. **Task Model (models/task.py)**:
   - Add `priority`, `tags`, `due_date` attributes
   - Add validation methods
   - Update `__repr__()` to show new attributes

2. **TaskManager Service (services/task_manager.py)**:
   - Add `search_tasks(keyword)` method
   - Add `filter_tasks(status, priority, due_date_filter)` method
   - Add `sort_tasks(sort_by)` method
   - Update existing methods to handle new attributes

3. **CLI Interface (cli/main.py)**:
   - Add menu options: Search (6), Filter (7), Sort (8)
   - Add handler functions for each new operation
   - Update Add Task and Update Task flows to prompt for priority/tags
   - Update View Tasks to display priority, tags, due date

### No Changes Required

1. **Existing Basic Level operations**: Add, View, Update, Delete, Complete - work as-is
2. **Project structure**: No new files or directories
3. **Dependencies**: No new packages to install

---

## Risk Mitigation

### Identified Risks

1. **Performance degradation with large lists**: Mitigated by spec limit of 1000 tasks and Python's optimized built-ins
2. **Date parsing errors**: Mitigated by clear format requirements and exception handling
3. **Breaking existing functionality**: Mitigated by default values and extending (not replacing) methods

### Testing Strategy (if tests were required)

1. Create tasks with and without new attributes
2. Verify backward compatibility: old operations work with new Task structure
3. Test edge cases: empty tags, missing due dates, invalid priorities
4. Performance test: 1000 tasks search/filter/sort under 1 second

---

## Summary

All technical decisions prioritize simplicity, maintainability, and spec compliance. No external dependencies required. All functionality achievable with Python 3.13+ standard library. Changes are incremental, backward-compatible, and align with existing architectural patterns.
