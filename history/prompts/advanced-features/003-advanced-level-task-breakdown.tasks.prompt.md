---
id: 003
title: Advanced Level Task Breakdown
stage: tasks
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: advanced-features
branch: 002-advanced-features
user: system
command: /sp.tasks
labels: ["tasks", "planning", "advanced-level", "implementation-breakdown", "recurring-tasks", "reminders"]
links:
  spec: specs/002-advanced-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-advanced-features/tasks.md
tests:
  - N/A (planning phase)
---

## Prompt

Generate task breakdown for implementing the Advanced Level features based on the approved specification and implementation plan.

**Context**: Implementation plan complete with:
- 8 key technical decisions documented in research.md
- Data model extensions defined (due_time, recurrence, reminders, parent_recurrence_id)
- CLI contracts specified for all operations
- Architecture prioritizing simplicity and backward compatibility

**Requirements**:
- Create detailed, actionable task breakdown
- Organize tasks by user story for independent delivery
- Define clear dependencies and parallel execution opportunities
- Identify MVP scope for fastest time-to-value
- Ensure each task is testable and has clear acceptance criteria

## Response snapshot

Generated comprehensive task breakdown with 92 tasks organized into 7 phases for implementing Advanced Level intelligent task management features.

**Task Organization**:

**Phase 1: Setup (4 tasks)**
- T001-T004: Verify Basic/Intermediate levels fully working
- Purpose: Ensure foundation is solid before extending

**Phase 2: Foundational Infrastructure (7 tasks, BLOCKS all user stories)**
- T005-T011: Time utilities, validation, thread safety infrastructure
- Critical foundation: datetime helpers, time parsing/validation, threading.Lock setup
- No user stories can proceed without this phase

**Phase 3: User Story 1 - Time-Aware Due Dates (13 tasks, MVP)**
- T012-T024: Add due_time field, CLI prompts, display, sorting
- Deliverable: Tasks with precise due times (HH:MM format)
- Independent: Can be delivered alone as MVP

**Phase 4: User Story 2 - Recurring Tasks (19 tasks)**
- T025-T043: Recurrence data model, calculation logic, next occurrence generation
- Deliverable: Automatic task rescheduling on completion
- Dependencies: Requires Phase 2 and Phase 3 (due_time for accurate scheduling)

**Phase 5: User Story 3 - Reminders (23 tasks)**
- T044-T066: ReminderService, background thread, notification triggers
- Deliverable: Time-based console notifications
- Dependencies: Requires Phase 2 and Phase 3 (due_time for trigger calculation)

**Phase 6: User Story 4 - Manage Recurrence (11 tasks)**
- T067-T077: Recurrence management UI, history views, edit/stop operations
- Deliverable: Full lifecycle control over recurring tasks
- Dependencies: Requires Phase 4 (recurrence must exist to manage)

**Phase 7: Polish and Validation (15 tasks)**
- T078-T092: Backward compatibility testing, edge cases, error handling validation
- Deliverable: Production-ready, fully validated implementation
- Dependencies: Requires all previous phases

**Key Implementation Files**:
- `src/todo_app/models/task.py` - Add 4 new fields + 2 helper methods
- `src/todo_app/services/task_manager.py` - Add recurrence logic + thread safety
- `src/todo_app/services/reminder_service.py` - NEW: Background reminder thread
- `src/todo_app/cli/main.py` - Extended UI for time/recurrence/reminders
- `src/todo_app/utils/time_utils.py` - NEW: Time parsing and validation

**MVP Strategy** (Fastest path to value):
1. Complete Phase 1: Setup (T001-T004) - ~10 minutes
2. Complete Phase 2: Foundational (T005-T011) - ~30-45 minutes
3. Complete Phase 3: User Story 1 (T012-T024) - ~2-3 hours
4. **STOP and VALIDATE**: Test time-aware dates independently
5. Deploy/demo MVP if ready

**Total MVP time**: ~3-4 hours for basic time-aware task scheduling

**Full Feature Strategy**:
- Complete all 7 phases sequentially
- Each phase has clear acceptance criteria
- Parallel execution opportunities marked with [P]
- Total estimate: 10-14 hours

**Parallel Execution Opportunities**:
- Phase 3 (US1) + Phase 4 (US2) + Phase 5 (US3) can run in parallel after Phase 2 completes
- Phase 6 (US4) must wait for Phase 4 completion
- Phase 7 (Polish) must wait for all feature phases

**Task Format**:
```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

Examples:
- `[ ] T012 [US1] Add due_time field to Task.__init__() in src/todo_app/models/task.py`
- `[ ] T029 [US2] Implement _calculate_next_due_date(task) helper in src/todo_app/services/task_manager.py`
- `[ ] T047 [US3] Create src/todo_app/services/reminder_service.py file`

**Dependencies Clearly Defined**:
- Phase 2 blocks all user stories (foundational infrastructure)
- Phase 3 (US1) required for Phase 4 (US2) and Phase 5 (US3) - recurrence and reminders need precise due times
- Phase 4 (US2) required for Phase 6 (US4) - can't manage recurrence without recurrence
- Phase 7 depends on all phases (validation of complete system)

**Acceptance Criteria Per Task**:
Each task includes:
- File path to modify/create
- Specific changes required
- Validation method (manual test scenario or verification step)
- Clear done condition

## Outcome

- ✅ Impact: Complete task breakdown ready for execution with clear dependencies and MVP path
- 🧪 Tests: Manual test strategy defined for each task (no formal test framework per conventions)
- 📁 Files: tasks.md (92 tasks across 7 phases)
- 🔁 Next prompts: `/sp.implement` to begin implementation, starting with MVP (Phases 1-3) or full feature (all phases)
- 🧠 Reflection: Task organization prioritizes incremental delivery and independent testing. MVP path (Phases 1-3) delivers immediate value with time-aware due dates in ~3-4 hours. Clear blocking relationships prevent out-of-order execution. Phase 2 (foundational infrastructure) is critical path - all user stories depend on it. Parallel execution opportunities identified where appropriate (US1/US2/US3 can run concurrently after Phase 2). Each phase has well-defined acceptance criteria and file scope. Task granularity appropriate for systematic execution and progress tracking.

## Evaluation notes (flywheel)

- Failure modes observed: None - all tasks derived from approved plan and specification
- Graders run and results (PASS/FAIL): Task structure validation - PASS (all tasks have clear descriptions, file paths, and acceptance criteria)
- Prompt variant (if applicable): Standard task generation workflow (extract from plan.md → organize by user story → define dependencies)
- Next experiment (smallest change to try): Begin implementation with `/sp.implement`, starting with MVP approach (Phases 1-3 only) to validate time-aware due dates before proceeding with recurring tasks and reminders
