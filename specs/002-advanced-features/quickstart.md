# Quickstart Guide: Advanced Level Implementation

**Feature**: Advanced Level - Intelligent Task Management
**Date**: 2025-12-30
**Audience**: Developers implementing Advanced Level features

## Overview

This guide provides a quickstart path for implementing time-aware task management with recurring tasks, precise due times, and reminder notifications. Follow this guide to understand the architecture, file changes, and implementation order.

---

## Prerequisites

Before starting implementation, ensure:

1. **Basic Level (Phase I) Complete**:
   - CRUD operations working (`add`, `view`, `update`, `delete`, `complete` tasks)
   - Task model with id, title, description, completed fields
   - TaskManager service with in-memory storage

2. **Intermediate Level (Phase II) Complete**:
   - Priority, tags, due_date fields on Task
   - Search, filter, sort operations working
   - CLI with 9 menu options (including placeholder for Advanced features)

3. **Python Environment**:
   - Python 3.13+ installed
   - No external dependencies required (stdlib only)

4. **Development Context**:
   - Working directory: `D:\todo\todo-app\`
   - Source code: `src/todo_app/`
   - Spec files: `specs/002-advanced-features/`

---

## Architecture Overview

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Layer                             │
│  (main.py - User interaction, input validation, display)    │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
      ┌────────────────┐            ┌─────────────────┐
      │  TaskManager   │◄───────────│ ReminderService │
      │   (Business    │            │   (Background   │
      │    Logic)      │            │     Thread)     │
      └────────┬───────┘            └─────────────────┘
               │
               ▼
        ┌──────────────┐
        │   Task Model │
        │  (Enhanced)  │
        └──────────────┘
```

**Key Relationships**:
- CLI → TaskManager: Creates/updates/deletes tasks
- TaskManager → Task: Manages task collection
- ReminderService → TaskManager: Reads task list (thread-safe)
- ReminderService → CLI: Outputs console notifications
- TaskManager ↔ ReminderService: Shared lock for thread safety

---

## File Changes Summary

### Files to MODIFY

1. **`src/todo_app/models/task.py`**
   - Add: `due_time`, `recurrence`, `reminders`, `parent_recurrence_id` fields
   - Add: `get_due_datetime()` helper method
   - Add: `get_reminder_trigger_time()` helper method
   - Lines changed: ~50-80 additions

2. **`src/todo_app/services/task_manager.py`**
   - Add: `threading.Lock` for thread-safe access
   - Add: Recurrence generation logic in `toggle_task_completion()`
   - Modify: `add_task()` signature to accept time/recurrence/reminders
   - Modify: `update_task()` signature for time/recurrence/reminders
   - Lines changed: ~100-150 additions

3. **`src/todo_app/cli/main.py`**
   - Extend: `add_task_operation()` with time/recurrence/reminder prompts
   - Extend: `update_task_operation()` with new field editing
   - Extend: `view_tasks_operation()` to display time/recurrence/reminders
   - Modify: `delete_task_operation()` with recurrence scope prompt
   - Modify: `main()` to start/stop ReminderService
   - Lines changed: ~200-300 additions

### Files to CREATE

4. **`src/todo_app/services/reminder_service.py`** (NEW)
   - Purpose: Background thread for reminder checking
   - Classes: `ReminderService`
   - Lines: ~150-200

5. **`src/todo_app/utils/time_utils.py`** (NEW)
   - Purpose: Time parsing, validation, recurrence calculation helpers
   - Functions: `parse_time()`, `validate_time()`, `parse_reminder()`, etc.
   - Lines: ~100-150

6. **`tests/manual_tests.md`** (NEW)
   - Purpose: Manual test scenarios for Advanced features
   - Lines: ~200-300 (documentation)

---

## Implementation Order (Recommended)

Follow this order for incremental, testable delivery:

### Milestone 1: Time-Aware Due Dates (MVP) - User Story 1

**Estimated Time**: 2-3 hours

**Steps**:
1. Extend Task model with `due_time` field and `get_due_datetime()` method
2. Create `utils/time_utils.py` with time parsing/validation functions
3. Modify `add_task_operation()` to prompt for time input
4. Modify `view_tasks_operation()` to display time
5. Modify sort logic to use `get_due_datetime()` for comparisons

**Test**: Create tasks with various times, verify sorting by date+time

**Deliverable**: Tasks can have precise due times (HH:MM)

---

### Milestone 2: Recurring Tasks - User Story 2

**Estimated Time**: 3-4 hours

**Steps**:
1. Add `recurrence` and `parent_recurrence_id` to Task model
2. Add recurrence calculation logic to TaskManager
3. Modify `toggle_task_completion()` to generate next occurrence
4. Extend `add_task_operation()` with recurrence prompts
5. Create `manage_recurrence_operation()` for editing patterns
6. Update `view_tasks_operation()` to show recurrence info
7. Update `delete_task_operation()` with scope prompt

**Test**: Create daily/weekly/custom recurring tasks, mark complete, verify next occurrence

**Deliverable**: Automatic task rescheduling on completion

---

### Milestone 3: Reminders - User Story 3

**Estimated Time**: 3-4 hours

**Steps**:
1. Add `reminders` field to Task model
2. Add `get_reminder_trigger_time()` method to Task
3. Create `services/reminder_service.py` with background thread
4. Add `threading.Lock` to TaskManager for thread-safe access
5. Start ReminderService in `main()` function
6. Create `manage_reminders_operation()` for adding/removing reminders
7. Update `view_tasks_operation()` to show reminder status

**Test**: Create tasks with reminders, wait for trigger time, verify console notification

**Deliverable**: Time-based notifications for upcoming tasks

---

### Milestone 4: Recurrence Management - User Story 4

**Estimated Time**: 2-3 hours

**Steps**:
1. Add occurrence history view to `manage_recurrence_operation()`
2. Add edit recurrence with future-only warning
3. Add stop recurrence option
4. Enhance delete with single/all-future scope

**Test**: Complete recurring task multiple times, view history, edit pattern, verify future-only

**Deliverable**: Full control over recurring task lifecycle

---

## Key Implementation Details

### 1. Time Storage Pattern

```python
# In models/task.py
class Task:
    def __init__(self, ..., due_date=None, due_time=None, ...):
        self.due_date = due_date  # datetime.date or None
        self.due_time = due_time  # "HH:MM" string or None

    def get_due_datetime(self) -> datetime | None:
        """Combine date and time for comparisons."""
        if not self.due_date:
            return None
        time_str = self.due_time if self.due_time else "23:59"
        hour, minute = map(int, time_str.split(':'))
        return datetime.combine(self.due_date, datetime.min.time().replace(hour=hour, minute=minute))
```

**Why**: Backward compatible (due_date remains date type), simple to combine when needed

---

### 2. Recurrence Calculation Logic

```python
# In services/task_manager.py
def _calculate_next_due_date(self, task: Task) -> datetime:
    """Calculate next occurrence from original due date."""
    if not task.due_date:
        # No due date: use completion time
        return datetime.now() + timedelta(days=task.recurrence['interval'])

    # Start from original due date
    next_dt = task.get_due_datetime()
    interval = self._get_recurrence_interval(task.recurrence)

    # Skip forward until future
    now = datetime.now()
    while next_dt <= now:
        next_dt += timedelta(days=interval)

    return next_dt

def _get_recurrence_interval(self, recurrence: dict) -> int:
    """Get interval in days from recurrence pattern."""
    if recurrence['type'] == 'daily':
        return 1
    elif recurrence['type'] == 'weekly':
        return 7
    elif recurrence['type'] == 'custom':
        return recurrence['interval']
    return 0  # 'none' type
```

**Why**: Prevents schedule drift, handles overdue tasks, maintains consistency

---

### 3. Reminder Background Thread

```python
# In services/reminder_service.py
import threading
import time
from datetime import datetime

class ReminderService:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.running = False
        self.thread = None

    def start(self):
        """Start daemon thread."""
        self.running = True
        self.thread = threading.Thread(target=self._check_loop, daemon=True)
        self.thread.start()

    def _check_loop(self):
        """Poll every 60 seconds."""
        while self.running:
            try:
                self._check_all_reminders()
            except Exception as e:
                print(f"[Reminder Error]: {e}")
            time.sleep(60)

    def _check_all_reminders(self):
        """Check tasks for due reminders (thread-safe)."""
        now = datetime.now()
        with self.task_manager.lock:
            for task in self.task_manager.tasks:
                if task.completed:
                    continue
                for reminder in task.reminders:
                    if not reminder['sent']:
                        trigger_time = task.get_reminder_trigger_time(reminder)
                        if trigger_time and now >= trigger_time:
                            self._trigger_reminder(task, reminder)
                            reminder['sent'] = True
                            reminder['sent_at'] = now
```

**Why**: Simple, adequate latency, daemon mode, thread-safe with lock

---

### 4. Thread Safety Pattern

```python
# In services/task_manager.py
import threading

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.lock = threading.Lock()  # Protect task list

    def get_all_tasks(self):
        """Thread-safe access."""
        with self.lock:
            return list(self.tasks)  # Return copy

    def add_task(self, ...):
        """Thread-safe add."""
        with self.lock:
            # ... create task
            self.tasks.append(task)
            return task
```

**Why**: Prevents race conditions when reminder thread reads while main thread modifies

---

## Common Pitfalls and Solutions

### Pitfall 1: Schedule Drift in Recurring Tasks

**Problem**: Calculating next occurrence from completion date causes tasks to "drift" later

**Solution**: Always calculate from original `due_date`, skip forward if result is in past

```python
# ❌ WRONG - causes drift
next_date = datetime.now() + timedelta(days=7)

# ✅ CORRECT - maintains schedule
next_date = task.get_due_datetime() + timedelta(days=7)
while next_date <= datetime.now():
    next_date += timedelta(days=7)
```

---

### Pitfall 2: Reminder Thread Crashes

**Problem**: Unhandled exception in reminder checking crashes background thread silently

**Solution**: Wrap check loop in try/except, log errors, continue checking

```python
# ❌ WRONG - crash stops all future reminders
def _check_loop(self):
    while self.running:
        self._check_all_reminders()
        time.sleep(60)

# ✅ CORRECT - errors logged, checking continues
def _check_loop(self):
    while self.running:
        try:
            self._check_all_reminders()
        except Exception as e:
            print(f"[Reminder Error]: {e}")
        time.sleep(60)
```

---

### Pitfall 3: Race Condition on Task List

**Problem**: Reminder thread iterates task list while main thread modifies it (crash or corrupted data)

**Solution**: Use `threading.Lock` for all task list access

```python
# ❌ WRONG - race condition
for task in self.task_manager.tasks:
    # ... check reminders

# ✅ CORRECT - lock protects access
with self.task_manager.lock:
    for task in self.task_manager.tasks:
        # ... check reminders
```

---

### Pitfall 4: Backward Incompatibility

**Problem**: Changing `due_date` from date to datetime breaks existing code

**Solution**: Keep `due_date` as date type, add separate `due_time` field, combine with helper

```python
# ❌ WRONG - breaking change
self.due_date = datetime(2026, 1, 15, 14, 30)  # Type changed!

# ✅ CORRECT - backward compatible
self.due_date = date(2026, 1, 15)  # Type unchanged
self.due_time = "14:30"             # New field
```

---

## Testing Strategy

### Manual Test Checklist

See `tests/manual_tests.md` for detailed test scenarios. Quick checklist:

**Time-Aware Due Dates**:
- [ ] Create task with date+time (e.g., "2026-01-15 14:30")
- [ ] Create task with date only (verify defaults to "23:59")
- [ ] Sort tasks by due date+time (verify correct order)
- [ ] Update task time (verify preserved)
- [ ] Invalid time input rejected (e.g., "25:00")

**Recurring Tasks**:
- [ ] Create daily recurring task, mark complete, verify next occurrence tomorrow
- [ ] Create weekly recurring task, mark complete, verify next occurrence +7 days
- [ ] Create custom (every 3 days), mark complete, verify next occurrence +3 days
- [ ] Complete overdue recurring task, verify skips to future date
- [ ] Edit recurrence pattern, verify only future occurrences affected
- [ ] Stop recurrence, verify no new occurrences created

**Reminders**:
- [ ] Create task with reminder "15 minutes before"
- [ ] Wait 15 minutes before due time, verify console notification
- [ ] Create task with multiple reminders, verify all trigger
- [ ] Complete task before reminder due, verify no notification
- [ ] Reminder in past warns user but doesn't trigger

**Recurrence Management**:
- [ ] View occurrence history (verify shows past completions)
- [ ] Delete single occurrence (verify others preserved)
- [ ] Delete all future occurrences (verify completed ones preserved)

**Backward Compatibility**:
- [ ] All Basic Level operations still work (CRUD)
- [ ] All Intermediate operations still work (search, filter, sort, priority, tags)
- [ ] Old tasks display correctly (no time, no recurrence, no reminders)

---

## Performance Considerations

### Reminder Checking Efficiency

**60-second polling**: Acceptable for up to ~1000 tasks
- Each check iterates all tasks (~O(n*m) where m=avg reminders per task)
- For 100 tasks with 2 reminders each: 200 comparisons/minute (negligible)
- If performance becomes issue: Use priority queue or scheduled timers

### Recurrence Generation

**On-demand calculation**: Next occurrence calculated on task completion
- Single datetime arithmetic operation (~O(1))
- No pre-calculation or caching needed
- Performance scales linearly with completion rate (not task count)

### Thread Safety Overhead

**Lock contention**: Minimal for CLI application
- Main thread: Infrequent operations (user-driven)
- Reminder thread: 60-second intervals
- Lock held briefly (~milliseconds for iteration)

---

## Deployment Checklist

Before merging Advanced Level implementation:

- [ ] All 4 user stories implemented and manually tested
- [ ] Backward compatibility verified (Basic/Intermediate operations work)
- [ ] No external dependencies added (Python stdlib only)
- [ ] Thread safety verified (no race conditions observed)
- [ ] Performance acceptable (100 recurring tasks, 50 reminders tested)
- [ ] Documentation complete (data-model.md, contracts, quickstart)
- [ ] Edge cases handled (see spec.md Edge Cases section)
- [ ] Constitution requirements met (Phase III checklist passed)

---

## Troubleshooting

### Reminder thread not starting

**Symptom**: Reminders never trigger
**Check**: `reminder_service.start()` called in `main()`?
**Fix**: Add `reminder_service.start()` after `task_manager = TaskManager()`

### Reminder triggers but doesn't display

**Symptom**: Time passes but no console output
**Check**: Task completed before trigger time?
**Fix**: Verify task still pending when reminder due

### Recurring task doesn't generate next occurrence

**Symptom**: Task marked complete but no new task created
**Check**: Recurrence type is not "none"?
**Fix**: Verify `task.recurrence["type"]` in ["daily", "weekly", "custom"]

### Times display incorrectly after DST change

**Symptom**: Task due times off by 1 hour after DST transition
**Expected**: This is correct behavior (local time stored, DST affects display)
**Not a bug**: Document as expected DST behavior

---

## Next Steps

After completing implementation:

1. Run `/sp.tasks` to generate detailed task breakdown
2. Follow task-by-task implementation plan
3. Test each milestone independently before proceeding
4. Create git commits after each milestone
5. Final integration testing with all features enabled

---

## References

- **Specification**: [spec.md](./spec.md) - Requirements and acceptance criteria
- **Research**: [research.md](./research.md) - Technical decisions and rationale
- **Data Model**: [data-model.md](./data-model.md) - Entity definitions
- **Contracts**: [contracts/cli-operations.md](./contracts/cli-operations.md) - Operation signatures
- **Constitution**: `../.specify/memory/constitution.md` - Phase III requirements

---

**Questions or Issues?** Refer to research.md for architectural decisions, or spec.md for functional requirements.
