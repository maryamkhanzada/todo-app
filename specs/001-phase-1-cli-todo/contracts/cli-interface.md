# CLI Interface Contract: Phase I - In-Memory CLI Todo Application

**Feature**: 001-phase-1-cli-todo
**Date**: 2025-12-27
**Version**: 1.0

## Overview

This document defines the exact interface contract for the CLI (Command-Line Interface) of the Phase I Todo application. It specifies all user interactions, menu structures, prompts, input formats, output formats, and error messages.

## Interface Type

**Type**: Menu-driven text-based CLI
**Platform**: Cross-platform terminal/console (Windows, macOS, Linux)
**Interaction Model**: Synchronous, blocking input/output
**Session**: Single-session (no persistence between runs)

## Main Menu

The main menu is the central navigation point and must be displayed after application startup and after every operation.

### Menu Display Format

```
=================================
    TODO APPLICATION - MENU
=================================

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter your choice (1-6):
```

### Menu Behavior

- Menu must be displayed immediately after application startup (within 5 seconds per SC-006)
- Menu must be redisplayed after every operation completes (per FR-010)
- User must enter a number from 1-6
- Invalid input (non-numeric, out of range) must display error and redisplay menu (per FR-014)

### Invalid Input Handling

**Input**: Any value not in range 1-6 (e.g., "7", "abc", "0", "-1", empty input)

**Output**:
```
Invalid choice. Please enter a number between 1 and 6.

[Main menu redisplayed]
```

---

## Operation 1: Add Task

**Menu Choice**: 1

### Flow

1. User selects option 1 from main menu
2. System prompts for task title
3. User enters title
4. System prompts for task description
5. User enters description
6. System creates task with auto-incremented ID and status "Pending"
7. System displays success message with task ID
8. System returns to main menu

### Prompts and Inputs

**Prompt 1 - Title**:
```
Enter task title:
```

**User Input**: String (any non-empty text)

**Prompt 2 - Description**:
```
Enter task description:
```

**User Input**: String (any non-empty text)

### Success Output

```
Task added successfully! Task ID: [ID]

[Main menu redisplayed]
```

Where `[ID]` is the auto-generated task ID (e.g., "Task added successfully! Task ID: 1")

### Edge Cases

**Empty Title**:
- **Input**: User presses Enter without typing anything
- **Output**: Accept empty input (specification does not enforce non-empty, implementation may choose to allow)

**Empty Description**:
- **Input**: User presses Enter without typing anything
- **Output**: Accept empty input (specification does not enforce non-empty, implementation may choose to allow)

**Very Long Title/Description**:
- **Input**: User enters 10,000+ character string
- **Output**: Accept input (no maximum length specified, handle gracefully)

### Requirements Mapping

- **FR-001**: Allow users to add tasks with title and description
- **FR-002**: Assign unique, auto-incremented ID
- **FR-003**: Set default status to "Pending"

---

## Operation 2: View Tasks

**Menu Choice**: 2

### Flow

1. User selects option 2 from main menu
2. System retrieves all tasks
3. If tasks exist, system displays all tasks in formatted list
4. If no tasks exist, system displays "no tasks" message
5. System returns to main menu

### Output Format - With Tasks

```
=================================
         ALL TASKS
=================================

Task ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Pending

---------------------------------

Task ID: 2
Title: Finish report
Description: Complete Q4 financial report
Status: Completed

---------------------------------

[Main menu redisplayed]
```

### Output Format - No Tasks

```
No tasks found.

[Main menu redisplayed]
```

### Display Requirements

- Each task must show: ID, Title, Description, Status (per FR-004)
- Status must display as "Pending" or "Completed" (not True/False)
- Tasks must be separated by a visual delimiter (e.g., dashed line)
- Display must be "clear and readable" (per FR-005)
- Response time must be under 1 second for up to 100 tasks (per SC-002)

### Requirements Mapping

- **FR-004**: Allow viewing all tasks with all fields
- **FR-005**: Display in clear, readable format

---

## Operation 3: Update Task

**Menu Choice**: 3

### Flow

1. User selects option 3 from main menu
2. System prompts for task ID
3. User enters task ID
4. System validates ID exists
5. If invalid ID, display error and return to menu
6. If valid ID, display current task details
7. System prompts for new title (optional update)
8. User enters new title or presses Enter to skip
9. System prompts for new description (optional update)
10. User enters new description or presses Enter to skip
11. System updates task fields (only if new values provided)
12. System displays success message
13. System returns to main menu

### Prompts and Inputs

**Prompt 1 - Task ID**:
```
Enter task ID to update:
```

**User Input**: Integer

**Prompt 2 - New Title**:
```
Current Title: [current title]
Enter new title (or press Enter to keep current):
```

**User Input**: String or Enter (empty)

**Prompt 3 - New Description**:
```
Current Description: [current description]
Enter new description (or press Enter to keep current):
```

**User Input**: String or Enter (empty)

### Success Output

```
Task updated successfully!

[Main menu redisplayed]
```

### Error Output - Invalid ID

**Input**: Non-existent task ID (e.g., "999" when only 5 tasks exist)

**Output**:
```
Error: Task ID [ID] not found.

[Main menu redisplayed]
```

### Error Output - Non-Numeric ID

**Input**: Non-numeric value (e.g., "abc")

**Output**:
```
Error: Invalid task ID. Please enter a number.

[Main menu redisplayed]
```

### Update Behavior

- If user presses Enter without typing, keep current value (no update)
- If user enters new value, update that field
- Both fields can be updated in same operation
- Only title and description can be updated (not ID or completed status)

### Requirements Mapping

- **FR-006**: Allow updating title and description by ID
- **FR-009**: Display error for invalid IDs without crashing
- **FR-014**: Gracefully handle invalid input

---

## Operation 4: Delete Task

**Menu Choice**: 4

### Flow

1. User selects option 4 from main menu
2. System prompts for task ID
3. User enters task ID
4. System validates ID exists
5. If invalid ID, display error and return to menu
6. If valid ID, display confirmation prompt
7. User confirms or cancels deletion
8. If confirmed, system deletes task
9. System displays success/cancellation message
10. System returns to main menu

### Prompts and Inputs

**Prompt 1 - Task ID**:
```
Enter task ID to delete:
```

**User Input**: Integer

**Prompt 2 - Confirmation**:
```
Are you sure you want to delete this task? (yes/no):
```

**User Input**: "yes", "y", "no", "n" (case-insensitive)

### Success Output - Confirmed

**Input**: User enters "yes" or "y"

**Output**:
```
Task deleted successfully!

[Main menu redisplayed]
```

### Success Output - Cancelled

**Input**: User enters "no" or "n"

**Output**:
```
Deletion cancelled.

[Main menu redisplayed]
```

### Error Output - Invalid ID

**Input**: Non-existent task ID

**Output**:
```
Error: Task ID [ID] not found.

[Main menu redisplayed]
```

### Error Output - Non-Numeric ID

**Input**: Non-numeric value

**Output**:
```
Error: Invalid task ID. Please enter a number.

[Main menu redisplayed]
```

### Requirements Mapping

- **FR-007**: Allow deleting tasks by ID with confirmation
- **FR-009**: Handle invalid IDs gracefully (no crash)

---

## Operation 5: Mark Complete/Incomplete

**Menu Choice**: 5

### Flow

1. User selects option 5 from main menu
2. System prompts for task ID
3. User enters task ID
4. System validates ID exists
5. If invalid ID, display error and return to menu
6. If valid ID, system retrieves current status
7. System toggles status (Pending → Completed or Completed → Pending)
8. System displays success message showing new status
9. System returns to main menu

### Prompts and Inputs

**Prompt 1 - Task ID**:
```
Enter task ID to mark complete/incomplete:
```

**User Input**: Integer

### Success Output - Marked Complete

**Input**: Task with ID has status "Pending"

**Output**:
```
Task marked as Completed!

[Main menu redisplayed]
```

### Success Output - Marked Incomplete

**Input**: Task with ID has status "Completed"

**Output**:
```
Task marked as Pending!

[Main menu redisplayed]
```

### Error Output - Invalid ID

**Input**: Non-existent task ID

**Output**:
```
Error: Task ID [ID] not found.

[Main menu redisplayed]
```

### Error Output - Non-Numeric ID

**Input**: Non-numeric value

**Output**:
```
Error: Invalid task ID. Please enter a number.

[Main menu redisplayed]
```

### Status Toggle Behavior

- Status is toggled automatically based on current state
- User does not choose whether to mark complete or incomplete
- System determines action based on current status
- Change must be visible immediately on next "View Tasks" (per SC-005)

### Requirements Mapping

- **FR-008**: Allow marking tasks as Completed or reverting to Pending
- **FR-009**: Handle invalid IDs without crashing
- **SC-005**: Status changes immediately visible

---

## Operation 6: Exit

**Menu Choice**: 6

### Flow

1. User selects option 6 from main menu
2. System displays exit message
3. Application terminates

### Output

```
Goodbye! Thank you for using the Todo Application.
```

### Requirements Mapping

- **FR-012**: Allow users to exit safely at any time

---

## Error Handling Standards

All error scenarios must adhere to these standards:

1. **No Crashes**: Application must never crash due to user input (per FR-009, SC-003, SC-004)
2. **Clear Messages**: Error messages must clearly state the problem (per Constitution VIII)
3. **Recovery**: After error, application must return to main menu (per FR-010)
4. **Prompt Re-entry**: Invalid input should allow user to try again (per FR-014)

### Standard Error Format

```
Error: [Clear description of the problem]

[Main menu redisplayed]
```

---

## Performance Contracts

These performance targets are contractual obligations:

| Operation | Maximum Time | Source |
|-----------|--------------|--------|
| Application startup → Main menu | 5 seconds | SC-006 |
| View Tasks (up to 100 tasks) | 1 second | SC-002 |
| Add Task (user input → success message) | 30 seconds | SC-001 |
| Update Task | 2 seconds | SC-007 |
| Delete Task | 2 seconds | SC-007 |
| Mark Complete/Incomplete | 2 seconds | SC-007 |

**Note**: SC-001 (30 seconds for task creation) includes user input time. The system processing time should be near-instant (< 1 second).

---

## Session Behavior

**Session Start**: Application launches and displays main menu
**Session End**: User selects "Exit" or forcibly terminates application
**Persistence**: All data is lost when session ends (no persistence between sessions per FR-013)

---

## Interface Evolution

This CLI interface is designed for **Phase I only**. Future phases may introduce:

- **Phase II**: Enhanced CLI with colors, formatting, search/filter
- **Phase III**: RESTful API for programmatic access
- **Phase IV**: Web interface, mobile apps

The simple, menu-driven text interface ensures:
1. Easy implementation in Phase I (constitutional simplicity requirement)
2. Clear contract for testing (deterministic behavior per Constitution VIII)
3. Foundation for future interface additions (evolution guarantee per Constitution IX)
