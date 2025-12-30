# Research: Advanced Level Technical Decisions

**Feature**: Advanced Level - Intelligent Task Management
**Date**: 2025-12-30
**Purpose**: Document technical research and architecture decisions for time-aware task management implementation

## Overview

This document captures the technical investigation and decision-making process for implementing recurring tasks, time-aware due dates, and reminder notifications in the Todo CLI application. All decisions prioritize simplicity, determinism, and backward compatibility with existing Basic and Intermediate level features.

---

## Decision 1: Time Storage and Handling

### Context

Tasks need to support both date and time components for precise scheduling. Existing implementation uses `datetime.date` for `due_date` field. Need to determine how to add time-of-day precision.

### Options Evaluated

**Option A: Separate `due_date` (date) and `due_time` (str) fields**
- Store date as `datetime.date`, time as string "HH:MM"
- Combine when needed for comparisons
- **Pros**: Minimal changes to existing code, clear separation
- **Cons**: Complex sorting (requires combining), harder datetime arithmetic, two fields to validate

**Option B: Combined `due_datetime` (datetime) field, migrate from `due_date`**
- Replace `due_date` with `due_datetime` storing full datetime
- Break backward compatibility with existing tasks
- **Pros**: Simplest comparisons and arithmetic, single source of truth
- **Cons**: Breaking change, requires data migration, violates backward compatibility requirement

**Option C: Keep `due_date` (date), add `due_time` (str), combine internally**
- Store date as `datetime.date`, time as string "HH:MM"
- Create combined datetime when needed using helper function
- **Pros**: Backward compatible, clear field roles, existing code works
- **Cons**: Helper function overhead, two fields to keep in sync

### Decision: **Option C - Hybrid approach with helper function**

**Rationale**:
- Backward compatibility is mandatory (per constitution)
- Existing `due_date` field remains `datetime.date` type
- New `due_time` field stores "HH:MM" string (defaults to "23:59")
- Helper function `get_due_datetime(task)` combines for comparisons/sorting
- Existing tasks without `due_time` get "23:59" default when accessed

**Implementation Details**:
```python
# In models/task.py
from datetime import datetime, date

class Task:
    def get_due_datetime(self) -> datetime | None:
        """Combine due_date and due_time into single datetime for comparisons."""
        if not self.due_date:
            return None
        time_str = self.due_time if self.due_time else "23:59"
        hour, minute = map(int, time_str.split(':'))
        return datetime.combine(self.due_date, datetime.min.time().replace(hour=hour, minute=minute))
```

**Alternatives Rejected**:
- Option A: Too complex for sorting and comparisons
- Option B: Violates backward compatibility requirement

---

## Decision 2: Recurrence Calculation Algorithm

### Context

When a recurring task is marked complete, need to calculate the due date for next occurrence. Two approaches: calculate from completion date or original due date.

### Options Evaluated

**Option A: Calculate from completion date**
- Next occurrence = completion_date + interval
- Example: Weekly task completed 2 days late → next due 7 days from completion
- **Pros**: Simple logic, no special handling for overdue tasks
- **Cons**: Schedule "drifts" over time (tasks creep later and later)

**Option B: Calculate from original due date**
- Next occurrence = original_due_date + interval
- Skip forward if result is in past
- Example: Weekly task completed 2 days late → next due still maintains original weekday
- **Pros**: Maintains schedule consistency, prevents drift
- **Cons**: Slightly more complex (need to skip past dates)

### Decision: **Option B - Calculate from original due date**

**Rationale**:
- Prevents schedule drift (critical for weekly/monthly recurring tasks)
- User expects "every Monday" to stay Monday, not drift to Tuesday/Wednesday
- Edge case handling is straightforward: while next_date < today, add interval again
- Matches behavior of calendar applications (Google Calendar, Outlook)

**Implementation Details**:
```python
# In services/task_manager.py
from datetime import datetime, timedelta

def _calculate_next_occurrence_date(task: Task) -> datetime:
    """Calculate next occurrence date from original due date."""
    if not task.due_date:
        # No due date: calculate from completion time
        return datetime.now() + timedelta(days=task.recurrence['interval'])

    # Start from original due date
    next_date = task.get_due_datetime()
    interval_days = task.recurrence['interval']

    # For weekly, use 7 days regardless of interval value
    if task.recurrence['type'] == 'weekly':
        interval_days = 7
    elif task.recurrence['type'] == 'daily':
        interval_days = 1
    # For 'custom', use interval value as-is

    # Skip forward until date is in future
    now = datetime.now()
    while next_date <= now:
        next_date += timedelta(days=interval_days)

    return next_date
```

**Alternatives Rejected**:
- Option A: Schedule drift unacceptable for recurring tasks (user frustration)

**Edge Cases Handled**:
- Overdue task: Skip forward to next valid future occurrence
- No due date: Use completion date (no original reference point)
- Multiple intervals in past: Loop until future date found

---

## Decision 3: Reminder Background Thread Strategy

### Context

Reminders need to trigger at specific times (e.g., 15 minutes before due time). Need background mechanism to check time and display notifications without blocking CLI interaction.

### Options Evaluated

**Option A: Single daemon thread with polling loop (60s interval)**
- One thread sleeps 60s, wakes up, checks all tasks for due reminders
- **Pros**: Simple, no callback management, daemon thread exits with main
- **Cons**: Up to 60s latency, continuous checking even without reminders

**Option B: Timer-based callbacks (threading.Timer per reminder)**
- Schedule Timer for each reminder's exact time
- **Pros**: Precise timing (<1s latency), no unnecessary checks
- **Cons**: Complex callback management, memory overhead (one Timer per reminder), potential leaks

**Option C: asyncio with scheduled tasks**
- Use asyncio event loop with scheduled coroutines
- **Pros**: Modern Python pattern, precise timing
- **Cons**: Requires rewriting CLI to be async, complex integration, overkill for use case

### Decision: **Option A - Daemon thread with 60s polling**

**Rationale**:
- Simplicity outweighs precision for this use case
- 60s latency acceptable per specification (SC-003: "within 1 minute")
- Daemon thread automatically exits when main process ends
- No callback lifecycle management complexity
- Easy to add thread-safe locking for task list access

**Implementation Details**:
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
        self.lock = threading.Lock()

    def start(self):
        """Start background reminder checking thread."""
        self.running = True
        self.thread = threading.Thread(target=self._check_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop background thread gracefully."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=65)  # Wait for one polling cycle

    def _check_loop(self):
        """Polling loop checking for due reminders every 60s."""
        while self.running:
            try:
                self._check_all_reminders()
            except Exception as e:
                print(f"[Reminder Error]: {e}")
            time.sleep(60)

    def _check_all_reminders(self):
        """Check all tasks for due reminders (thread-safe)."""
        now = datetime.now()
        with self.lock:
            for task in self.task_manager.get_all_tasks():
                if task.completed:
                    continue  # Skip completed tasks
                for reminder in task.reminders:
                    if not reminder['sent'] and self._is_reminder_due(task, reminder, now):
                        self._trigger_reminder(task, reminder)
                        reminder['sent'] = True
                        reminder['sent_at'] = now
```

**Alternatives Rejected**:
- Option B: Over-engineering, Timer lifecycle complexity not worth precision gain
- Option C: Async rewrite too invasive for marginal benefit

---

## Decision 4: Browser Notification Simulation (CLI Context)

### Context

Specification requires "browser notifications" but application is CLI-based with no browser context. Need fallback mechanism for displaying reminders.

### Options Evaluated

**Option A: Console output with timestamp**
- Print reminder message to console when due
- **Pros**: No dependencies, visible in CLI, simple implementation
- **Cons**: User must be watching console, not persistent

**Option B: System notifications (plyer library)**
- Use cross-platform notification library
- **Pros**: Desktop notifications work like browser notifications
- **Cons**: Violates zero-dependency constraint, platform inconsistencies

**Option C: Write to log file**
- Append reminders to `reminders.log` file
- **Pros**: Persistent record, no dependencies
- **Cons**: User won't see unless monitoring file, not a "notification"

### Decision: **Option A - Console output with timestamp**

**Rationale**:
- Zero-dependency constraint is mandatory (constitution)
- CLI context implies user is at terminal
- Console output provides immediate feedback if user present
- Clear formatting makes reminders stand out from normal CLI output
- Matches CLI application paradigm (all output goes to console)

**Implementation Details**:
```python
def _trigger_reminder(self, task: Task, reminder: dict):
    """Display console-based reminder notification."""
    now = datetime.now()
    due_dt = task.get_due_datetime()

    print("\n" + "=" * 60)
    print("⏰ REMINDER NOTIFICATION")
    print("=" * 60)
    print(f"Task: {task.title}")
    print(f"Due: {due_dt.strftime('%Y-%m-%d %H:%M')}")
    print(f"Priority: {task.priority.upper()}")
    if task.tags:
        print(f"Tags: {', '.join(task.tags)}")
    print(f"Reminder: {reminder['offset_value']} {reminder['offset_unit']} before due time")
    print(f"Triggered at: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")
```

**Alternatives Rejected**:
- Option B: Violates zero-dependency requirement
- Option C: Not a true "notification" (requires manual file monitoring)

**Notes**:
- Future enhancement: If application runs in web context, could add actual browser notification API
- Console output clearly marked as "REMINDER NOTIFICATION" to distinguish from normal output

---

## Decision 5: Data Model Storage (Recurrence/Reminders)

### Context

Recurring tasks and reminders need to be stored. Options range from simple dicts/lists to full ORM-style classes.

### Options Evaluated

**Option A: Store as dicts/lists on Task instances**
- `recurrence: dict = {"type": "none", "interval": 1}`
- `reminders: list[dict] = []`
- **Pros**: Simple, matches in-memory pattern, easy to serialize later
- **Cons**: No type safety, manual validation needed

**Option B: Create Reminder and Recurrence classes**
- Full dataclasses or classes with properties
- **Pros**: Type safety, encapsulated validation, cleaner code
- **Cons**: Over-engineering for in-memory app, more boilerplate

**Option C: Use dataclasses with frozen=True**
- Immutable dataclass instances
- **Pros**: Type safety + immutability guarantees
- **Cons**: Immutability complicates updates (sent status, sent_at timestamp)

### Decision: **Option A - Dicts/lists on Task**

**Rationale**:
- In-memory application with no persistence (no ORM benefits)
- Simplicity aligns with existing Task implementation
- Easy to extend/modify without class changes
- If persistence added later, dicts serialize naturally to JSON
- Validation can be done at TaskManager level (no need for class-level validation)

**Implementation Details**:
```python
# In models/task.py
class Task:
    def __init__(self, ..., recurrence=None, reminders=None):
        # Recurrence default
        self.recurrence = recurrence if recurrence else {"type": "none", "interval": 1}

        # Reminders default
        self.reminders = reminders if reminders else []

        # Validate recurrence structure
        if self.recurrence["type"] not in ["none", "daily", "weekly", "custom"]:
            raise ValueError(f"Invalid recurrence type: {self.recurrence['type']}")
```

**Alternatives Rejected**:
- Option B: Over-engineering for in-memory use case
- Option C: Immutability conflicts with updating reminder `sent` status

---

## Decision 6: Thread Safety for Reminder Checking

### Context

Background reminder thread reads task list while main CLI thread may be modifying it (adding, deleting, completing tasks). Need thread-safe access pattern.

### Options Evaluated

**Option A: threading.Lock for task list access**
- Single lock protects entire task list
- All access (read/write) acquires lock
- **Pros**: Simple, correct, no race conditions
- **Cons**: Lock contention if frequent access (unlikely in CLI app)

**Option B: Copy-on-read snapshot**
- Reminder thread makes copy of task list for each check
- **Pros**: No blocking, reads always succeed
- **Cons**: Memory overhead, changes during check not seen, copy overhead

**Option C: No locking (risk race conditions)**
- Hope for best, Python GIL might protect
- **Pros**: Simplest implementation
- **Cons**: Undefined behavior, potential crashes from list modification during iteration

### Decision: **Option A - threading.Lock**

**Rationale**:
- Correctness is more important than performance in this case
- Lock contention unlikely (60s reminder polling, infrequent CLI operations)
- Python list iteration can crash if list modified during iteration (GIL doesn't protect)
- Simple implementation with clear semantics
- Lock held for short duration (iteration + reminder checks)

**Implementation Details**:
```python
# In services/task_manager.py
import threading

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.lock = threading.Lock()  # Protect task list access

    def get_all_tasks(self):
        """Thread-safe task retrieval."""
        with self.lock:
            return list(self.tasks)  # Return copy to avoid iterator invalidation

# In services/reminder_service.py
def _check_all_reminders(self):
    """Check reminders with lock protection."""
    with self.task_manager.lock:
        for task in self.task_manager.tasks:
            # ... check reminders
```

**Alternatives Rejected**:
- Option B: Memory overhead and stale data not worth avoiding lock
- Option C: Unacceptable risk of crashes (no GIL protection for list iteration)

---

## Decision 7: Timezone Handling

### Context

Due dates with times need timezone context. Need to decide how to handle timezones, especially for cross-timezone users.

### Options Evaluated

**Option A: Store in local timezone (system default)**
- All datetime values use local time
- Display matches system clock
- **Pros**: Simple, matches user expectations, no conversion needed
- **Cons**: Confusing if user travels, no UTC consistency

**Option B: Store in UTC, display in local time**
- All storage uses UTC
- Convert to local for display
- **Pros**: Consistent internal representation, handles timezone changes
- **Cons**: Complexity, pytz dependency or stdlib timezone handling, overkill for single-user CLI

**Option C: Store with timezone info (aware datetimes)**
- Use timezone-aware datetime objects
- **Pros**: Explicit timezone handling, correct DST transitions
- **Cons**: Complexity, requires pytz or zoneinfo, overkill for use case

### Decision: **Option A - Local timezone only**

**Rationale**:
- Single-user CLI application (no cross-timezone sharing)
- Complexity of timezone conversion not justified
- User's mental model is local time (when they see clock, thinks in local time)
- Zero-dependency constraint (no pytz)
- DST transitions handled by OS (datetime.now() automatically uses DST)
- Document assumption clearly in quickstart guide

**Implementation Details**:
```python
# Always use naive datetime (no timezone info)
from datetime import datetime

now = datetime.now()  # Local time, naive
due = datetime.combine(due_date, time(hour, minute))  # Naive datetime
```

**Limitations Documented**:
- Times displayed may shift by 1 hour during DST transitions (expected behavior)
- Not suitable for cross-timezone task sharing (out of scope)
- Future enhancement: Add timezone support if persistence/sharing added

**Alternatives Rejected**:
- Option B: UTC storage confusing when displayed times don't match local clock
- Option C: Over-engineering for single-user CLI application

---

## Decision 8: Recurrence History Tracking

### Context

Need to track relationship between recurring task occurrences for viewing completion history and managing recurrence patterns.

### Options Evaluated

**Option A: parent_recurrence_id links occurrences**
- Each generated occurrence stores ID of original task
- All occurrences kept in main task list
- **Pros**: Simple queries (filter by parent_id), single data structure
- **Cons**: Task list grows over time, need to distinguish original vs occurrence

**Option B: Separate occurrence list on Task**
- Original task has `occurrences: list[Task]` field
- Completed occurrences stored in nested list
- **Pros**: Clear separation, easy to find all occurrences
- **Cons**: Nested structure complicates filtering/searching, two sources of truth

**Option C: Separate RecurrenceGroup entity**
- New entity managing list of related occurrences
- **Pros**: Clean abstraction, dedicated recurrence management
- **Cons**: Over-engineering, requires two-way links, complex queries

### Decision: **Option A - parent_recurrence_id field**

**Rationale**:
- Keeps all tasks in single flat list (consistent with existing design)
- Easy to filter: `[t for t in tasks if t.parent_recurrence_id == original_id]`
- Simple to display history: "Completed: 2025-12-25, 2025-12-18, 2025-12-11"
- First occurrence has `parent_recurrence_id = None` (is root)
- Generated occurrences have `parent_recurrence_id = root_task.id`

**Implementation Details**:
```python
# In models/task.py
class Task:
    def __init__(self, ..., parent_recurrence_id=None):
        self.parent_recurrence_id = parent_recurrence_id

# When generating next occurrence
def create_next_occurrence(completed_task):
    # Determine root ID (completed_task might itself be an occurrence)
    root_id = completed_task.parent_recurrence_id or completed_task.id

    new_task = Task(
        # ... copy fields from completed_task
        parent_recurrence_id=root_id  # Link to root
    )
    return new_task

# Query occurrence history
def get_occurrence_history(task):
    root_id = task.parent_recurrence_id or task.id
    return [t for t in all_tasks if t.parent_recurrence_id == root_id and t.completed]
```

**Alternatives Rejected**:
- Option B: Nested structure complicates search/filter operations
- Option C: Over-engineering, RecurrenceGroup adds unnecessary abstraction

---

## Summary of Key Decisions

| Area | Decision | Primary Rationale |
|------|----------|-------------------|
| Time Storage | Hybrid (date + time string + helper) | Backward compatibility |
| Recurrence Calc | From original due date | Prevents schedule drift |
| Reminder Thread | 60s polling daemon | Simplicity, adequate latency |
| Notifications | Console output | Zero dependencies |
| Data Storage | Dicts/lists on Task | Matches existing pattern |
| Thread Safety | threading.Lock | Correctness over performance |
| Timezone | Local time only | Single-user CLI context |
| Recurrence History | parent_recurrence_id | Flat list consistency |

All decisions prioritize simplicity, determinism, and backward compatibility while satisfying functional requirements from the specification.

---

## Open Questions (Resolved)

None. All technical unknowns have been researched and decided.

---

## References

- **Python datetime documentation**: https://docs.python.org/3/library/datetime.html
- **Python threading documentation**: https://docs.python.org/3/library/threading.html
- **Specification**: specs/002-advanced-features/spec.md
- **Constitution**: .specify/memory/constitution.md (Phase III requirements)
