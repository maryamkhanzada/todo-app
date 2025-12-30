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
    print("9. Exit")
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

    Prompts user for title, description, priority, and tags, creates task, displays success message.

    Args:
        task_manager: TaskManager instance to add task to.
    """
    print()
    title = input("Enter task title: ")
    description = input("Enter task description: ")

    # Prompt for priority
    priority_input = input("Enter priority (high/medium/low) or press Enter for default [medium]: ").strip()
    priority = priority_input if priority_input else 'medium'

    # Prompt for tags
    tags_input = input("Enter tags (comma-separated) or press Enter to skip: ").strip()
    tags = task_manager.parse_tags(tags_input)

    try:
        task = task_manager.add_task(title, description, priority=priority, tags=tags)
        print(f"\nTask added successfully! Task ID: {task.id}")
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

        # Format due date display
        due_display = task.due_date.isoformat() if task.due_date else "None"

        print(f"\n[{task.id}] {task.title} [{priority_display}] {tags_display}")
        print(f"    Description: {task.description}")
        print(f"    Status: {get_status_string(task.completed)}")
        print(f"    Due: {due_display}")
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

    # Toggle the completion status
    success = task_manager.toggle_task_completion(task_id)

    if success:
        # Display confirmation based on new state
        new_status = get_status_string(task.completed)
        if task.completed:
            print(f"\nTask marked as Completed!")
        else:
            print(f"\nTask marked as Pending!")
    else:
        print(f"\nError: Failed to update task {task_id}.")


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

    # Prompt for new values
    print()
    new_title = input("Enter new title (or press Enter to keep current): ").strip()
    new_description = input("Enter new description (or press Enter to keep current): ").strip()
    new_priority = input("Enter new priority (or press Enter to keep current): ").strip()
    new_tags_input = input("Enter new tags (comma-separated, or press Enter to keep current): ").strip()

    # Determine which fields to update (only non-empty inputs)
    title_to_update = new_title if new_title else None
    description_to_update = new_description if new_description else None
    priority_to_update = new_priority if new_priority else None
    tags_to_update = task_manager.parse_tags(new_tags_input) if new_tags_input else None

    # Check if user provided at least one update
    if all(v is None for v in [title_to_update, description_to_update, priority_to_update, tags_to_update]):
        print("\nNo changes made. Task remains unchanged.")
        return

    # Update the task
    try:
        success = task_manager.update_task(
            task_id,
            title_to_update,
            description_to_update,
            priority_to_update,
            tags_to_update
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

    # Confirmation prompt
    print()
    confirmation = input("Are you sure you want to delete this task? (yes/y or no/n): ").strip().lower()

    # Handle confirmation response
    if confirmation in ['yes', 'y']:
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


def main():
    """Main entry point for the Todo application."""
    task_manager = TaskManager()
    active_filters = {}  # Track current filter state
    active_sort = {}  # Track current sort state

    while True:
        display_menu()

        try:
            choice = input("Enter your choice (1-9): ").strip()

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
                # Exit operation
                print("\nGoodbye! Thank you for using the Todo Application.")
                break
            else:
                # Invalid menu choice
                print("\nInvalid choice. Please enter a number between 1 and 9.")

        except KeyboardInterrupt:
            print("\n\nGoodbye! Thank you for using the Todo Application.")
            break
        except EOFError:
            print("\n\nGoodbye! Thank you for using the Todo Application.")
            break


if __name__ == "__main__":
    main()
