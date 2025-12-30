# Feature Specification: Advanced Level - Intelligent Task Management

**Feature Branch**: `002-advanced-features`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Specify the ADVANCED level requirements for the Todo application. Assume BASIC and INTERMEDIATE levels are fully implemented. Focus on intelligent, time-aware task management features only. The system must support: Recurring tasks with automatic rescheduling (daily, weekly, or custom recurrence patterns), Completing a recurring task MUST automatically generate the next occurrence, Due dates with date and time support for tasks, Time-based reminders associated with task due dates, Browser notifications for reminders where supported. Clearly define: Recurrence rules and edge cases, Reminder scheduling and trigger behavior, Data model extensions required for recurrence and time handling, User interaction flow for setting and managing these features. Do NOT include UI styling, collaboration, payments, or AI predictions. Focus strictly on intelligent task behavior and scheduling."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Time-Aware Due Dates (Priority: P1) 🎯 MVP

Users can specify exact due dates with times (not just dates) for their tasks, enabling precise scheduling and time-based notifications.

**Why this priority**: This is the foundation for all time-aware features. Without precise due dates/times, reminders and recurrence cannot function properly. This delivers immediate value by allowing users to schedule tasks at specific times.

**Independent Test**: Create tasks with various date+time combinations (e.g., "2026-01-15 14:30"), verify tasks display the time component, verify tasks can be filtered/sorted by date+time, verify time is preserved when updating tasks.

**Acceptance Scenarios**:

1. **Given** a user is creating a new task, **When** they specify a due date with time (e.g., "2026-01-15 14:30"), **Then** the task stores and displays both date and time components
2. **Given** a user views a task with a due date+time, **When** the task is displayed, **Then** the time is shown in 24-hour format (HH:MM)
3. **Given** a task has a due date with time, **When** the user updates the task, **Then** the time component is preserved and editable
4. **Given** multiple tasks have different due times on the same date, **When** tasks are sorted by due date, **Then** tasks are ordered by date first, then by time within the same date
5. **Given** a user creates a task without specifying time, **When** the task is saved, **Then** the time defaults to 23:59 (end of day)

---

### User Story 2 - Recurring Tasks with Automatic Rescheduling (Priority: P2)

Users can mark tasks as recurring with customizable patterns (daily, weekly, monthly, custom intervals), and completing a recurring task automatically creates the next occurrence based on the recurrence rule.

**Why this priority**: Recurring tasks eliminate repetitive data entry and ensure users never forget routine activities. This is the core "intelligent" behavior that differentiates Advanced level from Intermediate.

**Independent Test**: Create recurring tasks with different patterns (daily, weekly, custom), mark them complete, verify next occurrence is automatically generated with correct due date/time, verify recurrence can be edited or stopped.

**Acceptance Scenarios**:

1. **Given** a user creates a task with daily recurrence, **When** the task is marked complete, **Then** a new task with the same title/description/priority/tags is created with due date set to tomorrow at the same time
2. **Given** a user creates a task with weekly recurrence, **When** the task is marked complete, **Then** a new task is created with due date set to 7 days from the original due date
3. **Given** a user creates a task with custom recurrence (e.g., every 3 days), **When** the task is marked complete, **Then** a new task is created with due date set to 3 days from the original due date
4. **Given** a recurring task exists, **When** the user marks it complete, **Then** the original task is marked complete AND a new occurrence is created (both tasks exist in history)
5. **Given** a recurring task exists, **When** the user edits the recurrence pattern, **Then** future occurrences use the new pattern, but past completed occurrences remain unchanged
6. **Given** a recurring task exists, **When** the user deletes the task, **Then** the user is prompted to confirm deletion and asked whether to delete only this occurrence or all future occurrences
7. **Given** a recurring task with no due date/time, **When** marked complete, **Then** the next occurrence due date is calculated from completion date (not original due date)

---

### User Story 3 - Time-Based Reminders with Notifications (Priority: P3)

Users can set reminders for tasks with due dates/times, and receive browser notifications at the specified reminder time (if supported by the environment).

**Why this priority**: Reminders ensure users don't miss important deadlines. Browser notifications leverage platform capabilities to alert users even when not actively viewing the app.

**Independent Test**: Create tasks with reminders at various times (15 min before, 1 hour before, 1 day before), verify reminders trigger at correct time, verify browser notifications appear (in CLI, this may be logged output), verify reminders can be added/removed/modified.

**Acceptance Scenarios**:

1. **Given** a user creates a task with due date+time, **When** they add a reminder (e.g., "15 minutes before"), **Then** the reminder is stored with the task and shows in task details
2. **Given** a task has a reminder set, **When** the reminder time arrives, **Then** a browser notification is displayed (if supported) with task title and due time
3. **Given** a task has a reminder set, **When** the reminder time arrives and notifications are not supported, **Then** the reminder is logged to console with task details
4. **Given** a task has multiple reminders (e.g., 1 day before AND 15 min before), **When** each reminder time arrives, **Then** separate notifications are triggered for each reminder
5. **Given** a task with reminder is marked complete, **When** the reminder time arrives, **Then** no notification is sent (reminders are cancelled on completion)
6. **Given** a task reminder has already triggered, **When** the user views the task, **Then** the task shows the reminder was sent and at what time
7. **Given** a recurring task has reminders, **When** the next occurrence is created, **Then** the reminders are copied to the new occurrence with updated times

---

### User Story 4 - Manage Recurring Patterns (Priority: P4)

Users can view, edit, and stop recurrence patterns for recurring tasks, with clear visibility into past and future occurrences.

**Why this priority**: Full control over recurrence ensures users can adapt to changing schedules. Viewing occurrence history provides accountability and tracking.

**Independent Test**: Create recurring task, complete it multiple times to generate history, edit recurrence pattern, verify future occurrences use new pattern, verify past occurrences unchanged, delete recurrence entirely.

**Acceptance Scenarios**:

1. **Given** a recurring task exists, **When** the user views task details, **Then** the recurrence pattern is clearly displayed (e.g., "Repeats: Every 7 days")
2. **Given** a recurring task has multiple completed occurrences, **When** the user views the task, **Then** a list of past completions with dates is displayed
3. **Given** a recurring task exists, **When** the user edits the recurrence pattern, **Then** the user is prompted to confirm changes and warned that only future occurrences will be affected
4. **Given** a recurring task exists, **When** the user chooses to stop recurrence, **Then** future occurrences are not created when the current task is completed
5. **Given** a user deletes a recurring task, **When** prompted, the user selects "delete all future occurrences", **Then** all incomplete occurrences are deleted, completed ones remain in history

---

### Edge Cases

#### Recurrence Edge Cases

- **What happens when a recurring task is completed before its due date?**
  The next occurrence is calculated from the original due date, not the completion date (except for tasks with no due date, where next occurrence is calculated from completion date). This prevents "drift" in scheduled recurring tasks.

- **What happens when a recurring task is completed after its due date?**
  Same behavior - next occurrence is calculated from the original due date to maintain schedule consistency. The overdue status is recorded but doesn't affect recurrence calculation.

- **What happens when a user deletes a recurring task occurrence?**
  Two options are presented: (1) Delete only this occurrence, or (2) Delete this and all future occurrences. Past completed occurrences are never deleted automatically.

- **What happens when a recurring task pattern would create a due date in the past?**
  The system skips to the next valid future date. For example, if a weekly task is 3 weeks overdue and completed, it creates the next occurrence 7 days from the original due date that falls in the future.

- **What happens when a user edits a recurring task's title/description/priority?**
  Changes apply only to the current occurrence. To change all future occurrences, the user must edit the recurrence pattern separately.

#### Reminder Edge Cases

- **What happens when a reminder time has already passed when the task is created?**
  The reminder is not triggered for past times. The system warns the user that the reminder time is in the past.

- **What happens when multiple reminders trigger simultaneously?**
  Each reminder triggers independently. Multiple notifications may appear at once if reminder times coincide.

- **What happens when browser notifications are not supported?**
  Reminders are logged to console output with timestamp and task details. Users are warned during reminder setup that notifications are unavailable.

- **What happens when a task with reminder is deleted?**
  All associated reminders are cancelled and removed from the reminder queue.

- **What happens when a task's due date is changed after a reminder is set?**
  Relative reminders (e.g., "15 minutes before") are recalculated based on the new due date. Absolute reminders (if supported) remain at their original time.

#### Time Handling Edge Cases

- **What happens when a task due time is set to an invalid time (e.g., 25:00)?**
  The system validates time input and rejects invalid times with a clear error message.

- **What happens when daylight saving time changes affect a task's due time?**
  Times are stored in a consistent format (24-hour clock). DST changes affect display but not the stored time value. No automatic adjustments are made.

- **What happens when a user specifies only a date without time?**
  The time defaults to 23:59 (end of day) for sorting and reminder purposes.

## Requirements *(mandatory)*

### Functional Requirements

#### Time-Aware Due Dates (FR-001 to FR-005)

- **FR-001**: System MUST support due dates with both date AND time components in format YYYY-MM-DD HH:MM
- **FR-002**: System MUST validate time input and reject invalid times (e.g., 25:00, 13:75)
- **FR-003**: System MUST default time to 23:59 when user specifies only a date without time
- **FR-004**: System MUST preserve time component when tasks are updated, filtered, or sorted
- **FR-005**: System MUST sort tasks by date first, then by time within the same date

#### Recurring Tasks (FR-006 to FR-017)

- **FR-006**: System MUST allow users to mark tasks as recurring with pattern options: daily, weekly, every N days (custom interval)
- **FR-007**: System MUST store recurrence pattern as part of task metadata (pattern type, interval value)
- **FR-008**: System MUST automatically create next occurrence when a recurring task is marked complete
- **FR-009**: Next occurrence MUST have same title, description, priority, tags, and recurrence pattern as original
- **FR-010**: Next occurrence due date MUST be calculated from original due date plus recurrence interval (not completion date)
- **FR-011**: For recurring tasks without due dates, next occurrence MUST be calculated from completion date plus interval
- **FR-012**: System MUST preserve both the completed task AND the new occurrence in history (no deletion of completed tasks)
- **FR-013**: Users MUST be able to edit recurrence pattern, affecting only future occurrences
- **FR-014**: Users MUST be able to stop recurrence, preventing future occurrence creation
- **FR-015**: When deleting recurring task, system MUST prompt for deletion scope: (1) This occurrence only, or (2) All future occurrences
- **FR-016**: System MUST skip past dates when calculating next occurrence (e.g., overdue weekly task creates occurrence for next valid future date)
- **FR-017**: System MUST display recurrence pattern clearly in task details (e.g., "Repeats: Every 7 days")

#### Reminders (FR-018 to FR-028)

- **FR-018**: Users MUST be able to add one or more reminders to tasks with due dates/times
- **FR-019**: Reminder format MUST support relative times: N minutes before, N hours before, N days before
- **FR-020**: System MUST store reminders with task metadata as reminder offset from due date/time
- **FR-021**: System MUST calculate absolute reminder time from due date/time and reminder offset
- **FR-022**: System MUST trigger reminders at calculated time by checking every minute (or reasonable interval)
- **FR-023**: System MUST send browser notification with task title and due time when reminder triggers (if supported)
- **FR-024**: If browser notifications not supported, system MUST log reminder to console with task details
- **FR-025**: System MUST cancel all reminders when task is marked complete
- **FR-026**: System MUST mark reminders as "sent" after triggering to prevent duplicate notifications
- **FR-027**: When recurring task creates next occurrence, reminders MUST be copied with times recalculated for new due date
- **FR-028**: System MUST warn user when adding reminder with time in the past (reminder will not trigger)

#### Data Model Extensions (FR-029 to FR-032)

- **FR-029**: Task entity MUST be extended with `due_time` field (string HH:MM format, optional, defaults to "23:59" if due_date set without time)
- **FR-030**: Task entity MUST be extended with `recurrence` field (object containing: pattern type ["none", "daily", "weekly", "custom"], interval value [integer])
- **FR-031**: Task entity MUST be extended with `reminders` field (list of reminder objects containing: offset_value [integer], offset_unit ["minutes", "hours", "days"], sent [boolean], sent_at [datetime, nullable])
- **FR-032**: Task entity MUST be extended with `parent_recurrence_id` field (integer, nullable, links recurring occurrences to track history)

### Key Entities

- **Task (Enhanced)**: Represents a todo item with time-aware scheduling and recurrence capabilities
  - **Existing attributes**: id, title, description, completed, priority, tags, due_date
  - **New attributes**:
    - `due_time`: Optional time component (HH:MM format), defaults to "23:59" if due_date is set
    - `recurrence`: Object storing recurrence pattern (type: "none"|"daily"|"weekly"|"custom", interval: integer)
    - `reminders`: List of reminder objects (offset_value, offset_unit, sent status, sent_at timestamp)
    - `parent_recurrence_id`: Links to original recurring task for history tracking (null for non-recurring)

- **Reminder**: Represents a scheduled notification for a task
  - **offset_value**: Numeric value (e.g., 15, 60, 1440)
  - **offset_unit**: Time unit ("minutes", "hours", "days")
  - **sent**: Boolean indicating if reminder notification was triggered
  - **sent_at**: Timestamp when reminder was sent (null if not sent)

- **Recurrence Pattern**: Configuration for automatic task rescheduling
  - **type**: "none" (default), "daily", "weekly", "custom"
  - **interval**: Integer value (e.g., 1 for daily, 7 for weekly, 3 for "every 3 days")

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create tasks with due dates including specific times (e.g., "2026-01-15 14:30") in under 30 seconds
- **SC-002**: Completing a recurring task creates the next occurrence automatically within 1 second
- **SC-003**: Reminders trigger within 1 minute of scheduled time (allowing for reasonable polling interval)
- **SC-004**: Browser notifications (when supported) display task title and due time clearly
- **SC-005**: Users can view past occurrences of recurring tasks, showing completion history
- **SC-006**: System handles at least 100 recurring tasks with different patterns without performance degradation
- **SC-007**: Users can set up recurring patterns (daily, weekly, custom) in under 1 minute
- **SC-008**: Reminders are successfully cancelled when tasks are completed (no notifications for completed tasks)
- **SC-009**: Time-based sorting orders tasks correctly by date and time (earlier times first within same date)
- **SC-010**: Users can add multiple reminders to a single task (e.g., 1 day before AND 15 minutes before)

## Assumptions

1. **Python Environment**: Application runs in Python 3.13+ environment with access to `datetime` and `threading` modules for time handling and reminder scheduling
2. **Browser Context**: For CLI application, "browser notifications" will be simulated through console output unless running in browser-capable environment
3. **Time Zone**: All times stored and displayed in local system time (no timezone conversion required for MVP)
4. **Reminder Polling**: System checks for due reminders every 60 seconds (1-minute granularity is acceptable)
5. **No Persistence**: Consistent with Basic and Intermediate levels, data remains in-memory only (no database)
6. **Recurrence Limits**: No limit on number of recurring occurrences that can be created (user manages cleanup)
7. **Time Format**: Use 24-hour clock (HH:MM) for consistency and unambiguous time specification
8. **No Calendar Integration**: System does not sync with external calendars (Google Calendar, Outlook, etc.)
9. **Single User**: No multi-user considerations for reminder scheduling (reminders are per-session)
10. **Backward Compatibility**: All new fields have sensible defaults to ensure existing Basic/Intermediate level tasks continue working

## Dependencies

- **Basic Level (Phase I)**: CRUD operations, task completion tracking
- **Intermediate Level (Phase II)**: Priority, tags, search, filter, sort capabilities
- **Python Standard Library**: `datetime` module for date/time handling, `threading` for background reminder checking
- **Console/Terminal**: For CLI-based notifications (logging output)
- **Optional - Browser Environment**: For actual browser notifications (if running in web context)

## Out of Scope

- UI styling, themes, or visual customization
- Multi-user collaboration or task sharing
- Payment processing or premium features
- AI-powered predictions or smart suggestions
- Integration with external calendar services (Google Calendar, Outlook, etc.)
- Timezone support or international date/time formatting
- Mobile push notifications (beyond browser notifications)
- Email or SMS reminder notifications
- Natural language processing for recurrence input (e.g., "every other Tuesday")
- Conflict detection for overlapping tasks
- Analytics or productivity metrics
