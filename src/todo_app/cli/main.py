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
    print("6. Exit")
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

    Prompts user for title and description, creates task, displays success message.

    Args:
        task_manager: TaskManager instance to add task to.
    """
    print()
    title = input("Enter task title: ")
    description = input("Enter task description: ")

    task = task_manager.add_task(title, description)
    print(f"\nTask added successfully! Task ID: {task.id}")


def view_tasks_operation(task_manager: TaskManager):
    """Handle View Tasks operation.

    Displays all tasks with formatted output or "No tasks found" message.

    Args:
        task_manager: TaskManager instance to retrieve tasks from.
    """
    tasks = task_manager.get_all_tasks()

    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n" + "=" * 33)
    print("         ALL TASKS")
    print("=" * 33)

    for task in tasks:
        print(f"\nTask ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Description: {task.description}")
        print(f"Status: {get_status_string(task.completed)}")
        print("\n" + "-" * 33)


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

    # Prompt for new title
    print()
    new_title = input("Enter new title (or press Enter to keep current): ").strip()

    # Prompt for new description
    new_description = input("Enter new description (or press Enter to keep current): ").strip()

    # Determine which fields to update (only non-empty inputs)
    title_to_update = new_title if new_title else None
    description_to_update = new_description if new_description else None

    # Check if user provided at least one update
    if title_to_update is None and description_to_update is None:
        print("\nNo changes made. Task remains unchanged.")
        return

    # Update the task
    success = task_manager.update_task(task_id, title_to_update, description_to_update)

    if success:
        print("\nTask updated successfully!")
    else:
        print(f"\nError: Failed to update task {task_id}.")


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


def main():
    """Main entry point for the Todo application."""
    task_manager = TaskManager()

    while True:
        display_menu()

        try:
            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                # Add Task operation
                add_task_operation(task_manager)
            elif choice == "2":
                # View Tasks operation
                view_tasks_operation(task_manager)
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
                # Exit operation
                print("\nGoodbye! Thank you for using the Todo Application.")
                break
            else:
                # Invalid menu choice
                print("\nInvalid choice. Please enter a number between 1 and 6.")

        except KeyboardInterrupt:
            print("\n\nGoodbye! Thank you for using the Todo Application.")
            break
        except EOFError:
            print("\n\nGoodbye! Thank you for using the Todo Application.")
            break


if __name__ == "__main__":
    main()
