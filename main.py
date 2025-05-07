#This is a maintenance Tracker for logging and resolving issues 

import csv
import datetime
import uuid
import os

CSV_FILE = 'tasks.csv'
FIELDNAMES = ['task_id', 'location', 'description', 'reported_date', 'priority', 'status']
STATUS_OPTIONS = ["Reported", "In Progress", "Completed"]
PRIORITY_OPTIONS = ["High", "Medium", "Low"]

def initialize_csv():
    """Creates the CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
        print(f"'{CSV_FILE}' created successfully.")

def load_tasks():
    """Loads tasks from the CSV file."""
    initialize_csv() # Ensure file exists
    tasks = []
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tasks.append(row)
    except FileNotFoundError:
        # This case is handled by initialize_csv, but good practice
        pass
    return tasks

def save_tasks(tasks):
    """Saves all tasks to the CSV file."""
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(tasks)

def generate_task_id():
    """Generates a unique task ID."""
    return str(uuid.uuid4()) # Using UUID for robust uniqueness

def add_task():
    """Adds a new maintenance task."""
    print("\n--- Add New Task ---")
    location = input("Enter task location (e.g., Room 101, Lobby): ").strip()
    description = input("Enter task description: ").strip()

    while True:
        priority_input = input(f"Enter task priority ({', '.join(PRIORITY_OPTIONS)}): ").strip().capitalize()
        if priority_input in PRIORITY_OPTIONS:
            priority = priority_input
            break
        else:
            print(f"Invalid priority. Please choose from: {', '.join(PRIORITY_OPTIONS)}")

    task_id = generate_task_id()
    reported_date = datetime.date.today().isoformat()
    status = "Reported" # Default status for new tasks

    new_task = {
        'task_id': task_id,
        'location': location,
        'description': description,
        'reported_date': reported_date,
        'priority': priority,
        'status': status
    }

    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"\nTask '{description}' added successfully with ID: {task_id}")

def view_tasks_list(tasks_to_display, title="--- All Tasks ---"):
    """Helper function to display a list of tasks."""
    print(f"\n{title}")
    if not tasks_to_display:
        print("No tasks to display.")
        return

    # Print headers
    header_string = "{:<38} {:<20} {:<40} {:<15} {:<10} {:<15}".format(*FIELDNAMES)
    print(header_string)
    print("-" * len(header_string))

    # Print tasks
    for task in tasks_to_display:
        print("{:<38} {:<20} {:<40} {:<15} {:<10} {:<15}".format(
            task.get('task_id', 'N/A'),
            task.get('location', 'N/A'),
            task.get('description', 'N/A'),
            task.get('reported_date', 'N/A'),
            task.get('priority', 'N/A'),
            task.get('status', 'N/A')
        ))
    print("-" * len(header_string))


def view_all_tasks():
    """Views all tasks."""
    tasks = load_tasks()
    view_tasks_list(tasks, title="--- All Maintenance Tasks ---")

def view_open_tasks():
    """Views all tasks that are not 'Completed'."""
    all_tasks = load_tasks()
    open_tasks = [task for task in all_tasks if task.get('status') != "Completed"]
    view_tasks_list(open_tasks, title="--- Open Maintenance Tasks ---")

def update_task_status():
    """Updates the status of an existing task."""
    print("\n--- Update Task Status ---")
    tasks = load_tasks()
    if not tasks:
        print("No tasks available to update.")
        return

    view_tasks_list(tasks, "Available Tasks to Update") # Show tasks so user can pick ID
    task_id_to_update = input("Enter the task ID of the task you want to update: ").strip()

    task_found = False
    for task in tasks:
        if task.get('task_id') == task_id_to_update:
            task_found = True
            print(f"\nUpdating Task ID: {task_id_to_update}")
            print(f"Current Status: {task.get('status')}")

            while True:
                new_status = input(f"Enter new status ({', '.join(STATUS_OPTIONS)}): ").strip().capitalize()
                if new_status in STATUS_OPTIONS:
                    task['status'] = new_status
                    save_tasks(tasks)
                    print(f"Task ID {task_id_to_update} status updated to '{new_status}'.")
                    break
                else:
                    print(f"Invalid status. Please choose from: {', '.join(STATUS_OPTIONS)}")
            break

    if not task_found:
        print(f"No task found with ID: {task_id_to_update}")

def main_menu():
    """Displays the main menu and handles user input."""
    initialize_csv() # Ensure CSV exists on startup

    while True:
        print("\n--- Maintenance Task Logger ---")
        print("1. Add New Task")
        print("2. View All Tasks")
        print("3. View Open Tasks")
        print("4. Update Task Status")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            add_task()
        elif choice == '2':
            view_all_tasks()
        elif choice == '3':
            view_open_tasks()
        elif choice == '4':
            update_task_status()
        elif choice == '5':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()
