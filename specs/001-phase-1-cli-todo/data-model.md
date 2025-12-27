# Data Model: Phase I - In-Memory CLI Todo Application

**Feature**: 001-phase-1-cli-todo
**Date**: 2025-12-27
**Version**: 1.0

## Overview

This document defines the data model for the Phase I Todo application. The model is intentionally simple, consisting of a single entity (Task) with minimal fields, reflecting the in-memory CLI nature of this phase.

## Entities

### Task

The Task entity represents a single todo item in the system.

**Purpose**: Store information about a task including its identity, content, and completion status.

**Lifecycle**: Tasks are created via the "Add Task" operation, can be modified via "Update Task", marked complete/incomplete via "Mark Complete/Incomplete", and deleted via "Delete Task". All tasks exist only in memory and are lost when the application exits.

**Fields**:

| Field Name | Type | Required | Default | Constraints | Description |
|------------|------|----------|---------|-------------|-------------|
| `id` | int | Yes | Auto-assigned | Unique, > 0, auto-incremented | Unique identifier for the task. Starts at 1 and increments for each new task. IDs are never reused, even after deletion. |
| `title` | str | Yes | None | Non-empty string | Short summary of the task. User-provided during task creation. Can be updated. |
| `description` | str | Yes | None | Non-empty string | Detailed description of the task. User-provided during task creation. Can be updated. |
| `completed` | bool | Yes | False | True or False | Completion status of the task. False = "Pending", True = "Completed". Defaults to False on creation. |

**Validation Rules**:

1. **ID Validation**:
   - IDs are system-assigned and cannot be manually set by users
   - IDs must be unique within the application session
   - IDs must be positive integers starting from 1
   - ID counter increments even when tasks are deleted (no ID reuse)

2. **Title Validation**:
   - Title cannot be empty (minimum length: 1 character)
   - Title is a string with no maximum length enforced (implementation may handle very long titles gracefully)
   - Title must be provided during task creation

3. **Description Validation**:
   - Description cannot be empty (minimum length: 1 character)
   - Description is a string with no maximum length enforced (implementation may handle very long descriptions gracefully)
   - Description must be provided during task creation

4. **Completed Validation**:
   - Must be a boolean value (True or False)
   - Cannot be null or undefined
   - Defaults to False (Pending) when a task is created

**State Transitions**:

```
[New Task Created]
       ↓
   completed = False ("Pending")
       ↓
   [User marks complete]
       ↓
   completed = True ("Completed")
       ↓
   [User marks incomplete]
       ↓
   completed = False ("Pending")
       ↓
   [Cycle can repeat]
```

**Business Rules**:

1. A task must always have all four fields (id, title, description, completed)
2. Only title and description can be modified after creation via "Update Task"
3. The ID field is immutable after assignment
4. The completed field can only be toggled via "Mark Complete/Incomplete" operations, not via "Update Task"
5. Tasks exist only in memory - no persistence between application sessions

## Relationships

**None** - This is a Phase I application with a single entity. No relationships exist.

Future phases may introduce:
- User entity (for multi-user support)
- Category/Tag entities (for organization)
- Project entity (for grouping tasks)

## Storage Implementation

**Phase I (In-Memory)**:

Tasks are stored in a Python list maintained by the TaskManager service:

```python
# Conceptual representation (not actual code)
tasks: List[Task] = []
next_id: int = 1
```

**Characteristics**:
- Tasks are stored in memory as Python objects
- No persistence to disk or database
- All data is lost when the application exits
- Operations (add, view, update, delete, complete) manipulate this in-memory list

**Future Evolution**:

The data model is designed to support future persistence layers:
- **Phase II**: File-based persistence (JSON, CSV, or SQLite)
- **Phase III**: Database persistence (PostgreSQL, MongoDB)
- **Phase IV**: Distributed storage (Redis, DynamoDB)

The simple structure (4 primitive fields) ensures easy serialization and migration across storage backends.

## Data Model Diagram

```
┌─────────────────────────────────┐
│           Task                  │
├─────────────────────────────────┤
│ - id: int (PK, auto-increment) │
│ - title: str                    │
│ - description: str              │
│ - completed: bool               │
├─────────────────────────────────┤
│ Methods: (None - plain data)   │
└─────────────────────────────────┘
```

## Sample Data

**Example 1: Pending Task**
```python
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread, and bananas",
    "completed": False
}
```

**Example 2: Completed Task**
```python
{
    "id": 2,
    "title": "Finish project proposal",
    "description": "Complete the Q1 project proposal and send to stakeholders",
    "completed": True
}
```

**Example 3: Task After Update**
```python
# Original
{
    "id": 3,
    "title": "Call doctor",
    "description": "Schedule annual checkup",
    "completed": False
}

# After Update (title changed)
{
    "id": 3,
    "title": "Call dentist",
    "description": "Schedule annual checkup and teeth cleaning",
    "completed": False
}
```

## Mapping to Requirements

This data model directly satisfies the following functional requirements:

- **FR-001**: System allows adding tasks with title and description → Task entity has title and description fields
- **FR-002**: Unique, auto-incremented ID → Task has id field with auto-increment behavior
- **FR-003**: Default "Pending" status → completed field defaults to False
- **FR-004**: View all tasks with ID, title, description, status → All fields present in Task entity
- **FR-006**: Update title and description → Task fields are mutable (except id)
- **FR-008**: Mark as Completed/Pending → completed boolean field supports toggle
- **FR-013**: In-memory storage → Storage implementation uses Python list

## Evolution Notes

This data model is designed for **simplicity and evolvability**:

1. **Simplicity**: Only 4 fields, all primitive types (int, str, bool) - easy to understand and implement
2. **Evolvability**: Structure supports future additions without breaking changes:
   - Add fields (e.g., `created_at`, `updated_at`, `priority`, `due_date`)
   - Add relationships (e.g., `user_id`, `category_id`)
   - Add methods (e.g., `is_overdue()`, `time_until_due()`)
3. **Persistence-agnostic**: Simple structure serializes easily to JSON, CSV, SQL, or NoSQL
4. **Constitutional alignment**: Follows "Designed for future extension" principle (Constitution VI)
