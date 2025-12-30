---
description: "Task breakdown for Advanced Level - Intelligent Task Management implementation"
---

# Tasks: Advanced Level - Intelligent Task Management

**Input**: Design documents from `/specs/002-advanced-features/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Not requested in specification - no test tasks included (manual testing per project conventions)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Each user story is a complete, deliverable increment.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/todo_app/` at repository root
- All changes extend existing modules: models/task.py, services/task_manager.py, cli/main.py
- New files: services/reminder_service.py, utils/time_utils.py

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify existing Basic and Intermediate Level foundation is ready for Advanced Level changes

- [X] T001 Verify Basic Level implementation complete and working (run application, test CRUD operations)
- [X] T002 Verify Intermediate Level implementation complete (test priority, tags, search, filter, sort)
- [X] T003 Verify Python 3.13+ environment and standard library modules available (datetime, threading, time)
- [X] T004 Review existing codebase structure in src/todo_app/ (models, services, cli)

**Checkpoint**: Basic and Intermediate Levels confirmed working - ready for Advanced Level enhancements

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create shared utilities and infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Create src/todo_app/utils/ directory for utility modules
- [X] T006 [P] Create src/todo_app/utils/time_utils.py with time parsing/validation functions
- [X] T007 [P] Implement parse_time(time_str) function in src/todo_app/utils/time_utils.py
- [X] T008 [P] Implement validate_time(time_str) function with regex validation in src/todo_app/utils/time_utils.py
- [X] T009 [P] Implement parse_reminder(reminder_str) function in src/todo_app/utils/time_utils.py
- [X] T010 [P] Add datetime, threading imports to src/todo_app/services/task_manager.py
- [X] T011 Add threading.Lock to TaskManager.__init__() in src/todo_app/services/task_manager.py

**Checkpoint**: Foundation ready - utilities and thread safety in place, all user stories can now build on this

---

## Phase 3: User Story 1 - Time-Aware Due Dates (Priority: P1) 🎯 MVP

**Goal**: Enable users to specify exact due dates with times (not just dates) for tasks

**Independent Test**: Create tasks with various date+time combinations (e.g., "2026-01-15 14:30"), verify tasks display the time component, verify tasks can be filtered/sorted by date+time, verify time is preserved when updating tasks.

### Implementation for User Story 1

- [X] T012 [US1] Add due_time field to Task.__init__() in src/todo_app/models/task.py (str | None, defaults to "23:59" if due_date set)
- [X] T013 [US1] Implement Task.get_due_datetime() method in src/todo_app/models/task.py (combines date + time)
- [X] T014 [US1] Update Task.__repr__() to include due_time in src/todo_app/models/task.py
- [X] T015 [US1] Add due_time validation in Task.__init__() using time_utils.validate_time() in src/todo_app/models/task.py
- [X] T016 [US1] Update TaskManager.add_task() signature to accept due_time parameter in src/todo_app/services/task_manager.py
- [X] T017 [US1] Update TaskManager.update_task() signature to accept due_time parameter in src/todo_app/services/task_manager.py
- [X] T018 [US1] Update TaskManager.sort_tasks('due_date') to use get_due_datetime() in src/todo_app/services/task_manager.py
- [X] T019 [US1] Update CLI add_task_operation() to prompt for due time in src/todo_app/cli/main.py
- [X] T020 [US1] Add time input validation and error handling in add_task_operation() in src/todo_app/cli/main.py
- [X] T021 [US1] Update CLI update_task_operation() to prompt for due time changes in src/todo_app/cli/main.py
- [X] T022 [US1] Add time input validation in update_task_operation() in src/todo_app/cli/main.py
- [X] T023 [US1] Update CLI view_tasks_operation() to display due_time for each task in src/todo_app/cli/main.py
- [X] T024 [US1] Format due_time display as "YYYY-MM-DD HH:MM" in view_tasks in src/todo_app/cli/main.py

**Checkpoint**: At this point, User Story 1 (Time-Aware Due Dates) is fully functional and testable independently. Users can set precise times when adding tasks, change times when updating tasks, and see times in the task list. This is a viable MVP.

---

## Phase 4: User Story 2 - Recurring Tasks with Automatic Rescheduling (Priority: P2)

**Goal**: Enable users to mark tasks as recurring with automatic next occurrence generation on completion

**Independent Test**: Create recurring tasks with different patterns (daily, weekly, custom), mark them complete, verify next occurrence is automatically generated with correct due date/time, verify recurrence can be edited or stopped.

### Implementation for User Story 2

- [X] T025 [US2] Add recurrence field to Task.__init__() in src/todo_app/models/task.py (dict with type/interval, defaults to {"type":"none","interval":1})
- [X] T026 [US2] Add parent_recurrence_id field to Task.__init__() in src/todo_app/models/task.py (int | None, defaults to None)
- [X] T027 [US2] Add recurrence validation in Task.__init__() in src/todo_app/models/task.py (type must be none/daily/weekly/custom)
- [X] T028 [US2] Update Task.__repr__() to include recurrence pattern in src/todo_app/models/task.py
- [X] T029 [US2] Implement _calculate_next_due_date(task) helper in src/todo_app/services/task_manager.py
- [X] T030 [US2] Implement _get_recurrence_interval(recurrence) helper in src/todo_app/services/task_manager.py
- [X] T031 [US2] Implement create_next_occurrence(completed_task) in src/todo_app/services/task_manager.py
- [X] T032 [US2] Modify TaskManager.toggle_task_completion() to generate next occurrence if recurring in src/todo_app/services/task_manager.py
- [X] T033 [US2] Update TaskManager.add_task() signature to accept recurrence parameter in src/todo_app/services/task_manager.py
- [X] T034 [US2] Update TaskManager.update_task() signature to accept recurrence parameter in src/todo_app/services/task_manager.py
- [X] T035 [US2] Implement get_occurrence_history(task) method in src/todo_app/services/task_manager.py
- [X] T036 [US2] Update CLI add_task_operation() to prompt for recurrence pattern in src/todo_app/cli/main.py
- [X] T037 [US2] Add recurrence input validation (daily/weekly/custom) in add_task_operation() in src/todo_app/cli/main.py
- [X] T038 [US2] Add custom interval input (1-365 days) in add_task_operation() in src/todo_app/cli/main.py
- [X] T039 [US2] Update CLI view_tasks_operation() to display recurrence pattern for each task in src/todo_app/cli/main.py
- [X] T040 [US2] Format recurrence display (e.g., "Repeats: Every 7 days") in view_tasks in src/todo_app/cli/main.py
- [X] T041 [US2] Update CLI toggle_task_completion() to display next occurrence info in src/todo_app/cli/main.py
- [X] T042 [US2] Update CLI delete_task_operation() to prompt for recurrence scope (single/all future) in src/todo_app/cli/main.py
- [X] T043 [US2] Implement delete scope logic (single occurrence vs all future) in delete_task_operation() in src/todo_app/cli/main.py

**Checkpoint**: At this point, User Story 2 (Recurring Tasks) is fully functional and testable independently. Users can set recurrence when adding tasks, mark recurring tasks complete to generate next occurrence, and manage recurring task deletion.

---

## Phase 5: User Story 3 - Time-Based Reminders with Notifications (Priority: P3)

**Goal**: Enable users to set reminders for tasks and receive console notifications at specified times

**Independent Test**: Create tasks with reminders at various times (15 min before, 1 hour before, 1 day before), verify reminders trigger at correct time, verify console notifications appear, verify reminders can be added/removed/modified.

### Implementation for User Story 3

- [X] T044 [US3] Add reminders field to Task.__init__() in src/todo_app/models/task.py (list of dicts, defaults to [])
- [X] T045 [US3] Implement Task.get_reminder_trigger_time(reminder) method in src/todo_app/models/task.py
- [X] T046 [US3] Update Task.__repr__() to include reminders count in src/todo_app/models/task.py
- [X] T047 [US3] Create src/todo_app/services/reminder_service.py file
- [X] T048 [US3] Implement ReminderService.__init__(task_manager) in src/todo_app/services/reminder_service.py
- [X] T049 [US3] Implement ReminderService.start() method (start daemon thread) in src/todo_app/services/reminder_service.py
- [X] T050 [US3] Implement ReminderService.stop() method (graceful shutdown) in src/todo_app/services/reminder_service.py
- [X] T051 [US3] Implement ReminderService._check_loop() method (60s polling) in src/todo_app/services/reminder_service.py
- [X] T052 [US3] Implement ReminderService._check_all_reminders() method (thread-safe) in src/todo_app/services/reminder_service.py
- [X] T053 [US3] Implement ReminderService._trigger_reminder(task, reminder) method (console output) in src/todo_app/services/reminder_service.py
- [X] T054 [US3] Update create_next_occurrence() to copy reminders with sent=False in src/todo_app/services/task_manager.py
- [X] T055 [US3] Update TaskManager.toggle_task_completion() to cancel reminders on completion in src/todo_app/services/task_manager.py
- [X] T056 [US3] Update CLI main() to create ReminderService instance in src/todo_app/cli/main.py
- [X] T057 [US3] Update CLI main() to start ReminderService after TaskManager initialization in src/todo_app/cli/main.py
- [X] T058 [US3] Update CLI main() to stop ReminderService on exit (Ctrl+C, menu exit) in src/todo_app/cli/main.py
- [X] T059 [US3] Create manage_reminders_operation() function with sub-menu in src/todo_app/cli/main.py
- [X] T060 [US3] Implement "Add Reminder" option in manage_reminders_operation() in src/todo_app/cli/main.py
- [X] T061 [US3] Implement "Remove Reminder" option in manage_reminders_operation() in src/todo_app/cli/main.py
- [X] T062 [US3] Implement "View Reminders" option in manage_reminders_operation() in src/todo_app/cli/main.py
- [X] T063 [US3] Add menu option 10 "Manage Reminders" to main menu in src/todo_app/cli/main.py
- [X] T064 [US3] Wire menu choice 10 to manage_reminders_operation() in main() in src/todo_app/cli/main.py
- [X] T065 [US3] Update view_tasks_operation() to display reminder status for each task in src/todo_app/cli/main.py
- [X] T066 [US3] Format reminder display (e.g., "15 minutes before (pending)") in view_tasks in src/todo_app/cli/main.py

**Checkpoint**: At this point, User Story 3 (Reminders) is fully functional and testable independently. Users can add reminders when creating or managing tasks, reminders trigger at correct times with console notifications, and reminders are managed independently.

---

## Phase 6: User Story 4 - Manage Recurring Patterns (Priority: P4)

**Goal**: Enable users to view, edit, and stop recurrence patterns with occurrence history

**Independent Test**: Create recurring task, complete it multiple times to generate history, edit recurrence pattern, verify future occurrences use new pattern, verify past occurrences unchanged, delete recurrence entirely.

### Implementation for User Story 4

- [X] T067 [US4] Create manage_recurrence_operation() function with sub-menu in src/todo_app/cli/main.py
- [X] T068 [US4] Implement "Set/Edit Recurrence Pattern" option in manage_recurrence_operation() in src/todo_app/cli/main.py
- [X] T069 [US4] Implement "Stop Recurrence" option in manage_recurrence_operation() in src/todo_app/cli/main.py
- [X] T070 [US4] Implement "View Occurrence History" option in manage_recurrence_operation() in src/todo_app/cli/main.py
- [X] T071 [US4] Add confirmation prompt for editing recurrence (future-only warning) in manage_recurrence_operation() in src/todo_app/cli/main.py
- [X] T072 [US4] Add confirmation prompt for stopping recurrence in manage_recurrence_operation() in src/todo_app/cli/main.py
- [X] T073 [US4] Add menu option 11 "Manage Recurrence" to main menu in src/todo_app/cli/main.py
- [X] T074 [US4] Wire menu choice 11 to manage_recurrence_operation() in main() in src/todo_app/cli/main.py
- [X] T075 [US4] Update view_tasks_operation() to display occurrence history for recurring tasks in src/todo_app/cli/main.py
- [X] T076 [US4] Format occurrence history display (last 5 completions with dates) in view_tasks in src/todo_app/cli/main.py
- [X] T077 [US4] Update CLI update_task_operation() to support editing recurrence with confirmation in src/todo_app/cli/main.py

**Checkpoint**: At this point, User Story 4 (Manage Recurring Patterns) is fully functional and testable independently. All Advanced Level features are now complete.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements, validation, and backward compatibility testing

- [X] T078 Update main menu to renumber Exit option to accommodate new menu items in src/todo_app/cli/main.py
- [X] T079 Test all Basic Level operations still work (Add, View, Update, Delete, Complete)
- [X] T080 Test all Intermediate Level operations still work (Priority, Tags, Search, Filter, Sort)
- [X] T081 Verify backward compatibility: existing tasks display with default time=23:59, recurrence=none, reminders=[]
- [X] T082 Test time input edge cases: invalid times (25:00, 13:75), missing time defaults to 23:59
- [X] T083 Test recurrence edge cases: overdue tasks skip to future, no due date calculates from completion
- [X] T084 Test reminder edge cases: past reminders warn user, completed tasks cancel reminders
- [X] T085 Test combined operations: recurring task with reminders, filtering recurring tasks, sorting by time
- [X] T086 Performance test with 100+ recurring tasks: verify recurrence generation <1s per task
- [X] T087 Performance test reminder thread: verify CPU usage <5% with 50 tasks with reminders
- [X] T088 Test thread safety: modify tasks while reminder thread checking (no crashes, no race conditions)
- [X] T089 Create tests/manual_tests.md with comprehensive manual test scenarios
- [X] T090 Review all error messages for clarity and helpfulness across all operations
- [X] T091 Final manual walkthrough of all 4 user stories to verify independent delivery
- [X] T092 Verify constitution compliance: zero dependencies, single project, backward compatible

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed) or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Time-Aware Dates)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2 - Recurring Tasks)**: Can start after Foundational (Phase 2) - Depends on US1 for due_time field
- **User Story 3 (P3 - Reminders)**: Can start after Foundational (Phase 2) - Depends on US1 for due_time, optionally uses US2 recurrence
- **User Story 4 (P4 - Manage Recurrence)**: Depends on US2 completion (extends recurrence management)

**Note**: While US2, US3, US4 have logical dependencies on US1, they modify different sections of code and can be developed in parallel with coordination.

### Within Each User Story

- All tasks within a user story modify the same files (task.py, task_manager.py, main.py)
- Tasks should be completed sequentially within each user story
- Model layer tasks (Task extensions) should complete before service layer tasks (TaskManager methods)
- Service layer tasks should complete before CLI tasks (UI interactions)

### Parallel Opportunities

**Between User Stories** (if team capacity allows):
- After Phase 2 completes, US1 can start immediately
- US2 can start in parallel with US1 after US1 completes T012-T015 (Task model changes)
- US3 can start in parallel with US2 after US1 completes T012-T015
- US4 must wait for US2 completion (extends US2 functionality)

**Within Foundational Phase**:
- T005-T009 (time_utils.py) can be done in parallel (same file but independent functions)
- T010-T011 (TaskManager thread safety) must be sequential

**Within User Stories**:
- Limited parallelization due to same-file modifications
- Model changes can be done in parallel with utility function development
- Display formatting (view updates) can be written in parallel with handler logic preparation

---

## Parallel Example: After Foundational Phase

```bash
# If you have 4 developers, launch user stories with dependencies:

Developer A: Phase 3 (US1 - Time-Aware Dates)     - T012 to T024 (foundation for others)
  → Once T012-T015 complete (Task model done):

Developer B: Phase 4 (US2 - Recurring Tasks)      - T025 to T043 (can start after US1 model)
Developer C: Phase 5 (US3 - Reminders)            - T044 to T066 (can start after US1 model)
  → Once Phase 4 complete:

Developer D: Phase 6 (US4 - Manage Recurrence)    - T067 to T077 (extends US2)

# Merge all changes together at the end
# Run Phase 7 (Polish) to test integration
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

**Fastest path to working Advanced Level features:**

1. Complete Phase 1: Setup (T001-T004) - ~10 minutes
2. Complete Phase 2: Foundational (T005-T011) - ~30-45 minutes
3. Complete Phase 3: User Story 1 (T012-T024) - ~2-3 hours
4. **STOP and VALIDATE**: Test time-aware dates independently
5. Deploy/demo if ready

**Total MVP time**: ~3-4 hours for basic time-aware task scheduling

### Incremental Delivery

**Recommended approach for staged rollout:**

1. **Sprint 1**: Setup + Foundational + US1 (Time-Aware Dates) → Deploy MVP
2. **Sprint 2**: Add US2 (Recurring Tasks) → Deploy with automatic rescheduling
3. **Sprint 3**: Add US3 (Reminders) → Deploy with notification capability
4. **Sprint 4**: Add US4 (Manage Recurrence) → Deploy full Advanced Level
5. **Sprint 5**: Polish (Phase 7) → Final validation and optimization

Each sprint adds value without breaking previous features.

### Parallel Team Strategy

**If you have multiple developers available:**

1. Team completes Setup + Foundational together (T001-T011)
2. Once Foundational is done:
   - Developer A: User Story 1 (T012-T024)
   - After T012-T015 complete:
     - Developer B: User Story 2 (T025-T043)
     - Developer C: User Story 3 (T044-T066)
   - After User Story 2 complete:
     - Developer D: User Story 4 (T067-T077)
3. Merge all changes
4. Team completes Polish together (T078-T092)

**Timeline**: Can complete all Advanced Level features in 2-3 days with parallel development.

---

## Notes

- **[P] tasks**: Different files or isolated sections, no dependencies - CAN run in parallel
- **[Story] label**: Maps task to specific user story for traceability and independent testing
- **File paths**: All tasks include exact file paths for clarity
- **Tests**: Not included because specification does not request testing framework (manual testing per conventions)
- **Backward compatibility**: Phase 2 ensures thread safety, US1 ensures all new fields have defaults
- Each user story is independently completable and testable
- Commit after each user story phase for clean incremental history
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same-method conflicts, cross-story dependencies that break independence

---

## Validation Checklist

Before marking implementation complete, verify:

- [ ] All 92 tasks completed
- [ ] All 4 user stories independently testable
- [ ] All Basic Level operations still work (backward compatibility)
- [ ] All Intermediate Level operations still work (backward compatibility)
- [ ] Time validation rejects invalid times (25:00, 13:75)
- [ ] Recurrence calculates from original due date (prevents drift)
- [ ] Reminders trigger within 60 seconds of due time
- [ ] Reminder thread runs without crashes or race conditions
- [ ] Performance: recurrence generation <1s, reminder checking <5% CPU
- [ ] Error messages are clear and helpful
- [ ] Menu options work correctly with new Manage Reminders and Manage Recurrence sub-menus
- [ ] Exit option renumbered appropriately

---

## Task Count Summary

- **Phase 1 (Setup)**: 4 tasks
- **Phase 2 (Foundational)**: 7 tasks
- **Phase 3 (US1 - Time-Aware Dates)**: 13 tasks
- **Phase 4 (US2 - Recurring Tasks)**: 19 tasks
- **Phase 5 (US3 - Reminders)**: 23 tasks
- **Phase 6 (US4 - Manage Recurrence)**: 11 tasks
- **Phase 7 (Polish)**: 15 tasks

**Total**: 92 tasks across 7 phases

**MVP Scope** (Phase 1 + 2 + 3): 24 tasks (~3-4 hours)
**Full Advanced Level**: 92 tasks (~10-14 hours)
