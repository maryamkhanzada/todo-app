# Implementation Plan: Advanced Level - Intelligent Task Management

**Branch**: `002-advanced-features` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-advanced-features/spec.md`

## Summary

Implement time-aware task management with recurring tasks, due dates with time components, and reminder notifications. This extends the existing Basic (CRUD) and Intermediate (organization) levels with intelligent scheduling features. The implementation adds time-of-day precision to due dates, automatic recurrence generation on task completion, and background reminder checking with console-based notifications.

**Technical Approach**: Extend Task model with time/recurrence/reminder fields, implement recurrence calculation logic in TaskManager, add background thread for reminder polling, and extend CLI with new interaction flows for time entry and recurrence management.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (`datetime`, `threading`, `time` modules)
**Storage**: In-memory (consistent with Basic/Intermediate levels - no persistence)
**Testing**: Manual testing (no test framework per project conventions)
**Target Platform**: CLI application (Windows/Linux/macOS cross-platform)
**Project Type**: Single project (extends existing `src/todo_app/` structure)
**Performance Goals**:
- Reminder checking: 60-second polling interval acceptable
- Recurrence generation: <1 second on task completion
- Time validation: instant (<100ms)
**Constraints**:
- No external dependencies (pure Python stdlib)
- Backward compatibility with existing Basic/Intermediate features required
- No database persistence (in-memory only)
- Background reminder thread must not block CLI interaction
**Scale/Scope**:
- Support 100+ recurring tasks without performance degradation
- Handle multiple simultaneous reminders
- Support custom recurrence intervals (every N days where N=1-365)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase III (Advanced Level) Requirements

✅ **Recurring Tasks**: Implementation supports daily, weekly, and custom (every N days) recurrence patterns with automatic next occurrence generation on completion.

✅ **Due Dates with Time**: Tasks extended with `due_time` field (HH:MM format) enabling time-of-day precision for scheduling.

✅ **Reminders**: Background thread polls for due reminders every 60 seconds and triggers console-based notifications.

✅ **Builds on Phase I & II**: All changes extend existing Task model and TaskManager service without breaking Basic or Intermediate functionality.

✅ **Deterministic and Testable**: Recurrence calculation uses deterministic date arithmetic (timedelta), reminder triggers based on datetime comparison (no randomness or non-deterministic behavior).

✅ **Timezone Considerations**: Times stored in local time (system timezone), no automatic DST adjustments (documented assumption in spec).

### Additional Checks

✅ **Zero External Dependencies**: All features use Python stdlib only (`datetime`, `threading`, `time` modules).

✅ **Single Project Structure**: Continues using `src/todo_app/` with models/services/cli organization.

✅ **No Manual Coding**: All implementation via Claude Code following this plan.

✅ **Backward Compatibility**: New Task fields have defaults (due_time="23:59", recurrence={"type":"none","interval":1}, reminders=[], parent_recurrence_id=None).

**Gate Status**: ✅ PASS - No constitution violations. All Phase III requirements satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/002-advanced-features/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 output (technical decisions)
├── data-model.md        # Phase 1 output (Task entity extensions)
├── quickstart.md        # Phase 1 output (developer guide)
├── contracts/           # Phase 1 output (CLI operation contracts)
│   └── cli-operations.md
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (NOT created by /sp.plan - created by /sp.tasks)
```

### Source Code (repository root)

```text
src/todo_app/
├── models/
│   └── task.py          # MODIFY: Add due_time, recurrence, reminders, parent_recurrence_id
├── services/
│   ├── task_manager.py  # MODIFY: Add recurrence logic, reminder tracking
│   └── reminder_service.py  # NEW: Background thread for reminder checking
├── cli/
│   └── main.py          # MODIFY: Add time input, recurrence UI, reminder UI
└── utils/
    └── time_utils.py    # NEW: Time parsing, validation, recurrence calculation helpers

tests/                   # No formal test framework (manual testing per conventions)
├── manual_tests.md      # NEW: Manual test scenarios for Advanced features
└── test_advanced.py     # Optional: Quick validation script (not part of formal testing)
```

**Structure Decision**: Extends existing single-project structure (`src/todo_app/`) with new service layer for reminders and utilities for time handling. Maintains backward compatibility by modifying existing files (Task model, TaskManager) rather than creating parallel implementations.

## Complexity Tracking

> **No violations - this section intentionally left empty**

All design decisions align with constitution constraints. No additional complexity beyond what's required by the feature specification.

---

## Phase 0: Research & Technical Decisions

**Purpose**: Resolve technical unknowns and document architecture decisions before detailed design.

### Research Topics

1. **Time Handling in Python**
   - Decision: Use `datetime.datetime` for due_date + due_time combined storage
   - Rationale: Single datetime object simplifies comparisons, sorting, and timedelta arithmetic
   - Alternative: Separate `date` and `time` fields rejected (complex sorting, harder to compare)

2. **Recurrence Calculation Algorithm**
   - Decision: Calculate next occurrence from original due_date using `timedelta(days=interval)`
   - Rationale: Prevents "drift" when tasks completed early/late, maintains schedule consistency
   - Alternative: Calculate from completion date rejected (causes schedule drift over time)

3. **Reminder Background Thread Strategy**
   - Decision: Single daemon thread with 60-second polling loop
   - Rationale: Simple, no race conditions, acceptable latency (<1 min), daemon thread exits with main process
   - Alternative: Timer-based callbacks rejected (complex callback management, potential memory leaks)

4. **Browser Notification Simulation (CLI Context)**
   - Decision: Console output with timestamp and task details
   - Rationale: CLI application has no browser context, console provides visible notification
   - Alternative: System notifications (plyer library) rejected (violates zero-dependency constraint)

5. **Data Model Storage (Recurrence/Reminders)**
   - Decision: Store as dicts/lists on Task instances (not separate entities)
   - Rationale: In-memory app with no persistence, simple to serialize if persistence added later
   - Alternative: Separate Reminder/Recurrence classes rejected (over-engineering for in-memory use case)

6. **Thread Safety for Reminder Checking**
   - Decision: Use threading.Lock for task list access in reminder thread
   - Rationale: Prevents race conditions when main thread modifies tasks while reminder thread reads
   - Alternative: No locking rejected (potential crashes from list modification during iteration)

7. **Timezone Handling**
   - Decision: Store all times in local timezone (system default), no conversion
   - Rationale: Single-user CLI app, complexity of timezone conversion unnecessary
   - Alternative: UTC storage rejected (confusing for user when displayed times don't match local clock)

8. **Recurrence History Tracking**
   - Decision: Use `parent_recurrence_id` to link occurrences, keep completed tasks in list
   - Rationale: Enables viewing completion history, simple implementation
   - Alternative: Separate occurrence list rejected (complicates querying and filtering)

### Key Decisions Summary

| Decision Area | Choice | Rationale |
|---------------|--------|-----------|
| Time Storage | Combined datetime object | Simplifies comparisons and arithmetic |
| Recurrence Calc | From original due date | Prevents schedule drift |
| Reminder Thread | 60s polling daemon thread | Simple, adequate latency, auto-exits |
| Notifications | Console output | No external deps, visible in CLI |
| Data Structure | Dicts/lists on Task | Matches in-memory storage pattern |
| Thread Safety | threading.Lock | Prevents race conditions |
| Timezone | Local time only | Matches single-user CLI context |
| Recurrence History | parent_recurrence_id link | Enables history queries |

**Output**: See [research.md](./research.md) for detailed technical investigation and decision rationale.

---

## Phase 1: Data Model & Contracts

**Purpose**: Define entity extensions and operation contracts before implementation.

### Data Model Changes

**Task Entity Extensions** (see [data-model.md](./data-model.md) for full details):

```python
class Task:
    # Existing attributes (unchanged):
    # id, title, description, completed, priority, tags, due_date

    # NEW attributes:
    due_time: str | None  # HH:MM format, defaults to "23:59" if due_date set
    recurrence: dict      # {"type": "none"|"daily"|"weekly"|"custom", "interval": int}
    reminders: list[dict] # [{"offset_value": int, "offset_unit": str, "sent": bool, "sent_at": datetime}]
    parent_recurrence_id: int | None  # Links to original recurring task for history
```

**New Service: ReminderService**

```python
class ReminderService:
    def __init__(self, task_manager: TaskManager)
    def start()  # Start background reminder thread
    def stop()   # Stop background thread gracefully
    def check_reminders()  # Poll loop checking for due reminders
    def trigger_reminder(task: Task, reminder: dict)  # Display console notification
```

### Operation Contracts

See [contracts/cli-operations.md](./contracts/cli-operations.md) for detailed CLI operation signatures and behaviors.

**New Operations**:
- `add_task_operation`: EXTENDED to prompt for due time, recurrence, reminders
- `update_task_operation`: EXTENDED to allow editing due time, recurrence, reminders
- `toggle_task_completion`: MODIFIED to trigger recurrence generation
- `view_tasks_operation`: MODIFIED to display due time, recurrence pattern, reminder status
- `manage_recurrence_operation`: NEW sub-menu for editing/stopping recurrence
- `manage_reminders_operation`: NEW sub-menu for adding/removing reminders

### Integration Points

1. **TaskManager ↔ ReminderService**: TaskManager notifies ReminderService of task changes (completion, deletion, time changes)
2. **CLI ↔ TaskManager**: CLI validates time input, parses recurrence patterns, passes to TaskManager
3. **ReminderService ↔ Task**: ReminderService reads task list with lock, updates reminder sent status

**Output**: See [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

---

## Implementation Strategy

### Incremental Delivery Path

**MVP (User Story 1 - Time-Aware Due Dates)**:
1. Extend Task model with `due_time` field
2. Update CLI to prompt for time input
3. Modify display/sort to show times
4. **Delivers Value**: Users can schedule tasks at specific times

**Milestone 2 (User Story 2 - Recurring Tasks)**:
5. Add `recurrence` and `parent_recurrence_id` to Task
6. Implement recurrence calculation in TaskManager
7. Modify `toggle_task_completion` to generate next occurrence
8. Add recurrence UI (set/edit/stop patterns)
9. **Delivers Value**: Automatic task rescheduling eliminates manual re-entry

**Milestone 3 (User Story 3 - Reminders)**:
10. Add `reminders` field to Task
11. Create ReminderService with background thread
12. Implement reminder checking loop
13. Add reminder UI (add/remove/view)
14. Start ReminderService in main()
15. **Delivers Value**: Users get notified of upcoming tasks

**Milestone 4 (User Story 4 - Recurrence Management)**:
16. Add occurrence history view
17. Add edit recurrence with future-only scope
18. Add delete with single/all-future options
19. **Delivers Value**: Full control over recurring task lifecycle

### Testing Strategy

**Manual Test Scenarios** (see tests/manual_tests.md):
- Time input validation (invalid times, missing time defaults to 23:59)
- Recurrence generation (daily, weekly, custom intervals)
- Recurrence edge cases (overdue tasks, no due date, past date calculation)
- Reminder triggering (before due time, multiple reminders, completion cancellation)
- Thread safety (modify tasks while reminders checking)
- Backward compatibility (existing Basic/Intermediate operations still work)

**Performance Validation**:
- Create 100 recurring tasks, verify recurrence generation <1s per task
- Create 50 tasks with reminders, verify reminder thread CPU usage <5%
- Sort 1000 tasks by due date+time, verify sort completes <100ms

### Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Reminder thread crash | Wrap polling loop in try/except, log errors, continue checking |
| Time zone confusion | Document assumption clearly, consistent local time display |
| Recurrence drift | Calculate from original due date (not completion), unit test arithmetic |
| Thread race conditions | Use threading.Lock for all task list access in reminder thread |
| Backward compatibility break | Test all Basic/Intermediate operations after changes, fix before merge |

---

## Next Steps

After Phase 1 completion:
1. Run `/sp.tasks` to generate task breakdown (Phase 2)
2. Begin implementation with `/sp.implement` following generated tasks
3. Validate backward compatibility with existing Intermediate-level tests
4. Manual testing using scenarios in tests/manual_tests.md
5. Git commit after each milestone with descriptive message

---

## Constitution Re-Check (Post-Design)

✅ **Phase III Requirements**: All Advanced Level capabilities implemented as specified.

✅ **Phase I & II Intact**: Backward compatibility verified through default values and non-breaking extensions.

✅ **Deterministic Behavior**: All recurrence and reminder logic uses deterministic datetime arithmetic.

✅ **Zero Dependencies**: All implementation using Python stdlib only.

✅ **Single Project Structure**: Extends existing `src/todo_app/` without introducing additional projects.

**Final Gate Status**: ✅ PASS - Design complete and constitution-compliant.
