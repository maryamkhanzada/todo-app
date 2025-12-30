# CLI Operations Contract: Advanced Level

**Feature**: Advanced Level - Intelligent Task Management
**Date**: 2025-12-30
**Purpose**: Define CLI operation signatures and behaviors for time-aware task management

## Overview

This document specifies the command-line interface operations for Advanced Level features, extending existing Basic and Intermediate CLI operations with time input, recurrence management, and reminder configuration.

---

## Modified Operations (Existing operations extended)

### add_task_operation(task_manager: TaskManager, reminder_service: ReminderService)

**Purpose**: Create new task with optional time, recurrence, and reminders

**Signature**: Extended from Basic/Intermediate with new prompts

**User Interaction Flow**:

```
1. Enter task title: [user input]
2. Enter task description: [user input]
3. Enter priority (high/medium/low) or press Enter for default [medium]: [user input]
4. Enter tags (comma-separated) or press Enter to skip: [user input]
5. Enter due date (YYYY-MM-DD) or press Enter to skip: [user input]
   → If date entered:
     6. Enter due time (HH:MM) or press Enter for end of day [23:59]: [user input]
     7. Set recurrence? (yes/no) [no]: [user input]
        → If yes:
          8. Recurrence type (daily/weekly/custom): [user input]
             → If custom:
               9. Every N days (1-365): [user input]
     10. Add reminders? (yes/no) [no]: [user input]
         → If yes (repeats until user enters "done"):
           11. Reminder: N minutes/hours/days before (or "done" to finish): [user input]
```

**Input Validation**:
- Due date: Must match `YYYY-MM-DD` format, reject invalid dates
- Due time: Must match `HH:MM` 24-hour format, reject invalid times (25:00, 13:75)
- Recurrence type: Must be "daily", "weekly", or "custom"
- Custom interval: Must be integer 1-365
- Reminder format: Must be "{value} {unit}" where unit is "minutes"/"hours"/"days"

**Error Handling**:
- Invalid date: "Error: Invalid date format. Use YYYY-MM-DD (e.g., 2026-01-15)"
- Invalid time: "Error: Invalid time format. Use HH:MM in 24-hour format (e.g., 14:30)"
- Invalid recurrence: "Error: Recurrence type must be 'daily', 'weekly', or 'custom'"
- Invalid reminder: "Error: Reminder format must be 'N minutes/hours/days'"
- Reminder in past: "Warning: Reminder time is in the past and will not trigger"

**Output**:
```
Task added successfully! Task ID: 42
Due: 2026-01-15 14:30
Recurrence: Every 7 days (weekly)
Reminders: 1 day before, 15 minutes before
```

**Backward Compatibility**:
- User can skip time, recurrence, reminders by pressing Enter
- Skipped fields use defaults (time="23:59", recurrence="none", reminders=[])

---

### update_task_operation(task_manager: TaskManager, reminder_service: ReminderService)

**Purpose**: Update existing task including time, recurrence, and reminders

**Signature**: Extended from Basic/Intermediate with new fields

**User Interaction Flow**:

```
1. Enter task ID to update: [user input]
   → System displays current task details with time, recurrence, reminders
2. Current Title: [value]
   Current Description: [value]
   Current Priority: [value]
   Current Tags: [value]
   Current Due: [date] [time] or None
   Current Recurrence: [pattern] or None
   Current Reminders: [list] or None

3. Enter new title (or press Enter to keep current): [user input]
4. Enter new description (or press Enter to keep current): [user input]
5. Enter new priority (or press Enter to keep current): [user input]
6. Enter new tags (or press Enter to keep current): [user input]
7. Enter new due date (or press Enter to keep current, or "none" to remove): [user input]
   → If date entered or existing:
     8. Enter new due time (or press Enter to keep current, or "none" to remove): [user input]
9. Update recurrence? (yes/no/clear) [no]: [user input]
   → If yes: [follow recurrence setup flow]
   → If clear: Remove recurrence (task becomes non-recurring)
10. Update reminders? (yes/no/clear) [no]: [user input]
    → If yes: [follow reminder setup flow]
    → If clear: Remove all reminders
```

**Special Behaviors**:
- Changing due_date/due_time recalculates reminder trigger times (relative reminders)
- Editing recurrence pattern prompts: "This affects only future occurrences. Continue? (yes/no)"
- Clearing recurrence prompts: "Stop recurring? Future occurrences will not be created. Continue? (yes/no)"

**Output**:
```
Task updated successfully!
Changes: Due time changed to 15:30, recurrence updated to every 3 days
```

---

### toggle_task_completion(task_manager: TaskManager, reminder_service: ReminderService)

**Purpose**: Mark task complete/incomplete, trigger recurrence generation

**Signature**: Extended from Basic with recurrence logic

**User Interaction Flow**:

```
1. Enter task ID to toggle completion status: [user input]
   → System retrieves task
2. Task: [title]
   Current Status: [Pending/Completed]
   Toggle to: [Completed/Pending]? (yes/no): [user input]
   → If yes and task has recurrence:
     3. [System generates next occurrence]
     4. Display: "Task marked as Completed! Next occurrence created: Task ID 43, Due 2026-01-22 14:30"
   → If yes and no recurrence:
     5. Display: "Task marked as Completed!"
```

**Recurrence Generation Logic**:
- Calculate next due date from original due_date + recurrence interval
- Skip forward if calculated date is in past
- Copy all task attributes (title, description, priority, tags, recurrence)
- Copy reminders with `sent=False`, `sent_at=None` (reset sent status)
- Set `parent_recurrence_id` to link occurrence to root task
- Add new task to task list
- Preserve completed task in list (both exist for history)

**Reminder Handling**:
- Cancel all reminders on completed task (set `sent=True` to prevent triggering)
- New occurrence gets fresh reminders (not marked as sent)

**Output Examples**:
```
# Non-recurring task
Task marked as Completed!

# Recurring task
Task marked as Completed!
Next occurrence created:
  Task ID: 43
  Title: Weekly Team Meeting
  Due: 2026-01-22 14:30
  Recurrence: Every 7 days
```

---

### view_tasks_operation(task_manager: TaskManager, active_filters: dict, active_sort: dict)

**Purpose**: Display tasks with time, recurrence, and reminder information

**Signature**: Extended from Intermediate with new display fields

**Display Format** (per task):

```
[ID] Title [PRIORITY] [tags]
    Description: [text]
    Status: [Pending/Completed]
    Due: [YYYY-MM-DD HH:MM] or None
    Recurrence: [pattern description] or None
    Reminders: [list of reminders] or None
    Occurrence History: [completion dates if recurring] or None
```

**Recurrence Display Examples**:
- Daily: "Repeats: Every day"
- Weekly: "Repeats: Every 7 days (weekly)"
- Custom: "Repeats: Every 3 days"
- None: [field omitted]

**Reminder Display Examples**:
- `[{"offset_value": 15, "offset_unit": "minutes", "sent": False}]` → "Reminder: 15 minutes before (pending)"
- `[{"offset_value": 1, "offset_unit": "days", "sent": True, "sent_at": ...}]` → "Reminder: 1 day before (sent on 2026-01-14 14:30)"
- Multiple: "Reminders: 1 day before (pending), 15 minutes before (pending)"

**Occurrence History** (for recurring tasks):
- Show last 5 completed occurrences
- Format: "Completed: 2025-12-25, 2025-12-18, 2025-12-11 (+2 more)"

**Sort Behavior**:
- When sorted by due date: Tasks sorted by `get_due_datetime()` (includes time)
- Tasks with same date sorted by time (earlier first)

---

### delete_task_operation(task_manager: TaskManager, reminder_service: ReminderService)

**Purpose**: Delete task with recurrence scope handling

**Signature**: Extended from Basic with recurrence confirmation

**User Interaction Flow**:

```
1. Enter task ID to delete: [user input]
   → System retrieves task and checks recurrence
2. Task to delete:
     ID: [id]
     Title: [title]
     Description: [description]
     Recurrence: [pattern or None]

   → If task has recurrence or is recurring occurrence:
     3. This is a recurring task. Delete:
        1. Only this occurrence
        2. This and all future occurrences
        Choice (1/2): [user input]

   → If non-recurring:
     3. Are you sure you want to delete this task? (yes/no): [user input]

   → If confirmed:
     4. [Delete task(s)]
     5. [Cancel associated reminders via reminder_service]
     6. Display: "Task deleted successfully!" or "Task and future occurrences deleted!"
```

**Deletion Scopes**:
- **"Only this occurrence"**: Delete single task, keep others with same `parent_recurrence_id`
- **"All future occurrences"**: Delete this task + all tasks where `parent_recurrence_id == root_id AND completed == False`
- **Completed occurrences**: Never deleted automatically (preserved for history)

**Reminder Cleanup**:
- All reminders for deleted task(s) must be cancelled (prevent notifications for non-existent tasks)

---

## New Operations (Advanced Level only)

### manage_recurrence_operation(task_manager: TaskManager)

**Purpose**: Sub-menu for managing recurring tasks

**User Interaction Flow**:

```
MANAGE RECURRENCE - MENU
1. Set/Edit Recurrence Pattern
2. Stop Recurrence (keep task)
3. View Occurrence History
4. Back to Main Menu

Enter your choice (1-4): [user input]

→ If choice == 1:
  [Follow recurrence setup flow]

→ If choice == 2:
  Enter task ID: [user input]
  Confirm stop recurrence? Future occurrences will not be created. (yes/no): [user input]
  [If yes: Set recurrence.type = "none"]

→ If choice == 3:
  Enter task ID: [user input]
  [Display all occurrences with completion dates]
  Occurrence History for "[title]":
    ✓ 2025-12-25 14:30 (completed)
    ✓ 2025-12-18 14:30 (completed)
    ✓ 2025-12-11 14:30 (completed)
    • 2026-01-01 14:30 (pending - current occurrence)
```

---

### manage_reminders_operation(task_manager: TaskManager, reminder_service: ReminderService)

**Purpose**: Sub-menu for managing task reminders

**User Interaction Flow**:

```
MANAGE REMINDERS - MENU
1. Add Reminder
2. Remove Reminder
3. View Reminders
4. Back to Main Menu

Enter your choice (1-4): [user input]

→ If choice == 1:
  Enter task ID: [user input]
  Enter reminder (e.g., "15 minutes", "1 hour", "1 day"): [user input]
  [Validate format]
  [Add reminder to task.reminders list]
  Display: "Reminder added: 15 minutes before due time"

→ If choice == 2:
  Enter task ID: [user input]
  [Display numbered list of reminders]
  1. 1 day before (pending)
  2. 15 minutes before (pending)
  Which reminder to remove (1-N): [user input]
  [Remove reminder from list]
  Display: "Reminder removed"

→ If choice == 3:
  Enter task ID: [user input]
  [Display all reminders with status]
  Reminders for "[title]":
    • 1 day before - Status: Sent on 2026-01-14 14:30
    • 15 minutes before - Status: Pending
```

---

## Service Operations (ReminderService)

### ReminderService.__init__(task_manager: TaskManager)

**Purpose**: Initialize reminder service with reference to task manager

**Parameters**:
- `task_manager`: TaskManager instance for accessing task list

**Initialization**:
- Store task_manager reference
- Initialize running flag (False)
- Initialize thread reference (None)
- Create threading.Lock for thread-safe access

---

### ReminderService.start()

**Purpose**: Start background reminder checking thread

**Behavior**:
- Set `running = True`
- Create daemon thread running `_check_loop()`
- Start thread
- Daemon mode: Thread exits automatically when main process exits

**Thread Safety**: Uses task_manager.lock for all task list access

---

### ReminderService.stop()

**Purpose**: Stop background thread gracefully

**Behavior**:
- Set `running = False`
- Wait for thread to finish (max 65 seconds - one polling cycle)
- Clean shutdown

**Usage**: Called on application exit (Ctrl+C, menu exit)

---

### ReminderService._check_loop() [Internal]

**Purpose**: Polling loop checking for due reminders

**Behavior**:
```python
while self.running:
    try:
        self._check_all_reminders()
    except Exception as e:
        print(f"[Reminder Error]: {e}")
    time.sleep(60)  # 60-second polling interval
```

**Error Handling**: Wrap in try/except to prevent thread crash from single error

---

### ReminderService._check_all_reminders() [Internal]

**Purpose**: Check all tasks for due reminders (called every 60s)

**Behavior**:
```python
now = datetime.now()
with task_manager.lock:
    for task in task_manager.tasks:
        if task.completed:
            continue  # Skip completed tasks
        for reminder in task.reminders:
            if not reminder['sent']:
                trigger_time = task.get_reminder_trigger_time(reminder)
                if trigger_time and now >= trigger_time:
                    self._trigger_reminder(task, reminder)
                    reminder['sent'] = True
                    reminder['sent_at'] = now
```

**Thread Safety**: Acquires lock before iterating task list

---

### ReminderService._trigger_reminder(task: Task, reminder: dict) [Internal]

**Purpose**: Display console notification for reminder

**Output Format**:
```
============================================================
⏰ REMINDER NOTIFICATION
============================================================
Task: Weekly Team Meeting
Due: 2026-01-15 14:30
Priority: HIGH
Tags: work, meeting
Reminder: 15 minutes before due time
Triggered at: 2026-01-15 14:15:23
============================================================
```

**Behavior**:
- Print formatted notification to console
- Include task title, due datetime, priority, tags
- Include reminder offset and trigger time
- Clearly marked as "REMINDER NOTIFICATION" to distinguish from normal output

---

## Validation Summary

| Operation | Validation | Error Message |
|-----------|------------|---------------|
| add_task | Due date format | "Invalid date format. Use YYYY-MM-DD" |
| add_task | Due time format | "Invalid time format. Use HH:MM (24-hour)" |
| add_task | Recurrence type | "Recurrence type must be daily/weekly/custom" |
| add_task | Custom interval | "Interval must be 1-365 days" |
| add_task | Reminder format | "Format: 'N minutes/hours/days'" |
| add_task | Reminder in past | "Warning: Reminder time is in the past" |
| update_task | Task not found | "Error: Task with ID X not found" |
| delete_task | Recurrence scope | Prompt for scope (occurrence vs all future) |
| manage_reminders | Invalid reminder number | "Invalid reminder number. Choose 1-N" |

---

## Integration Points

1. **TaskManager ↔ ReminderService**:
   - ReminderService reads task list via `task_manager.tasks` (with lock)
   - ReminderService updates reminder `sent` status directly on Task objects
   - No TaskManager methods called from reminder thread (only direct task access)

2. **CLI ↔ TaskManager**:
   - CLI validates all input before passing to TaskManager
   - TaskManager performs final validation on Task creation
   - CLI formats output from Task objects

3. **CLI ↔ ReminderService**:
   - CLI starts ReminderService in main() after TaskManager initialization
   - CLI stops ReminderService on exit (Ctrl+C, menu exit)
   - No direct CLI → ReminderService calls during operation (service runs autonomously)

---

## Backward Compatibility

**All existing Basic/Intermediate operations continue working**:

- `add_task()` without time/recurrence/reminders creates standard task
- `update_task()` on old tasks works (new fields shown as "None" or default)
- `view_tasks()` shows old tasks without time/recurrence/reminders (fields omitted)
- `delete_task()` on non-recurring tasks behaves identically to Basic level
- `toggle_task_completion()` on non-recurring tasks unchanged

**No breaking changes** - Only additive extensions to existing operations.

---

## References

- **Specification**: specs/002-advanced-features/spec.md (Functional Requirements FR-006 to FR-028)
- **Data Model**: specs/002-advanced-features/data-model.md (Task extensions)
- **Research**: specs/002-advanced-features/research.md (Decision 3: Reminder thread strategy)
