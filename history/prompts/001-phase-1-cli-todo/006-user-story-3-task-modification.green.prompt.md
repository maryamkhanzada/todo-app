---
id: 006
title: User Story 3 Task Modification Implementation
stage: green
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5
feature: 001-phase-1-cli-todo
branch: 001-phase-1-cli-todo
user: maryamkhanzada
command: implement
labels: ["implementation", "user-story-3", "task-modification", "phase-5"]
links:
  spec: specs/001-phase-1-cli-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/todo_app/services/task_manager.py
  - src/todo_app/cli/main.py
  - specs/001-phase-1-cli-todo/tasks.md
tests:
  - Manual validation: update_task with both title and description
  - Manual validation: update_task with title only (description unchanged)
  - Manual validation: update_task with description only (title unchanged)
  - Manual validation: update_task with invalid ID returns False
  - Manual validation: update_task with both fields None keeps task unchanged
  - Manual validation: Multiple tasks updated independently
  - Manual validation: CLI operation with numeric input validation
  - Manual validation: CLI operation displays current values
  - Manual validation: CLI operation prompts with "press Enter to keep current"
  - Manual validation: CLI operation handles empty input (keeps current values)
---

## Prompt

Implement User Story 3 (P3) - Task Modification in the Todo CLI application.

**Context:**
- Feature: Phase I - In-Memory CLI Todo Application
- Scope: Phase 5 - User Story 3 (Priority P3)
- Tasks: T025-T029 (5 tasks)
- Goal: Enable users to update task titles and descriptions

**Requirements from spec:**
- User can update task title and/or description by ID
- Display current values before prompting for updates
- Allow partial updates (title only, description only, or both)
- Prompt with "or press Enter to keep current" for each field
- Only update fields where user provides new values
- Validate task ID input (numeric, exists)
- Handle errors gracefully (invalid IDs, non-numeric input)
- Return to main menu after operation

**Acceptance Criteria:**
- User can update both title and description
- User can update only title (description unchanged)
- User can update only description (title unchanged)
- Pressing Enter without input keeps current value
- Changes are reflected in task list view
- Clear error messages for invalid input

## Response snapshot

Successfully completed all 5 tasks for User Story 3:

**TaskManager Service Updates (T025):**

Added `update_task` method to `src/todo_app/services/task_manager.py`:

```python
def update_task(self, task_id: int, title: Optional[str] = None,
                description: Optional[str] = None) -> bool:
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
```

Key features:
- Optional parameters (None = keep current value)
- Finds task using existing get_task_by_id method
- Updates only provided fields
- Returns success/failure boolean

**CLI Operation Implementation (T026-T029):**

Added `update_task_operation()` to `src/todo_app/cli/main.py`:

- Prompts user for task ID
- Validates numeric input (catches ValueError for non-numeric)
- Checks if task exists
- Displays current title and description
- Prompts for new title: "Enter new title (or press Enter to keep current):"
- Prompts for new description: "Enter new description (or press Enter to keep current):"
- Converts empty strings to None (keeps current values)
- Checks if at least one field was updated
- Displays appropriate messages:
  - Success: "Task updated successfully!"
  - No changes: "No changes made. Task remains unchanged."
  - Invalid ID: "Error: Task with ID {id} not found."
  - Non-numeric: "Error: Task ID must be a number."

Updated main() function to call the operation on menu choice "3"

**Validation Results:**
All tests passed:
- ✅ update_task updates both title and description
- ✅ update_task updates only title (description unchanged)
- ✅ update_task updates only description (title unchanged)
- ✅ update_task returns False for non-existent task (ID 999)
- ✅ update_task with both None keeps task unchanged
- ✅ Multiple tasks can be updated independently
- ✅ CLI operation validates numeric input
- ✅ CLI operation displays current values
- ✅ CLI operation handles empty input correctly

## Outcome

- ✅ Impact: User Story 3 fully implemented. Users can now update task titles and/or descriptions with flexible partial update support.
- 🧪 Tests: 9 manual validation tests executed - all passed
- 📁 Files: 2 files modified (TaskManager service, CLI main), 1 file updated (tasks.md)
- 🔁 Next prompts: User Story 4 (Task Deletion - P4), Polish phase (cross-cutting improvements)
- 🧠 Reflection: Clean implementation with flexible partial updates. Optional parameters in update_task provide elegant solution for "keep current" behavior. User experience enhanced with clear prompts and current value display.

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation completed smoothly
- Graders run and results (PASS/FAIL): All validation tests PASS
- Prompt variant (if applicable): Standard implementation workflow
- Next experiment (smallest change to try): Proceed to User Story 4 - implement delete_task method in TaskManager with confirmation workflow in CLI
