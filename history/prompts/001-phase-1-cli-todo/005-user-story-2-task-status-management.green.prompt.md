---
id: 005
title: User Story 2 Task Status Management Implementation
stage: green
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5
feature: 001-phase-1-cli-todo
branch: 001-phase-1-cli-todo
user: maryamkhanzada
command: implement
labels: ["implementation", "user-story-2", "status-management", "phase-4"]
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
  - Manual validation: get_task_by_id with valid ID
  - Manual validation: get_task_by_id with invalid ID returns None
  - Manual validation: toggle_task_completion marks task as completed
  - Manual validation: toggle_task_completion reverts task to pending
  - Manual validation: toggle_task_completion returns False for non-existent task
  - Manual validation: CLI operation with numeric input validation
  - Manual validation: CLI operation with invalid ID error handling
  - Manual validation: Status change confirmation messages
---

## Prompt

Implement User Story 2 (P2) - Task Status Management for the Todo CLI application.

**Context:**
- Feature: Phase I - In-Memory CLI Todo Application
- Scope: Phase 4 - User Story 2 (Priority P2)
- Tasks: T020-T024 (5 tasks)
- Goal: Enable users to mark tasks as completed or revert them to pending

**Requirements from spec:**
- User can toggle task completion status by ID
- Display appropriate confirmation message based on new state
- Validate task ID input (numeric, exists)
- Handle errors gracefully (invalid IDs, non-numeric input)
- Return to main menu after operation

**Acceptance Criteria:**
- User can mark a pending task as completed
- User can mark a completed task as pending
- Status changes are reflected in task list view
- Clear error messages for invalid input

## Response snapshot

Successfully completed all 5 tasks for User Story 2:

**TaskManager Service Updates (T020-T021):**

Added two new methods to `src/todo_app/services/task_manager.py`:

1. `get_task_by_id(task_id: int) -> Optional[Task]`
   - Finds and returns task by ID
   - Returns None if task not found
   - Used by other operations for task lookup

2. `toggle_task_completion(task_id: int) -> bool`
   - Toggles the completed boolean status
   - Returns True if successful, False if task not found
   - Uses get_task_by_id internally

**CLI Operation Implementation (T022-T024):**

Added `mark_complete_incomplete_operation()` to `src/todo_app/cli/main.py`:

- Prompts user for task ID
- Validates numeric input (catches ValueError for non-numeric)
- Checks if task exists before toggling
- Displays appropriate confirmation:
  - "Task marked as Completed!" when toggled to completed
  - "Task marked as Pending!" when toggled to pending
- Error handling for:
  - Non-numeric input: "Error: Task ID must be a number."
  - Invalid ID: "Error: Task with ID {id} not found."

Updated main() function to call the operation on menu choice "5"

**Validation Results:**
All tests passed:
- ✅ get_task_by_id returns correct task for valid ID
- ✅ get_task_by_id returns None for non-existent task
- ✅ toggle_task_completion changes status to Completed
- ✅ toggle_task_completion reverts status to Pending
- ✅ toggle_task_completion returns False for invalid ID
- ✅ Multiple tasks can be toggled independently
- ✅ CLI operation validates numeric input
- ✅ CLI operation handles invalid IDs gracefully

## Outcome

- ✅ Impact: User Story 2 fully implemented. Users can now mark tasks as completed/pending and see status changes in task list.
- 🧪 Tests: 8 manual validation tests executed - all passed
- 📁 Files: 2 files modified (TaskManager service, CLI main), 1 file updated (tasks.md)
- 🔁 Next prompts: User Story 3 (Task Modification - P3), User Story 4 (Task Deletion - P4)
- 🧠 Reflection: Implementation follows constitutional constraints. Clean separation between service layer (business logic) and CLI layer (presentation). Error handling comprehensive and user-friendly.

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation completed without issues
- Graders run and results (PASS/FAIL): All validation tests PASS
- Prompt variant (if applicable): Standard implementation workflow
- Next experiment (smallest change to try): Proceed to User Story 3 - implement update_task method in TaskManager and update operation in CLI
