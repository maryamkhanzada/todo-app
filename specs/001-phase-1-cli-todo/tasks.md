---

description: "Task list for Phase I - In-Memory CLI Todo Application"
---

# Tasks: Phase I - In-Memory CLI Todo Application

**Input**: Design documents from `/specs/001-phase-1-cli-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/cli-interface.md, quickstart.md

**Tests**: Tests are NOT explicitly requested in the specification. Implementation will focus on functional requirements with manual testing per quickstart.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use absolute paths from repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize UV project with Python 3.13+ in project root (create pyproject.toml)
- [x] T002 Create .python-version file specifying Python 3.13
- [x] T003 [P] Create src/todo_app/__init__.py package initialization file
- [x] T004 [P] Create src/todo_app/models/__init__.py package file
- [x] T005 [P] Create src/todo_app/services/__init__.py package file
- [x] T006 [P] Create src/todo_app/cli/__init__.py package file
- [x] T007 Create README.md with setup and execution instructions per quickstart.md

**Checkpoint**: Project structure initialized - ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Implement Task entity in src/todo_app/models/task.py with fields (id: int, title: str, description: str, completed: bool)
- [x] T009 Implement TaskManager service skeleton in src/todo_app/services/task_manager.py with in-memory storage (list for tasks, counter for next_id)
- [x] T010 Implement main menu display in src/todo_app/cli/main.py with 6 options (Add, View, Update, Delete, Complete, Exit)
- [x] T011 Implement menu input handling and routing in src/todo_app/cli/main.py (dispatch to operation functions based on user choice 1-6)
- [x] T012 Implement invalid menu choice error handling in src/todo_app/cli/main.py (display error for invalid input, redisplay menu)
- [x] T013 Create src/__main__.py entry point that imports and runs main() from src/todo_app/cli/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Task Creation and Viewing (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks with titles and descriptions, and view all tasks in a clear format

**Independent Test**: Launch CLI, add multiple tasks with different titles/descriptions, view task list with all fields (ID, title, description, status) displayed correctly

### Implementation for User Story 1

- [x] T014 [P] [US1] Implement add_task method in src/todo_app/services/task_manager.py (create Task with auto-incremented ID, default completed=False, add to list)
- [x] T015 [P] [US1] Implement get_all_tasks method in src/todo_app/services/task_manager.py (return list of all tasks)
- [x] T016 [US1] Implement "Add Task" operation in src/todo_app/cli/main.py (prompt for title and description, call task_manager.add_task, display success with task ID)
- [x] T017 [US1] Implement "View Tasks" operation in src/todo_app/cli/main.py (call task_manager.get_all_tasks, display formatted list or "No tasks found" message)
- [x] T018 [US1] Implement task display formatting in src/todo_app/cli/main.py (show ID, Title, Description, Status with clear spacing per contracts/cli-interface.md)
- [x] T019 [US1] Implement status display conversion in src/todo_app/cli/main.py (convert completed boolean to "Pending"/"Completed" strings)

**Checkpoint**: At this point, User Story 1 (MVP) should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Status Management (Priority: P2)

**Goal**: Enable users to mark tasks as completed or revert them to pending

**Independent Test**: Create tasks, mark as completed, verify status changes in task list, revert to pending

### Implementation for User Story 2

- [x] T020 [P] [US2] Implement get_task_by_id method in src/todo_app/services/task_manager.py (find task by ID, return Task or None)
- [x] T021 [P] [US2] Implement toggle_task_completion method in src/todo_app/services/task_manager.py (find task by ID, toggle completed boolean, return success/failure)
- [x] T022 [US2] Implement "Mark Complete/Incomplete" operation in src/todo_app/cli/main.py (prompt for task ID, call task_manager.toggle_task_completion)
- [x] T023 [US2] Implement status change confirmation messages in src/todo_app/cli/main.py (display "Task marked as Completed!" or "Task marked as Pending!" based on new state)
- [x] T024 [US2] Implement task ID validation in src/todo_app/cli/main.py for status toggle (handle invalid IDs, non-numeric input, display error, return to menu)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Modification (Priority: P3)

**Goal**: Enable users to update task titles and descriptions

**Independent Test**: Create task, update title and/or description, verify changes reflected in task list

### Implementation for User Story 3

- [x] T025 [US3] Implement update_task method in src/todo_app/services/task_manager.py (find task by ID, update title/description if provided, return success/failure)
- [x] T026 [US3] Implement "Update Task" operation in src/todo_app/cli/main.py (prompt for task ID, validate ID exists, display current values)
- [x] T027 [US3] Implement update prompts in src/todo_app/cli/main.py (prompt for new title with "or press Enter to keep current", same for description)
- [x] T028 [US3] Implement update field handling in src/todo_app/cli/main.py (only update fields where user provided new values, keep current if Enter pressed)
- [x] T029 [US3] Implement update error handling in src/todo_app/cli/main.py (invalid IDs, non-numeric input, display errors, return to menu safely)

**Checkpoint**: All user stories 1, 2, AND 3 should now be independently functional

---

## Phase 6: User Story 4 - Task Deletion (Priority: P4)

**Goal**: Enable users to delete tasks with confirmation

**Independent Test**: Create tasks, delete specific tasks by ID, confirm deletion prompts work, verify deleted tasks removed from list

### Implementation for User Story 4

- [x] T030 [US4] Implement delete_task method in src/todo_app/services/task_manager.py (find task by ID, remove from list, return success/failure)
- [x] T031 [US4] Implement "Delete Task" operation in src/todo_app/cli/main.py (prompt for task ID, validate ID exists)
- [x] T032 [US4] Implement deletion confirmation prompt in src/todo_app/cli/main.py (display "Are you sure?" prompt, accept yes/y/no/n responses case-insensitive)
- [x] T033 [US4] Implement confirmation response handling in src/todo_app/cli/main.py (call delete_task if yes, display "Deletion cancelled" if no)
- [x] T034 [US4] Implement deletion error handling in src/todo_app/cli/main.py (invalid IDs, non-numeric input, handle gracefully without crash)
- [x] T035 [US4] Implement double-deletion handling in src/todo_app/cli/main.py (attempt to delete already-deleted task, display appropriate error)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final touches

- [x] T036 [P] Implement "Exit" operation in src/todo_app/cli/main.py (display goodbye message, terminate application cleanly)
- [x] T037 [P] Add input validation helpers in src/todo_app/cli/main.py (validate numeric input for task IDs, return error messages for non-numeric)
- [x] T038 [P] Verify all operations return to main menu per FR-010 (audit all operation functions)
- [x] T039 [P] Verify all error messages are clear and user-friendly per Constitution VIII (audit all error handling)
- [x] T040 Verify application startup time < 5 seconds per SC-006 (test startup performance)
- [x] T041 Verify task viewing < 1 second for 100 tasks per SC-002 (test with large task list)
- [x] T042 Verify all operations complete < 2 seconds per SC-007 (test operation performance)
- [x] T043 Test with empty task list (verify "No tasks found" message displays correctly)
- [x] T044 Test with very long title/description (verify graceful handling of 1000+ character strings)
- [x] T045 Test rapid consecutive operations (add 10 tasks quickly, verify all created correctly)
- [x] T046 Run through all examples in quickstart.md to validate end-to-end functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses get_task_by_id but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses get_task_by_id but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Uses get_task_by_id but should be independently testable

### Within Each User Story

- Tasks marked [P] can run in parallel (different files or independent methods)
- Tasks without [P] should run sequentially (same file or dependent logic)
- Each story should be completable independently
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T003-T006) marked [P] can run in parallel
- Within Foundational: T008, T009, T010 can run in parallel (different files)
- Within User Story 1: T014, T015 can run in parallel (independent methods)
- Within User Story 2: T020, T021 can run in parallel (independent methods)
- Most Polish tasks (T036-T039, T040-T042, T043-T045) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all parallel model tasks for User Story 1 together:
Task: "Implement add_task method in src/todo_app/services/task_manager.py"
Task: "Implement get_all_tasks method in src/todo_app/services/task_manager.py"

# Then sequential CLI tasks:
Task: "Implement 'Add Task' operation in src/todo_app/cli/main.py"
Task: "Implement 'View Tasks' operation in src/todo_app/cli/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T013) - CRITICAL blocking phase
3. Complete Phase 3: User Story 1 (T014-T019)
4. **STOP and VALIDATE**: Test User Story 1 independently using quickstart.md examples
5. Ready for demo/delivery (minimal viable product)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T014-T019) → Test independently → Demo/Deliver (MVP!)
3. Add User Story 2 (T020-T024) → Test independently → Demo/Deliver
4. Add User Story 3 (T025-T029) → Test independently → Demo/Deliver
5. Add User Story 4 (T030-T035) → Test independently → Demo/Deliver
6. Add Polish (T036-T046) → Final testing and validation
7. Each story adds value without breaking previous stories

### Sequential Development Strategy

If working alone or sequentially:

1. **Phase 1** (Setup): T001 → T002 → T003-T006 (parallel or sequential) → T007
2. **Phase 2** (Foundational): T008 → T009 → T010 → T011 → T012 → T013
3. **Phase 3** (US1): T014-T015 (parallel) → T016 → T017 → T018 → T019
4. **Validate MVP** before proceeding
5. **Phase 4** (US2): T020-T021 (parallel) → T022 → T023 → T024
6. **Phase 5** (US3): T025 → T026 → T027 → T028 → T029
7. **Phase 6** (US4): T030 → T031 → T032 → T033 → T034 → T035
8. **Phase 7** (Polish): T036-T046 (most can be parallel)

---

## Notes

- **[P] tasks** = different files or independent methods, no dependencies
- **[Story] label** maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **No tests explicitly requested** - validation via manual testing using quickstart.md
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 46

**Tasks by Phase**:
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 6 tasks (BLOCKING - must complete before user stories)
- Phase 3 (User Story 1 - P1): 6 tasks (MVP)
- Phase 4 (User Story 2 - P2): 5 tasks
- Phase 5 (User Story 3 - P3): 5 tasks
- Phase 6 (User Story 4 - P4): 6 tasks
- Phase 7 (Polish): 11 tasks

**Parallel Opportunities**: 19 tasks marked [P] can run in parallel with other tasks

**MVP Scope** (Recommended first delivery):
- Phase 1: Setup (7 tasks)
- Phase 2: Foundational (6 tasks)
- Phase 3: User Story 1 (6 tasks)
- **Total MVP**: 19 tasks

**Independent Test Criteria**:
- **US1**: Can add tasks and view them with all fields displayed correctly
- **US2**: Can toggle task completion status and see changes in task list
- **US3**: Can update task title/description and see changes reflected
- **US4**: Can delete tasks with confirmation and verify removal from list
