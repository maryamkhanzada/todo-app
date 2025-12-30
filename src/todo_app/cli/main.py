"""Main CLI interface for the Todo application.

This module provides the menu-driven command-line interface.
"""

from ..services.task_manager import TaskManager


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 33)
    print("    TODO APPLICATION - MENU")
    print("=" * 33)
    print("\n1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("6. Search Tasks")
    print("7. Filter Tasks")
    print("8. Sort Tasks")
    print("9. Manage Reminders")
    print("10. Manage Recurrence")
    print("11. Exit")
    print()


def get_status_string(completed: bool) -> str:
    """Convert completed boolean to status string.

    Args:
        completed: Boolean completion status.

    Returns:
        "Completed" if True, "Pending" if False.
    """
    return "Completed" if completed else "Pending"


def validate_task_id_input(task_id_input: str) -> tuple[bool, int | str]:
    """Validate and parse task ID input.

    Args:
        task_id_input: The string input from the user.

    Returns:
        Tuple of (success, result) where:
        - If valid: (True, task_id as int)
        - If invalid: (False, error_message as str)
    """
    try:
        task_id = int(task_id_input.strip())
        return (True, task_id)
    except ValueError:
        return (False, "Error: Task ID must be a number.")


def add_task_operation(task_manager: TaskManager):
    """Handle Add Task operation.

    Prompts user for title, description, priority, tags, due date, and due time, creates task, displays success message.

    Args:
        task_manager: TaskManager instance to add task to.
    """
    from datetime import datetime
    from ..utils.time_utils import parse_time

    print()
    title = input("Enter task title: ")
    description = input("Enter task description: ")

    # Prompt for priority
    priority_input = input("Enter priority (high/medium/low) or press Enter for default [medium]: ").strip()
    priority = priority_input if priority_input else 'medium'

    # Prompt for tags
    tags_input = input("Enter tags (comma-separated) or press Enter to skip: ").strip()
    tags = task_manager.parse_tags(tags_input)

    # Prompt for due date
    due_date = None
    due_time = None
    date_input = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip()
    if date_input:
        try:
            due_date = datetime.strptime(date_input, "%Y-%m-%d").date()

            # If date provided, prompt for time
            time_input = input("Enter due time (HH:MM) or press Enter for end of day [23:59]: ").strip()
            if time_input:
                due_time = parse_time(time_input)
                if not due_time:
                    print("\nError: Invalid time format. Use HH:MM in 24-hour format (e.g., '14:30', '09:00')")
                    return
        except ValueError:
            print("\nError: Invalid date format. Use YYYY-MM-DD (e.g., '2026-01-15')")
            return

    # Prompt for recurrence
    recurrence = None
    recurrence_input = input("Set recurrence? (yes/no) [no]: ").strip().lower()
    if recurrence_input == 'yes' or recurrence_input == 'y':
        rec_type_input = input("Recurrence type (daily/weekly/custom): ").strip().lower()
        if rec_type_input in ['daily', 'weekly']:
            recurrence = {"type": rec_type_input, "interval": 7 if rec_type_input == 'weekly' else 1}
        elif rec_type_input == 'custom':
            interval_input = input("Every N days (1-365): ").strip()
            try:
                interval = int(interval_input)
                if 1 <= interval <= 365:
                    recurrence = {"type": "custom", "interval": interval}
                else:
                    print("\nError: Interval must be between 1 and 365 days")
                    return
            except ValueError:
                print("\nError: Interval must be a number")
                return
        else:
            print("\nError: Recurrence type must be 'daily', 'weekly', or 'custom'")
            return

    try:
        task = task_manager.add_task(title, description, priority=priority, tags=tags, due_date=due_date, due_time=due_time, recurrence=recurrence)
        print(f"\nTask added successfully! Task ID: {task.id}")
        if due_date:
            time_display = due_time if due_time else "23:59"
            print(f"Due: {due_date.isoformat()} {time_display}")
        if recurrence and recurrence.get("type") != "none":
            if recurrence["type"] == "daily":
                print("Recurrence: Every day")
            elif recurrence["type"] == "weekly":
                print("Recurrence: Every 7 days (weekly)")
            elif recurrence["type"] == "custom":
                print(f"Recurrence: Every {recurrence['interval']} days")
    except ValueError as e:
        print(f"\nError: {e}")


def view_tasks_operation(task_manager: TaskManager, active_filters: dict = None, active_sort: dict = None):
    """Handle View Tasks operation.

    Displays all tasks (or filtered/sorted tasks) with formatted output or "No tasks found" message.

    Args:
        task_manager: TaskManager instance to retrieve tasks from.
        active_filters: Dictionary of active filters (optional).
        active_sort: Dictionary of active sort settings (optional).
    """
    # Get all tasks first
    all_tasks = task_manager.get_all_tasks()

    # Apply filters if any are active
    if active_filters:
        tasks = task_manager.filter_tasks(
            status=active_filters.get('status'),
            priority=active_filters.get('priority'),
            due_date_op=active_filters.get('due_date_op'),
            due_date_value=active_filters.get('due_date_value')
        )
    else:
        tasks = all_tasks

    # Apply sort if active
    if active_sort and 'sort_by' in active_sort:
        # Create a temporary TaskManager with filtered tasks to sort
        temp_manager = TaskManager()
        temp_manager.tasks = tasks
        tasks = temp_manager.sort_tasks(active_sort['sort_by'])

    if not tasks:
        print("\nNo tasks found.")
        if active_filters:
            print("(Try clearing filters to see all tasks)")
        return

    print("\n" + "=" * 50)
    print("                   ALL TASKS")
    print("=" * 50)

    for task in tasks:
        # Format priority display
        priority_display = task.priority.upper()

        # Format tags display
        tags_display = f"[{', '.join(task.tags)}]" if task.tags else ""

        # Format due date and time display
        if task.due_date:
            if task.due_time:
                due_display = f"{task.due_date.isoformat()} {task.due_time}"
            else:
                due_display = task.due_date.isoformat()
        else:
            due_display = "None"

        # Format recurrence display
        if task.recurrence and task.recurrence.get("type") != "none":
            rec_type = task.recurrence["type"]
            if rec_type == "daily":
                recurrence_display = "Repeats: Every day"
            elif rec_type == "weekly":
                recurrence_display = "Repeats: Every 7 days (weekly)"
            elif rec_type == "custom":
                interval = task.recurrence.get("interval", 1)
                recurrence_display = f"Repeats: Every {interval} days"
            else:
                recurrence_display = None
        else:
            recurrence_display = None

        print(f"\n[{task.id}] {task.title} [{priority_display}] {tags_display}")
        print(f"    Description: {task.description}")
        print(f"    Status: {get_status_string(task.completed)}")
        print(f"    Due: {due_display}")
        if recurrence_display:
            print(f"    {recurrence_display}")

        # Display reminders if any
        if task.reminders:
            from ..utils.time_utils import format_reminder_display
            print("    Reminders:")
            for reminder in task.reminders:
                reminder_display = format_reminder_display(reminder)
                print(f"      - {reminder_display}")

        print("\n" + "-" * 50)

    # Display filter and sort information if active
    if active_filters or active_sort:
        print()
        if active_filters:
            print(f"Showing {len(tasks)} of {len(all_tasks)} tasks")
            print("Active filters:")
            if 'status' in active_filters:
                status_text = "Completed" if active_filters['status'] else "Pending"
                print(f"  - Status: {status_text}")
            if 'priority' in active_filters:
                print(f"  - Priority: {active_filters['priority'].capitalize()}")
            if 'due_date_op' in active_filters and 'due_date_value' in active_filters:
                op_text = active_filters['due_date_op'].capitalize()
                date_text = active_filters['due_date_value'].isoformat()
                print(f"  - Due Date: {op_text} {date_text}")
            print("(Use 'Filter Tasks' menu option 4 to clear filters)")

        if active_sort and 'sort_by' in active_sort:
            sort_labels = {
                'due_date': 'Due Date',
                'priority': 'Priority (High → Medium → Low)',
                'alphabetical': 'Alphabetically (A-Z)'
            }
            sort_label = sort_labels.get(active_sort['sort_by'], active_sort['sort_by'])
            print(f"Active sort: {sort_label}")
            print("(Use 'Sort Tasks' menu option 4 to clear sort)")


def mark_complete_incomplete_operation(task_manager: TaskManager):
    """Handle Mark Complete/Incomplete operation.

    Prompts for task ID, toggles completion status, displays confirmation.

    Args:
        task_manager: TaskManager instance to update task in.
    """
    print()
    task_id_input = input("Enter task ID to toggle completion status: ").strip()

    # Validate numeric input
    try:
        task_id = int(task_id_input)
    except ValueError:
        print("\nError: Task ID must be a number.")
        return

    # Get the task to check current state before toggling
    task = task_manager.get_task_by_id(task_id)
    if not task:
        print(f"\nError: Task with ID {task_id} not found.")
        return

    # Toggle the completion status (returns next occurrence if recurring)
    next_occurrence = task_manager.toggle_task_completion(task_id)

    # Display confirmation based on new state
    if task.completed:
        print(f"\nTask marked as Completed!")

        # If recurring task, display next occurrence info
        if next_occurrence:
            print("\nNext occurrence created:")
            print(f"  Task ID: {next_occurrence.id}")
            print(f"  Title: {next_occurrence.title}")
            if next_occurrence.due_date:
                time_display = next_occurrence.due_time if next_occurrence.due_time else "23:59"
                print(f"  Due: {next_occurrence.due_date.isoformat()} {time_display}")
            if next_occurrence.recurrence and next_occurrence.recurrence.get("type") != "none":
                rec_type = next_occurrence.recurrence["type"]
                if rec_type == "daily":
                    print("  Recurrence: Every day")
                elif rec_type == "weekly":
                    print("  Recurrence: Every 7 days (weekly)")
                elif rec_type == "custom":
                    interval = next_occurrence.recurrence.get("interval", 1)
                    print(f"  Recurrence: Every {interval} days")
    else:
        print(f"\nTask marked as Pending!")


def update_task_operation(task_manager: TaskManager):
    """Handle Update Task operation.

    Prompts for task ID, displays current values, prompts for new values.
    Updates only fields where user provides new input.

    Args:
        task_manager: TaskManager instance to update task in.
    """
    print()
    task_id_input = input("Enter task ID to update: ").strip()

    # Validate numeric input
    try:
        task_id = int(task_id_input)
    except ValueError:
        print("\nError: Task ID must be a number.")
        return

    # Get the task and validate it exists
    task = task_manager.get_task_by_id(task_id)
    if not task:
        print(f"\nError: Task with ID {task_id} not found.")
        return

    # Display current values
    print(f"\nCurrent Title: {task.title}")
    print(f"Current Description: {task.description}")
    print(f"Current Priority: {task.priority}")
    tags_display = ', '.join(task.tags) if task.tags else "(no tags)"
    print(f"Current Tags: {tags_display}")

    # Display current due date and time
    if task.due_date:
        if task.due_time:
            print(f"Current Due: {task.due_date.isoformat()} {task.due_time}")
        else:
            print(f"Current Due: {task.due_date.isoformat()}")
    else:
        print("Current Due: None")

    # Prompt for new values
    print()
    new_title = input("Enter new title (or press Enter to keep current): ").strip()
    new_description = input("Enter new description (or press Enter to keep current): ").strip()
    new_priority = input("Enter new priority (or press Enter to keep current): ").strip()
    new_tags_input = input("Enter new tags (comma-separated, or press Enter to keep current): ").strip()

    # Prompt for due date and time
    from datetime import datetime
    from ..utils.time_utils import parse_time

    new_due_date = input("Enter new due date (YYYY-MM-DD, or press Enter to keep current, or 'none' to remove): ").strip()
    due_date_to_update = None
    due_time_to_update = None

    if new_due_date and new_due_date.lower() != 'none':
        try:
            due_date_to_update = datetime.strptime(new_due_date, "%Y-%m-%d").date()

            # Prompt for time if date provided
            new_due_time = input("Enter new due time (HH:MM, or press Enter to keep current, or 'none' to remove): ").strip()
            if new_due_time and new_due_time.lower() != 'none':
                due_time_to_update = parse_time(new_due_time)
                if not due_time_to_update:
                    print("\nError: Invalid time format. Use HH:MM in 24-hour format (e.g., '14:30', '09:00')")
                    return
        except ValueError:
            print("\nError: Invalid date format. Use YYYY-MM-DD (e.g., '2026-01-15')")
            return
    elif new_due_date and new_due_date.lower() == 'none':
        # User wants to remove due date (set to None)
        due_date_to_update = None

    # Determine which fields to update (only non-empty inputs)
    title_to_update = new_title if new_title else None
    description_to_update = new_description if new_description else None
    priority_to_update = new_priority if new_priority else None
    tags_to_update = task_manager.parse_tags(new_tags_input) if new_tags_input else None

    # Check if user provided at least one update
    if all(v is None for v in [title_to_update, description_to_update, priority_to_update, tags_to_update, due_date_to_update, due_time_to_update]):
        print("\nNo changes made. Task remains unchanged.")
        return

    # Update the task
    try:
        success = task_manager.update_task(
            task_id,
            title_to_update,
            description_to_update,
            priority_to_update,
            tags_to_update,
            due_date_to_update,
            due_time_to_update
        )
        if success:
            print("\nTask updated successfully!")
        else:
            print(f"\nError: Failed to update task {task_id}.")
    except ValueError as e:
        print(f"\nError: {e}")


def delete_task_operation(task_manager: TaskManager):
    """Handle Delete Task operation.

    Prompts for task ID, displays confirmation, deletes task if confirmed.

    Args:
        task_manager: TaskManager instance to delete task from.
    """
    print()
    task_id_input = input("Enter task ID to delete: ").strip()

    # Validate numeric input
    try:
        task_id = int(task_id_input)
    except ValueError:
        print("\nError: Task ID must be a number.")
        return

    # Get the task and validate it exists
    task = task_manager.get_task_by_id(task_id)
    if not task:
        print(f"\nError: Task with ID {task_id} not found.")
        return

    # Display task details for confirmation
    print(f"\nTask to delete:")
    print(f"  ID: {task.id}")
    print(f"  Title: {task.title}")
    print(f"  Description: {task.description}")

    # Check if this is a recurring task or recurring occurrence
    is_recurring = task.recurrence and task.recurrence.get("type") != "none"
    is_occurrence = task.parent_recurrence_id is not None

    # Handle recurrence scope if applicable
    delete_all_future = False
    if is_recurring or is_occurrence:
        print("\nThis is a recurring task. Delete:")
        print("  1. Only this occurrence")
        print("  2. This and all future occurrences")
        scope_choice = input("Choice (1/2): ").strip()

        if scope_choice == "2":
            delete_all_future = True
            print("\nConfirm: This will delete this task and all future occurrences.")
        elif scope_choice == "1":
            delete_all_future = False
            print("\nConfirm: This will delete only this occurrence.")
        else:
            print("\nInvalid choice. Deletion cancelled.")
            return

    # Confirmation prompt
    print()
    confirmation = input("Are you sure you want to proceed? (yes/y or no/n): ").strip().lower()

    # Handle confirmation response
    if confirmation in ['yes', 'y']:
        if delete_all_future:
            # Delete this task and all future uncompleted occurrences with same parent_recurrence_id
            root_id = task.parent_recurrence_id if task.parent_recurrence_id else task.id
            tasks_to_delete = [t for t in task_manager.tasks if (t.id == task_id or (t.parent_recurrence_id == root_id and not t.completed))]

            deleted_count = 0
            for t in tasks_to_delete:
                if task_manager.delete_task(t.id):
                    deleted_count += 1

            print(f"\n{deleted_count} task(s) deleted successfully!")
        else:
            # Delete only this task
            success = task_manager.delete_task(task_id)
            if success:
                print("\nTask deleted successfully!")
            else:
                print(f"\nError: Failed to delete task {task_id}.")
    elif confirmation in ['no', 'n']:
        print("\nDeletion cancelled.")
    else:
        print("\nInvalid response. Deletion cancelled.")


def search_tasks_operation(task_manager: TaskManager):
    """Handle Search Tasks operation.

    Prompts for keyword, searches tasks, displays results.

    Args:
        task_manager: TaskManager instance to search tasks in.
    """
    print()
    keyword = input("Enter search keyword: ").strip()

    try:
        results = task_manager.search_tasks(keyword)
        if results:
            print(f"\n=== Search Results for '{keyword}' ===\n")
            for task in results:
                # Format priority display
                priority_display = task.priority.upper()

                # Format tags display
                tags_display = f"[{', '.join(task.tags)}]" if task.tags else ""

                # Format due date display
                due_display = task.due_date.isoformat() if task.due_date else "None"

                print(f"[{task.id}] {task.title} [{priority_display}] {tags_display}")
                print(f"    Description: {task.description}")
                print(f"    Status: {get_status_string(task.completed)}")
                print(f"    Due: {due_display}\n")

            print(f"Found {len(results)} task(s)")
        else:
            print(f"\nNo tasks found matching '{keyword}'.")
    except ValueError as e:
        print(f"\nError: {e}")


def sort_tasks_operation(task_manager: TaskManager, active_sort: dict):
    """Handle Sort Tasks operation with sub-menu.

    Prompts user to select sort criterion, updates active_sort dict.

    Args:
        task_manager: TaskManager instance to sort tasks from.
        active_sort: Dictionary tracking current sort state.
    """
    print("\n" + "=" * 33)
    print("       SORT TASKS - MENU")
    print("=" * 33)
    print("\n1. Sort by Due Date")
    print("2. Sort by Priority")
    print("3. Sort Alphabetically")
    print("4. Clear Sort")
    print("5. Back to Main Menu")
    print()

    sort_choice = input("Enter your choice (1-5): ").strip()

    if sort_choice == "1":
        active_sort['sort_by'] = 'due_date'
        print("\nSort applied: Tasks sorted by Due Date (tasks without due dates appear last)")
    elif sort_choice == "2":
        active_sort['sort_by'] = 'priority'
        print("\nSort applied: Tasks sorted by Priority (High → Medium → Low)")
    elif sort_choice == "3":
        active_sort['sort_by'] = 'alphabetical'
        print("\nSort applied: Tasks sorted Alphabetically (A-Z)")
    elif sort_choice == "4":
        active_sort.clear()
        print("\nSort cleared.")
    elif sort_choice == "5":
        # Back to main menu
        return
    else:
        print("\nInvalid choice. Please enter a number between 1 and 5.")


def filter_tasks_operation(task_manager: TaskManager, active_filters: dict):
    """Handle Filter Tasks operation with sub-menu.

    Prompts user to select filter type, applies filter, updates active_filters dict.

    Args:
        task_manager: TaskManager instance to filter tasks from.
        active_filters: Dictionary tracking current filter state.
    """
    print("\n" + "=" * 33)
    print("      FILTER TASKS - MENU")
    print("=" * 33)
    print("\n1. Filter by Status")
    print("2. Filter by Priority")
    print("3. Filter by Due Date")
    print("4. Clear All Filters")
    print("5. Back to Main Menu")
    print()

    filter_choice = input("Enter your choice (1-5): ").strip()

    if filter_choice == "1":
        # Filter by status
        print("\nFilter by Status:")
        print("1. Completed")
        print("2. Pending")
        status_choice = input("Enter choice (1-2): ").strip()

        if status_choice == "1":
            active_filters['status'] = True
            print("\nFilter applied: Showing only Completed tasks")
        elif status_choice == "2":
            active_filters['status'] = False
            print("\nFilter applied: Showing only Pending tasks")
        else:
            print("\nInvalid choice. Filter not applied.")

    elif filter_choice == "2":
        # Filter by priority
        print("\nFilter by Priority:")
        print("1. High")
        print("2. Medium")
        print("3. Low")
        priority_choice = input("Enter choice (1-3): ").strip()

        if priority_choice == "1":
            active_filters['priority'] = 'high'
            print("\nFilter applied: Showing only High priority tasks")
        elif priority_choice == "2":
            active_filters['priority'] = 'medium'
            print("\nFilter applied: Showing only Medium priority tasks")
        elif priority_choice == "3":
            active_filters['priority'] = 'low'
            print("\nFilter applied: Showing only Low priority tasks")
        else:
            print("\nInvalid choice. Filter not applied.")

    elif filter_choice == "3":
        # Filter by due date
        from datetime import datetime

        print("\nFilter by Due Date:")
        print("1. Before a date")
        print("2. After a date")
        print("3. On a specific date")
        date_op_choice = input("Enter choice (1-3): ").strip()

        date_input = input("Enter date (YYYY-MM-DD): ").strip()

        try:
            due_date_value = datetime.strptime(date_input, "%Y-%m-%d").date()

            if date_op_choice == "1":
                active_filters['due_date_op'] = 'before'
                active_filters['due_date_value'] = due_date_value
                print(f"\nFilter applied: Showing tasks due before {date_input}")
            elif date_op_choice == "2":
                active_filters['due_date_op'] = 'after'
                active_filters['due_date_value'] = due_date_value
                print(f"\nFilter applied: Showing tasks due after {date_input}")
            elif date_op_choice == "3":
                active_filters['due_date_op'] = 'on'
                active_filters['due_date_value'] = due_date_value
                print(f"\nFilter applied: Showing tasks due on {date_input}")
            else:
                print("\nInvalid choice. Filter not applied.")
        except ValueError:
            print("\nError: Invalid date format. Use YYYY-MM-DD (e.g., 2025-12-31)")

    elif filter_choice == "4":
        # Clear all filters
        active_filters.clear()
        print("\nAll filters cleared.")

    elif filter_choice == "5":
        # Back to main menu
        return

    else:
        print("\nInvalid choice. Please enter a number between 1 and 5.")


def manage_reminders_operation(task_manager: TaskManager):
    """Handle Manage Reminders operation.

    Provides sub-menu for adding, removing, and viewing reminders for tasks.

    Args:
        task_manager: TaskManager instance to manage reminders for.
    """
    from ..utils.time_utils import parse_reminder, format_reminder_display

    print("\n" + "=" * 40)
    print("         MANAGE REMINDERS")
    print("=" * 40)
    print("\n1. Add Reminder to Task")
    print("2. Remove Reminder from Task")
    print("3. View All Reminders")
    print("4. Back to Main Menu")
    print()

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
        # Add Reminder
        print()
        task_id_input = input("Enter task ID to add reminder: ").strip()

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("\nError: Task ID must be a number.")
            return

        task = task_manager.get_task_by_id(task_id)
        if not task:
            print(f"\nError: Task with ID {task_id} not found.")
            return

        # Check if task has due date
        if not task.due_date:
            print("\nError: Task must have a due date to set reminders.")
            return

        print(f"\nTask: {task.title}")
        print("Enter reminder (e.g., '15 minutes', '1 hour', '2 days'):")
        reminder_input = input("Reminder: ").strip()

        reminder = parse_reminder(reminder_input)
        if not reminder:
            print("\nError: Invalid reminder format. Use 'N minutes/hours/days'")
            return

        # Add reminder to task
        task.reminders.append(reminder)
        print(f"\nReminder added successfully!")
        print(f"Will remind you {reminder['offset_value']} {reminder['offset_unit']} before due time")

    elif choice == "2":
        # Remove Reminder
        print()
        task_id_input = input("Enter task ID to remove reminder from: ").strip()

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("\nError: Task ID must be a number.")
            return

        task = task_manager.get_task_by_id(task_id)
        if not task:
            print(f"\nError: Task with ID {task_id} not found.")
            return

        if not task.reminders:
            print("\nThis task has no reminders.")
            return

        # Display reminders
        print(f"\nTask: {task.title}")
        print("\nCurrent Reminders:")
        for i, reminder in enumerate(task.reminders, 1):
            display = format_reminder_display(reminder)
            print(f"  {i}. {display}")

        print()
        reminder_index_input = input("Enter reminder number to remove: ").strip()

        try:
            reminder_index = int(reminder_index_input) - 1
            if 0 <= reminder_index < len(task.reminders):
                removed = task.reminders.pop(reminder_index)
                print(f"\nReminder removed successfully!")
            else:
                print(f"\nError: Invalid reminder number.")
        except ValueError:
            print("\nError: Reminder number must be a number.")

    elif choice == "3":
        # View All Reminders
        print("\n" + "=" * 60)
        print("              ALL TASK REMINDERS")
        print("=" * 60)

        found_any = False
        for task in task_manager.get_all_tasks():
            if task.reminders and not task.completed:
                found_any = True
                print(f"\n[{task.id}] {task.title}")
                if task.due_date:
                    time_display = task.due_time if task.due_time else "23:59"
                    print(f"    Due: {task.due_date.isoformat()} {time_display}")
                print("    Reminders:")
                for reminder in task.reminders:
                    display = format_reminder_display(reminder)
                    print(f"      - {display}")

        if not found_any:
            print("\nNo active reminders found.")

        print("\n" + "-" * 60)

    elif choice == "4":
        # Back to Main Menu
        return

    else:
        print("\nInvalid choice. Please enter a number between 1 and 4.")


def manage_recurrence_operation(task_manager: TaskManager):
    """Handle Manage Recurrence operation.

    Provides sub-menu for setting, editing, stopping recurrence patterns and viewing history.

    Args:
        task_manager: TaskManager instance to manage recurrence for.
    """
    print("\n" + "=" * 40)
    print("       MANAGE RECURRENCE")
    print("=" * 40)
    print("\n1. Set/Edit Recurrence Pattern")
    print("2. Stop Recurrence")
    print("3. View Occurrence History")
    print("4. Back to Main Menu")
    print()

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
        # Set/Edit Recurrence Pattern
        print()
        task_id_input = input("Enter task ID to set/edit recurrence: ").strip()

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("\nError: Task ID must be a number.")
            return

        task = task_manager.get_task_by_id(task_id)
        if not task:
            print(f"\nError: Task with ID {task_id} not found.")
            return

        # Check if task has due date
        if not task.due_date:
            print("\nError: Task must have a due date to set recurrence.")
            return

        # Display current recurrence
        print(f"\nTask: {task.title}")
        if task.recurrence and task.recurrence.get("type") != "none":
            rec_type = task.recurrence["type"]
            if rec_type == "daily":
                print("Current Recurrence: Every day")
            elif rec_type == "weekly":
                print("Current Recurrence: Every 7 days (weekly)")
            elif rec_type == "custom":
                interval = task.recurrence.get("interval", 1)
                print(f"Current Recurrence: Every {interval} days")
        else:
            print("Current Recurrence: None")

        # Confirm if editing existing recurrence
        if task.recurrence and task.recurrence.get("type") != "none":
            print("\n⚠️  WARNING: Changing recurrence will only affect future occurrences.")
            print("Past completed occurrences will retain their original pattern.")
            confirm = input("Continue? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("\nOperation cancelled.")
                return

        # Prompt for new recurrence
        print("\nNew recurrence type:")
        print("  1. Daily (every day)")
        print("  2. Weekly (every 7 days)")
        print("  3. Custom (every N days)")
        print("  4. None (stop recurrence)")
        rec_choice = input("Choice (1-4): ").strip()

        if rec_choice == "1":
            new_recurrence = {"type": "daily", "interval": 1}
            print("\nRecurrence set to: Every day")
        elif rec_choice == "2":
            new_recurrence = {"type": "weekly", "interval": 7}
            print("\nRecurrence set to: Every 7 days (weekly)")
        elif rec_choice == "3":
            interval_input = input("Every N days (1-365): ").strip()
            try:
                interval = int(interval_input)
                if 1 <= interval <= 365:
                    new_recurrence = {"type": "custom", "interval": interval}
                    print(f"\nRecurrence set to: Every {interval} days")
                else:
                    print("\nError: Interval must be between 1 and 365 days")
                    return
            except ValueError:
                print("\nError: Interval must be a number")
                return
        elif rec_choice == "4":
            new_recurrence = {"type": "none", "interval": 1}
            print("\nRecurrence stopped.")
        else:
            print("\nError: Invalid choice")
            return

        # Update task recurrence
        task.recurrence = task._validate_recurrence(new_recurrence)
        print("Recurrence pattern updated successfully!")

    elif choice == "2":
        # Stop Recurrence
        print()
        task_id_input = input("Enter task ID to stop recurrence: ").strip()

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("\nError: Task ID must be a number.")
            return

        task = task_manager.get_task_by_id(task_id)
        if not task:
            print(f"\nError: Task with ID {task_id} not found.")
            return

        # Check if task has recurrence
        if not task.recurrence or task.recurrence.get("type") == "none":
            print("\nThis task has no active recurrence.")
            return

        # Display current recurrence
        print(f"\nTask: {task.title}")
        rec_type = task.recurrence["type"]
        if rec_type == "daily":
            print("Current Recurrence: Every day")
        elif rec_type == "weekly":
            print("Current Recurrence: Every 7 days (weekly)")
        elif rec_type == "custom":
            interval = task.recurrence.get("interval", 1)
            print(f"Current Recurrence: Every {interval} days")

        # Confirmation
        print("\n⚠️  WARNING: Stopping recurrence will prevent future occurrences from being created.")
        print("Completed occurrences will remain in your task history.")
        confirm = input("Are you sure you want to stop recurrence? (yes/no): ").strip().lower()

        if confirm in ['yes', 'y']:
            task.recurrence = {"type": "none", "interval": 1}
            print("\nRecurrence stopped successfully!")
        else:
            print("\nOperation cancelled.")

    elif choice == "3":
        # View Occurrence History
        print()
        task_id_input = input("Enter task ID to view occurrence history: ").strip()

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("\nError: Task ID must be a number.")
            return

        task = task_manager.get_task_by_id(task_id)
        if not task:
            print(f"\nError: Task with ID {task_id} not found.")
            return

        # Get occurrence history
        occurrences = task_manager.get_occurrence_history(task)

        if len(occurrences) <= 1:
            print(f"\nTask '{task.title}' has no occurrence history.")
            print("(This may be a non-recurring task or the first occurrence)")
            return

        # Display history
        print("\n" + "=" * 60)
        print(f"   OCCURRENCE HISTORY: {task.title}")
        print("=" * 60)

        for i, occurrence in enumerate(occurrences, 1):
            status = "✓ Completed" if occurrence.completed else "○ Pending"
            if occurrence.due_date:
                time_display = occurrence.due_time if occurrence.due_time else "23:59"
                due_str = f"{occurrence.due_date.isoformat()} {time_display}"
            else:
                due_str = "No due date"

            print(f"\n{i}. [{occurrence.id}] {status}")
            print(f"   Due: {due_str}")
            if occurrence.recurrence and occurrence.recurrence.get("type") != "none":
                rec_type = occurrence.recurrence["type"]
                if rec_type == "daily":
                    print("   Recurrence: Every day")
                elif rec_type == "weekly":
                    print("   Recurrence: Every 7 days")
                elif rec_type == "custom":
                    interval = occurrence.recurrence.get("interval", 1)
                    print(f"   Recurrence: Every {interval} days")

        print("\n" + "-" * 60)
        print(f"Total occurrences: {len(occurrences)}")

    elif choice == "4":
        # Back to Main Menu
        return

    else:
        print("\nInvalid choice. Please enter a number between 1 and 4.")


def main():
    """Main entry point for the Todo application."""
    from ..services.reminder_service import ReminderService

    task_manager = TaskManager()
    active_filters = {}  # Track current filter state
    active_sort = {}  # Track current sort state

    # Create and start ReminderService
    reminder_service = ReminderService(task_manager)
    reminder_service.start()

    try:
        while True:
            display_menu()

            try:
                choice = input("Enter your choice (1-11): ").strip()

                if choice == "1":
                    # Add Task operation
                    add_task_operation(task_manager)
                elif choice == "2":
                    # View Tasks operation
                    view_tasks_operation(task_manager, active_filters, active_sort)
                elif choice == "3":
                    # Update Task operation
                    update_task_operation(task_manager)
                elif choice == "4":
                    # Delete Task operation
                    delete_task_operation(task_manager)
                elif choice == "5":
                    # Mark Complete/Incomplete operation
                    mark_complete_incomplete_operation(task_manager)
                elif choice == "6":
                    # Search Tasks operation
                    search_tasks_operation(task_manager)
                elif choice == "7":
                    # Filter Tasks operation
                    filter_tasks_operation(task_manager, active_filters)
                elif choice == "8":
                    # Sort Tasks operation
                    sort_tasks_operation(task_manager, active_sort)
                elif choice == "9":
                    # Manage Reminders operation
                    manage_reminders_operation(task_manager)
                elif choice == "10":
                    # Manage Recurrence operation
                    manage_recurrence_operation(task_manager)
                elif choice == "11":
                    # Exit operation
                    print("\nGoodbye! Thank you for using the Todo Application.")
                    break
                else:
                    # Invalid menu choice
                    print("\nInvalid choice. Please enter a number between 1 and 11.")

            except KeyboardInterrupt:
                print("\n\nGoodbye! Thank you for using the Todo Application.")
                break
            except EOFError:
                print("\n\nGoodbye! Thank you for using the Todo Application.")
                break

    finally:
        # Stop ReminderService on exit
        reminder_service.stop()


if __name__ == "__main__":
    main()
