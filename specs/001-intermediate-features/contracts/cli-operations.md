# CLI Operation Contracts: Intermediate Level

**Feature**: 001-intermediate-features
**Date**: 2025-12-30
**Phase**: 1 - Design & Contracts

## Overview

This document defines the input/output contracts for all CLI operations in the Intermediate Level Todo application, including both existing Basic Level operations (unchanged) and new Intermediate Level operations.

---

## Basic Level Operations (Unchanged)

### 1. Add Task

**Menu Option**: 1
**Description**: Create a new task with title and description

**Inputs**:
- Title: string (required, prompted)
- Description: string (required, prompted)
- **NEW** Priority: string (optional, prompted) - "high", "medium", or "low"
- **NEW** Tags: string (optional, prompted) - comma-separated list

**Outputs**:
- Success: "Task added successfully! Task ID: {id}"
- Error (invalid priority): "Invalid priority. Must be one of: high, medium, low"

**Side Effects**:
- Creates new Task with auto-incremented ID
- Sets completed=False
- Sets priority to user input or "medium" if not provided
- Parses and stores tags as list

**Example Session**:
```
Enter task title: Buy groceries
Enter task description: Milk, eggs, bread
Enter priority (high/medium/low) or press Enter for default [medium]: high
Enter tags (comma-separated) or press Enter to skip: personal, shopping
Task added successfully! Task ID: 1
```

---

### 2. View Tasks

**Menu Option**: 2
**Description**: Display all tasks with their details

**Inputs**: None

**Outputs**:
- Success: List of tasks with ID, title, description, status, **priority**, **tags**, **due date**
- Empty state: "No tasks to display."
- **NEW** Display format includes priority, tags, and due date

**Example Output**:
```
=== All Tasks ===

[1] Buy groceries [HIGH] [personal, shopping]
    Description: Milk, eggs, bread
    Status: Pending
    Due: 2025-12-31

[2] Team meeting [MEDIUM] [work]
    Description: Discuss Q1 planning
    Status: Completed
    Due: None

No filters active | No sorting active
Total: 2 tasks
```

---

### 3. Update Task

**Menu Option**: 3
**Description**: Modify title, description, **priority**, or **tags** of an existing task

**Inputs**:
- Task ID: integer (required, prompted)
- New title: string (optional, press Enter to keep current)
- New description: string (optional, press Enter to keep current)
- **NEW** New priority: string (optional, press Enter to keep current)
- **NEW** New tags: string (optional, press Enter to keep current)

**Outputs**:
- Success: "Task {id} updated successfully!"
- Error (not found): "Task with ID {id} not found."
- Error (invalid ID): "Please enter a valid task ID."
- Error (invalid priority): "Invalid priority. Must be one of: high, medium, low"

**Example Session**:
```
Enter task ID to update: 1
Current title: Buy groceries
Enter new title (or press Enter to keep current):
Current description: Milk, eggs, bread
Enter new description (or press Enter to keep current): Milk, eggs, bread, cheese
Current priority: high
Enter new priority (or press Enter to keep current): medium
Current tags: personal, shopping
Enter new tags (or press Enter to keep current): personal, groceries
Task 1 updated successfully!
```

---

### 4. Delete Task

**Menu Option**: 4
**Description**: Remove a task permanently

**Inputs**:
- Task ID: integer (required, prompted)
- Confirmation: string (required, prompted) - "yes" or "no"

**Outputs**:
- Success: "Task {id} deleted successfully!"
- Cancelled: "Task deletion cancelled."
- Error (not found): "Task with ID {id} not found."
- Error (invalid ID): "Please enter a valid task ID."

**Behavior**: Unchanged from Basic Level

---

### 5. Mark Complete/Incomplete

**Menu Option**: 5
**Description**: Toggle completion status of a task

**Inputs**:
- Task ID: integer (required, prompted)

**Outputs**:
- Success (mark complete): "Task {id} marked as completed!"
- Success (mark incomplete): "Task {id} marked as incomplete!"
- Error (not found): "Task with ID {id} not found."
- Error (invalid ID): "Please enter a valid task ID."

**Behavior**: Unchanged from Basic Level

---

## New Intermediate Level Operations

### 6. Search Tasks

**Menu Option**: 6
**Description**: Find tasks by keyword in title or description (FR-014)

**Inputs**:
- Keyword: string (required, prompted, non-empty)

**Outputs**:
- Success: List of matching tasks with full details
- No matches: "No tasks found matching '{keyword}'."
- Error (empty keyword): "Please enter a search keyword."

**Matching Rules** (FR-015, FR-016, FR-021):
- Case-insensitive matching
- Partial word matching (substring)
- Searches both title and description fields

**Example Session**:
```
Enter search keyword: meet
=== Search Results for 'meet' ===

[2] Team meeting [MEDIUM] [work]
    Description: Discuss Q1 planning
    Status: Completed
    Due: None

[7] Client meeting prep [HIGH] [work]
    Description: Prepare slides and agenda
    Status: Pending
    Due: 2026-01-05

Found 2 tasks
```

---

### 7. Filter Tasks

**Menu Option**: 7
**Description**: Show tasks matching filter criteria (FR-022, FR-023, FR-024)

**Sub-Menu Options**:
1. Filter by Status
2. Filter by Priority
3. Filter by Due Date
4. Clear Filters
5. Back to Main Menu

**Inputs** (varies by filter type):

**7.1 Filter by Status**:
- Status: "completed" or "pending" (prompted)

**7.2 Filter by Priority**:
- Priority: "high", "medium", or "low" (prompted)

**7.3 Filter by Due Date**:
- Filter type: "before", "after", or "on" (prompted)
- Date: string in YYYY-MM-DD format (prompted)

**7.4 Clear Filters**:
- No input required

**Outputs**:
- Success: Filtered task list displayed
- Active filter indicator: "Active filters: status=completed, priority=high"
- No matches: "No tasks match the current filters."
- Error (invalid date): "Invalid date format. Use YYYY-MM-DD (e.g., 2025-12-31)"

**Filter Behavior** (FR-027):
- Filters persist until explicitly cleared or changed
- Multiple filters use AND logic (task must match all active filters)
- Viewing all tasks (option 2) shows current filters and filtered results

**Example Session**:
```
=== Filter Tasks ===
1. Filter by Status
2. Filter by Priority
3. Filter by Due Date
4. Clear Filters
5. Back to Main Menu

Choose filter option: 1
Select status (completed/pending): pending

Active filters: status=pending
Filtered results:

[1] Buy groceries [HIGH] [personal, shopping]
    Description: Milk, eggs, bread, cheese
    Status: Pending
    Due: 2025-12-31

[7] Client meeting prep [HIGH] [work]
    Description: Prepare slides and agenda
    Status: Pending
    Due: 2026-01-05

Showing 2 of 10 total tasks
```

---

### 8. Sort Tasks

**Menu Option**: 8
**Description**: Reorder task list by specified criteria (FR-028, FR-029, FR-030)

**Sub-Menu Options**:
1. Sort by Due Date (earliest first)
2. Sort by Priority (high to low)
3. Sort Alphabetically (A-Z)
4. Clear Sort
5. Back to Main Menu

**Inputs**: Selection of sort option (1-5)

**Outputs**:
- Success: Task list displayed in sorted order
- Active sort indicator: "Sorted by: due_date"
- Info: Tasks without due dates appear last when sorting by due date (FR-031)

**Sort Behavior** (FR-032, FR-033, FR-034):
- Sort order persists until explicitly changed or cleared
- Newly added tasks appear in correct sorted position
- Stable sort: tasks with equal values preserve original order
- Viewing all tasks (option 2) shows current sort order

**Sort Keys**:
- **Due Date**: Tasks sorted by due_date ascending; None values last
- **Priority**: high (0) > medium (1) > low (2)
- **Alphabetical**: Case-insensitive title comparison (A-Z)

**Example Session**:
```
=== Sort Tasks ===
1. Sort by Due Date (earliest first)
2. Sort by Priority (high to low)
3. Sort Alphabetically (A-Z)
4. Clear Sort
5. Back to Main Menu

Choose sort option: 2

Sorted by: priority

[1] Buy groceries [HIGH] [personal, shopping]
    Due: 2025-12-31

[7] Client meeting prep [HIGH] [work]
    Due: 2026-01-05

[4] Submit tax return [MEDIUM] [personal, finance]
    Due: 2026-04-15

[2] Team meeting [MEDIUM] [work]
    Due: None

[5] Read book [LOW] [personal]
    Due: None

Showing 5 tasks
```

---

### 9. Exit

**Menu Option**: 9 (renumbered from 6 due to new options)
**Description**: Exit the application

**Inputs**: None

**Outputs**: "Goodbye!"

**Side Effects**: Program terminates, all data lost (in-memory only)

---

## Error Handling

### Common Error Responses

| Error Condition | User Message |
|----------------|--------------|
| Invalid menu choice | "Invalid choice. Please select a number from 1-9." |
| Invalid task ID (non-numeric) | "Please enter a valid task ID." |
| Task not found | "Task with ID {id} not found." |
| Empty required field | "This field cannot be empty." |
| Invalid priority | "Invalid priority. Must be one of: high, medium, low" |
| Invalid date format | "Invalid date format. Use YYYY-MM-DD (e.g., 2025-12-31)" |
| Empty search keyword | "Please enter a search keyword." |

### Input Validation

All user inputs are validated before processing:
- Task IDs: Must be numeric and exist in task list
- Priorities: Must be one of the three valid values
- Dates: Must parse as valid ISO format
- Keywords: Must be non-empty after trimming

---

## Display Format Conventions

### Task Display Template

```
[{id}] {title} [{PRIORITY}] [{tags}]
    Description: {description}
    Status: {Completed|Pending}
    Due: {YYYY-MM-DD|None}
```

### Priority Display

- HIGH: Display in uppercase
- MEDIUM: Display in uppercase
- LOW: Display in uppercase

### Tags Display

- Comma-separated: `[work, urgent]`
- Empty: No tag indicator shown
- Lowercase: Display as stored

### Date Display

- Present: `YYYY-MM-DD` format
- Absent: `None`

### Status Indicators

At bottom of filtered/sorted views:
```
Active filters: {filter_summary} | Sorted by: {sort_key}
Showing {filtered_count} of {total_count} total tasks
```

---

## State Management

### Filter State

```python
current_filters = {
    'status': None | 'completed' | 'pending',
    'priority': None | 'high' | 'medium' | 'low',
    'due_date_filter': None | {'op': 'before'|'after'|'on', 'date': date}
}
```

### Sort State

```python
current_sort = None | 'due_date' | 'priority' | 'alphabetical'
```

State persists across menu operations until explicitly cleared or application exits.

---

## Performance Contracts

Per success criteria, all operations must complete within specified time limits:

| Operation | Max Response Time (1000 tasks) |
|-----------|-------------------------------|
| Search | <1 second (SC-003) |
| Filter | <1 second (SC-004) |
| Sort | <1 second (SC-005) |
| Add/Update/Delete | <2 seconds (SC-001) |

---

## Backward Compatibility

All Basic Level operations (1-5) continue working with new Task structure:
- Optional priority prompt in Add/Update (press Enter to skip)
- Priority/tags/due date display in View (show defaults if not set)
- No changes to Delete or Complete operations
