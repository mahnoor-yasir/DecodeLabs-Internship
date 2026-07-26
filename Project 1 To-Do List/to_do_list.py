import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class Task:
    """Advanced Task class with priority, due dates, tags, and completion status"""
    
    PRIORITY_LEVELS = ['low', 'medium', 'high', 'critical']
    
    def __init__(self, title: str, description: str = "", priority: str = 'medium', 
                 due_date: Optional[str] = None, tags: List[str] = None):
        self.id = None
        self.title = title
        self.description = description
        self.priority = priority.lower() if priority.lower() in self.PRIORITY_LEVELS else 'medium'
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.due_date = due_date
        self.tags = tags or []
        self.completed = False
        self.completed_at = None
        self.subtasks = []
        self.attachments = []
        
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'due_date': self.due_date,
            'tags': self.tags,
            'completed': self.completed,
            'completed_at': self.completed_at,
            'subtasks': self.subtasks,
            'attachments': self.attachments
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        task = cls(
            title=data['title'],
            description=data['description'],
            priority=data['priority'],
            due_date=data.get('due_date'),
            tags=data.get('tags', [])
        )
        task.id = data['id']
        task.created_at = data['created_at']
        task.updated_at = data['updated_at']
        task.completed = data['completed']
        task.completed_at = data.get('completed_at')
        task.subtasks = data.get('subtasks', [])
        task.attachments = data.get('attachments', [])
        return task
    
    def mark_complete(self):
        self.completed = True
        self.completed_at = datetime.now().isoformat()
        self.updated_at = self.completed_at
        
    def mark_incomplete(self):
        self.completed = False
        self.completed_at = None
        self.updated_at = datetime.now().isoformat()
    
    def add_subtask(self, subtask_title: str):
        self.subtasks.append({
            'id': len(self.subtasks) + 1,
            'title': subtask_title,
            'completed': False,
            'created_at': datetime.now().isoformat()
        })
        self.updated_at = datetime.now().isoformat()
    
    def __str__(self) -> str:
        status = "DONE" if self.completed else "PENDING"
        due_str = f" | Due: {self.due_date}" if self.due_date else ""
        tags_str = f" | Tags: {', '.join(self.tags)}" if self.tags else ""
        return f"{status} | {self.priority.upper()} | {self.title}{due_str}{tags_str}"

class TodoList:
    """Advanced To-Do List Manager with persistence, search, filtering, and analytics"""
    
    def __init__(self, username: str = "default"):
        self.username = username
        self.tasks: List[Task] = []
        self.history: List[Dict] = []
        self.next_id = 1
        self.data_file = f"todo_{username}.json"
        self.history_file = f"todo_history_{username}.json"
        self.load_data()
        
    def load_data(self):
        """Load tasks and history from JSON files"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
                    if self.tasks:
                        self.next_id = max(task.id for task in self.tasks) + 1
                    else:
                        self.next_id = 1
            except Exception as e:
                print(f"Error loading data: {e}")
                self.tasks = []
                self.next_id = 1
        else:
            self.tasks = []
            self.next_id = 1
            
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []
        else:
            self.history = []
    
    def save_data(self):
        """Save tasks and history to JSON files"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2)
            
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def log_action(self, action: str, task_id: int = None):
        """Log user actions for history/audit"""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'task_id': task_id,
            'user': self.username
        })
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
        self.save_data()
    
    def add_task(self, title: str, description: str = "", priority: str = 'medium',
                 due_date: Optional[str] = None, tags: List[str] = None) -> Task:
        """Add a new task with comprehensive details"""
        task = Task(title, description, priority, due_date, tags)
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.log_action('add_task', task.id)
        self.save_data()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.log_action('delete_task', task_id)
                del self.tasks[i]
                self.save_data()
                return True
        return False
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        """Update task fields dynamically"""
        for task in self.tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key) and key not in ['id', 'created_at']:
                        setattr(task, key, value)
                task.updated_at = datetime.now().isoformat()
                self.log_action('update_task', task_id)
                self.save_data()
                return True
        return False
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as complete"""
        for task in self.tasks:
            if task.id == task_id:
                task.mark_complete()
                self.log_action('complete_task', task_id)
                self.save_data()
                return True
        return False
    
    def uncomplete_task(self, task_id: int) -> bool:
        """Mark a task as incomplete"""
        for task in self.tasks:
            if task.id == task_id:
                task.mark_incomplete()
                self.log_action('uncomplete_task', task_id)
                self.save_data()
                return True
        return False
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks(self, filter_by: Dict = None) -> List[Task]:
        """Get tasks with optional filtering"""
        tasks = self.tasks.copy()
        
        if filter_by:
            if 'completed' in filter_by:
                tasks = [t for t in tasks if t.completed == filter_by['completed']]
            
            if 'priority' in filter_by:
                tasks = [t for t in tasks if t.priority in filter_by['priority']]
            
            if 'tags' in filter_by:
                tasks = [t for t in tasks if any(tag in t.tags for tag in filter_by['tags'])]
            
            if 'due_before' in filter_by:
                due_before = datetime.fromisoformat(filter_by['due_before'])
                tasks = [t for t in tasks if t.due_date and 
                        datetime.fromisoformat(t.due_date) <= due_before]
            
            if 'due_after' in filter_by:
                due_after = datetime.fromisoformat(filter_by['due_after'])
                tasks = [t for t in tasks if t.due_date and 
                        datetime.fromisoformat(t.due_date) >= due_after]
            
            if 'search' in filter_by:
                search_term = filter_by['search'].lower()
                tasks = [t for t in tasks if 
                        search_term in t.title.lower() or 
                        search_term in t.description.lower()]
        
        return tasks
    
    def sort_tasks(self, tasks: List[Task], sort_by: str = 'created_at', reverse: bool = False) -> List[Task]:
        """Sort tasks by different criteria"""
        if sort_by == 'priority':
            priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
            return sorted(tasks, key=lambda t: priority_order.get(t.priority, 4), reverse=not reverse)
        elif sort_by == 'due_date':
            tasks_with_due = [t for t in tasks if t.due_date]
            tasks_without_due = [t for t in tasks if not t.due_date]
            sorted_with_due = sorted(tasks_with_due, key=lambda t: t.due_date, reverse=reverse)
            return sorted_with_due + tasks_without_due
        else:
            return sorted(tasks, key=lambda t: getattr(t, sort_by, ''), reverse=reverse)
    
    def get_statistics(self) -> Dict:
        """Get comprehensive task statistics"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.completed])
        pending = total - completed
        
        priority_stats = {p: 0 for p in Task.PRIORITY_LEVELS}
        for task in self.tasks:
            priority_stats[task.priority] += 1
        
        now = datetime.now()
        due_soon = 0
        overdue = 0
        for task in self.tasks:
            if task.due_date and not task.completed:
                due_date = datetime.fromisoformat(task.due_date)
                if due_date < now:
                    overdue += 1
                elif (due_date - now).days <= 7:
                    due_soon += 1
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': (completed / total * 100) if total > 0 else 0,
            'by_priority': priority_stats,
            'due_soon': due_soon,
            'overdue': overdue,
            'tags': list(set([tag for task in self.tasks for tag in task.tags]))
        }
    
    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Get tasks due within the next N days"""
        now = datetime.now()
        future = now + timedelta(days=days)
        return [t for t in self.tasks if t.due_date and not t.completed and
                now <= datetime.fromisoformat(t.due_date) <= future]
    
    def get_overdue_tasks(self) -> List[Task]:
        """Get overdue tasks"""
        now = datetime.now()
        return [t for t in self.tasks if t.due_date and not t.completed and
                datetime.fromisoformat(t.due_date) < now]
    
    def export_to_text(self, filename: str = None):
        """Export tasks to a formatted text file"""
        if not filename:
            filename = f"todo_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"=== TO-DO LIST EXPORT ({self.username}) ===\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            stats = self.get_statistics()
            f.write("STATISTICS:\n")
            f.write(f"  Total: {stats['total']} | Completed: {stats['completed']} | Pending: {stats['pending']}\n")
            f.write(f"  Completion Rate: {stats['completion_rate']:.1f}%\n")
            f.write(f"  Overdue: {stats['overdue']} | Due Soon: {stats['due_soon']}\n\n")
            
            for i, task in enumerate(self.tasks, 1):
                status = "COMPLETED" if task.completed else "PENDING"
                f.write(f"{i}. {task.title}\n")
                f.write(f"   ID: {task.id}\n")
                f.write(f"   Status: {status}\n")
                f.write(f"   Priority: {task.priority.upper()}\n")
                if task.description:
                    f.write(f"   Description: {task.description}\n")
                if task.due_date:
                    f.write(f"   Due Date: {task.due_date}\n")
                if task.tags:
                    f.write(f"   Tags: {', '.join(task.tags)}\n")
                if task.subtasks:
                    f.write("   Subtasks:\n")
                    for subtask in task.subtasks:
                        sub_status = "DONE" if subtask['completed'] else "PENDING"
                        f.write(f"     {sub_status} {subtask['title']}\n")
                f.write(f"   Created: {task.created_at}\n")
                if task.completed_at:
                    f.write(f"   Completed: {task.completed_at}\n")
                f.write("   " + "-" * 40 + "\n\n")
        
        print(f"Exported to {filename}")
        return filename

class TodoApp:
    """Main application with CLI interface"""
    
    def __init__(self):
        print("=" * 60)
        print("ADVANCED TO-DO LIST MANAGER")
        print("=" * 60)
        username = input("Enter your username: ").strip() or "default"
        self.todo = TodoList(username)
        print(f"Welcome, {username}! Loaded {len(self.todo.tasks)} tasks.\n")
        self.run()
    
    def run(self):
        while True:
            self.show_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.add_task_menu()
            elif choice == '2':
                self.view_tasks_menu()
            elif choice == '3':
                self.complete_task_menu()
            elif choice == '4':
                self.update_task_menu()
            elif choice == '5':
                self.delete_task_menu()
            elif choice == '6':
                self.search_tasks_menu()
            elif choice == '7':
                self.show_statistics()
            elif choice == '8':
                self.manage_subtasks_menu()
            elif choice == '9':
                self.export_tasks_menu()
            elif choice == '0':
                self.save_and_exit()
                break
            else:
                print("Invalid choice. Please try again.")
    
    def show_menu(self):
        print("\n" + "=" * 60)
        print("MAIN MENU")
        print("=" * 60)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Search Tasks")
        print("7. Statistics")
        print("8. Manage Subtasks")
        print("9. Export Tasks")
        print("0. Save & Exit")
        print("=" * 60)
        print(f"Total: {len(self.todo.tasks)} tasks | Pending: {self.todo.get_statistics()['pending']}")
    
    def add_task_menu(self):
        print("\n" + "-" * 40)
        print("ADD NEW TASK")
        print("-" * 40)
        
        title = input("Title: ").strip()
        if not title:
            print("Title is required!")
            return
        
        description = input("Description (optional): ").strip()
        
        print("\nPriority Levels: low, medium, high, critical")
        priority = input("Priority (default: medium): ").strip().lower()
        if priority not in Task.PRIORITY_LEVELS:
            priority = 'medium'
        
        due_date = input("Due Date (YYYY-MM-DD, optional): ").strip()
        if due_date:
            try:
                datetime.fromisoformat(due_date)
            except ValueError:
                print("Invalid date format. Date will be ignored.")
                due_date = None
        
        tags_input = input("Tags (comma-separated, optional): ").strip()
        tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
        
        task = self.todo.add_task(title, description, priority, due_date, tags)
        print(f"Task added successfully! (ID: {task.id})")
    
    def view_tasks_menu(self):
        print("\n" + "-" * 40)
        print("VIEW TASKS")
        print("-" * 40)
        
        print("\nFilter options:")
        print("1. All tasks")
        print("2. Pending tasks")
        print("3. Completed tasks")
        print("4. Overdue tasks")
        print("5. Upcoming tasks (7 days)")
        print("6. High priority tasks")
        
        choice = input("\nSelect filter (1-6, default: 1): ").strip()
        
        filter_by = {}
        if choice == '2':
            filter_by['completed'] = False
        elif choice == '3':
            filter_by['completed'] = True
        elif choice == '4':
            tasks = self.todo.get_overdue_tasks()
            self.display_tasks_table(tasks, "OVERDUE TASKS")
            return
        elif choice == '5':
            tasks = self.todo.get_upcoming_tasks(7)
            self.display_tasks_table(tasks, "UPCOMING TASKS (7 days)")
            return
        elif choice == '6':
            filter_by['priority'] = ['high', 'critical']
        
        tasks = self.todo.get_tasks(filter_by)
        
        if not tasks:
            print("No tasks found.")
            return
        
        print("\nSort by:")
        print("1. Created date (newest)")
        print("2. Created date (oldest)")
        print("3. Priority (highest)")
        print("4. Due date (soonest)")
        
        sort_choice = input("Select sort (1-4, default: 1): ").strip()
        sort_map = {'2': 'created_at', '3': 'priority', '4': 'due_date'}
        sort_by = sort_map.get(sort_choice, 'created_at')
        reverse = sort_choice == '1'
        
        tasks = self.todo.sort_tasks(tasks, sort_by, reverse)
        self.display_tasks_table(tasks)
    
    def display_tasks_table(self, tasks: List[Task], title: str = "TASKS"):
        """Display tasks in a formatted table"""
        if not tasks:
            print("No tasks to display.")
            return
        
        print("\n" + "=" * 100)
        print(f"{title} ({len(tasks)})")
        print("=" * 100)
        
        # Table header
        print(f"{'ID':<5} {'STATUS':<10} {'PRIORITY':<10} {'TITLE':<30} {'DUE DATE':<15} {'TAGS':<20}")
        print("-" * 100)
        
        # Table rows
        for task in tasks:
            status = "DONE" if task.completed else "PENDING"
            priority = task.priority.upper()
            title_display = task.title[:27] + "..." if len(task.title) > 30 else task.title
            due_date = task.due_date if task.due_date else "N/A"
            
            # Check if due date is overdue or upcoming
            if task.due_date and not task.completed:
                due_date_obj = datetime.fromisoformat(task.due_date)
                now = datetime.now()
                if due_date_obj < now:
                    due_date = "OVERDUE"
                elif (due_date_obj - now).days <= 7:
                    due_date = "SOON"
            
            tags_display = ", ".join(task.tags[:2]) if task.tags else "N/A"
            if len(task.tags) > 2:
                tags_display += "..."
            
            print(f"{task.id:<5} {status:<10} {priority:<10} {title_display:<30} {due_date:<15} {tags_display:<20}")
        
        print("=" * 100)
        print(f"Total: {len(tasks)} tasks")
        
        # Show details for selected task option
        print("\nOptions:")
        print("1. View task details")
        print("2. Return to menu")
        
        choice = input("\nEnter your choice: ").strip()
        if choice == '1':
            try:
                task_id = int(input("Enter task ID to view details: ").strip())
                task = self.todo.get_task(task_id)
                if task:
                    self.display_task_details(task)
                else:
                    print("Task not found!")
            except ValueError:
                print("Invalid ID!")
    
    def display_task_details(self, task: Task):
        """Display detailed view of a single task"""
        print("\n" + "=" * 60)
        print("TASK DETAILS")
        print("=" * 60)
        
        print(f"ID:          {task.id}")
        print(f"Title:       {task.title}")
        print(f"Status:      {'COMPLETED' if task.completed else 'PENDING'}")
        print(f"Priority:    {task.priority.upper()}")
        print(f"Description: {task.description if task.description else 'No description'}")
        print(f"Due Date:    {task.due_date if task.due_date else 'No due date'}")
        print(f"Tags:        {', '.join(task.tags) if task.tags else 'No tags'}")
        print(f"Created:     {task.created_at}")
        print(f"Updated:     {task.updated_at}")
        if task.completed_at:
            print(f"Completed:   {task.completed_at}")
        
        if task.subtasks:
            print("\nSubtasks:")
            print("-" * 40)
            for subtask in task.subtasks:
                status = "DONE" if subtask['completed'] else "PENDING"
                print(f"  [{status}] {subtask['title']} (ID: {subtask['id']})")
        
        print("=" * 60)
        input("\nPress Enter to continue...")
    
    def complete_task_menu(self):
        try:
            task_id = int(input("Enter task ID to complete: ").strip())
            if self.todo.complete_task(task_id):
                print("Task completed!")
            else:
                print("Task not found!")
        except ValueError:
            print("Please enter a valid task ID (number)!")
    
    def update_task_menu(self):
        try:
            task_id = int(input("Enter task ID to update: ").strip())
            task = self.todo.get_task(task_id)
            if not task:
                print("Task not found!")
                return
            
            print(f"\nUpdating: {task.title}")
            print("Leave blank to keep current value.\n")
            
            title = input(f"Title [{task.title}]: ").strip()
            description = input(f"Description [{task.description}]: ").strip()
            
            print(f"\nPriority Levels: {', '.join(Task.PRIORITY_LEVELS)}")
            priority = input(f"Priority [{task.priority}]: ").strip().lower()
            
            due_date = input(f"Due Date [{task.due_date or 'None'}]: ").strip()
            
            tags = input(f"Tags [{', '.join(task.tags) or 'None'}]: ").strip()
            
            updates = {}
            if title:
                updates['title'] = title
            if description:
                updates['description'] = description
            if priority in Task.PRIORITY_LEVELS:
                updates['priority'] = priority
            if due_date:
                try:
                    datetime.fromisoformat(due_date)
                    updates['due_date'] = due_date
                except ValueError:
                    print("Invalid date format. Skipping.")
            if tags:
                updates['tags'] = [tag.strip() for tag in tags.split(',')]
            
            if updates:
                self.todo.update_task(task_id, **updates)
                print("Task updated successfully!")
            else:
                print("No changes made.")
        except ValueError:
            print("Please enter a valid task ID (number)!")
    
    def delete_task_menu(self):
        try:
            task_id = int(input("Enter task ID to delete: ").strip())
            confirm = input(f"Are you sure you want to delete task {task_id}? (y/n): ").strip().lower()
            if confirm == 'y':
                if self.todo.delete_task(task_id):
                    print("Task deleted successfully!")
                else:
                    print("Task not found!")
            else:
                print("Deletion cancelled.")
        except ValueError:
            print("Please enter a valid task ID (number)!")
    
    def search_tasks_menu(self):
        search_term = input("Enter search term: ").strip()
        if not search_term:
            print("Please enter a search term.")
            return
        
        tasks = self.todo.get_tasks({'search': search_term})
        self.display_tasks_table(tasks, f"SEARCH RESULTS: '{search_term}'")
    
    def show_statistics(self):
        stats = self.todo.get_statistics()
        
        print("\n" + "=" * 60)
        print("TASK STATISTICS")
        print("=" * 60)
        
        print(f"\nOverview:")
        print(f"  Total Tasks: {stats['total']}")
        print(f"  Completed: {stats['completed']}")
        print(f"  Pending: {stats['pending']}")
        print(f"  Completion Rate: {stats['completion_rate']:.1f}%")
        
        print(f"\nPriority Distribution:")
        for priority, count in stats['by_priority'].items():
            bar = "#" * min(count, 20) + "." * (20 - min(count, 20))
            print(f"  {priority.upper():8} {bar} {count}")
        
        print(f"\nDeadlines:")
        print(f"  Overdue: {stats['overdue']}")
        print(f"  Due Soon (7 days): {stats['due_soon']}")
        
        if stats['tags']:
            print(f"\nTags ({len(stats['tags'])}):")
            for tag in sorted(stats['tags'])[:10]:
                count = sum(1 for t in self.todo.tasks if tag in t.tags)
                print(f"  #{tag} ({count} tasks)")
    
    def manage_subtasks_menu(self):
        try:
            task_id = int(input("Enter task ID to manage subtasks: ").strip())
            task = self.todo.get_task(task_id)
            if not task:
                print("Task not found!")
                return
            
            print(f"\nManaging subtasks for: {task.title}")
            print("-" * 40)
            
            if task.subtasks:
                print("\nCurrent subtasks:")
                # Display subtasks in table format
                print(f"{'ID':<5} {'STATUS':<10} {'TITLE':<30}")
                print("-" * 45)
                for subtask in task.subtasks:
                    status = "DONE" if subtask['completed'] else "PENDING"
                    print(f"{subtask['id']:<5} {status:<10} {subtask['title']:<30}")
            
            print("\nOptions:")
            print("1. Add subtask")
            print("2. Complete subtask")
            print("3. Delete subtask")
            
            choice = input("\nSelect option (1-3, or 0 to cancel): ").strip()
            
            if choice == '1':
                subtask_title = input("Enter subtask title: ").strip()
                if subtask_title:
                    task.add_subtask(subtask_title)
                    self.todo.save_data()
                    print("Subtask added!")
                else:
                    print("Subtask title is required!")
            
            elif choice == '2':
                try:
                    subtask_id = int(input("Enter subtask ID to complete: ").strip())
                    for subtask in task.subtasks:
                        if subtask['id'] == subtask_id:
                            subtask['completed'] = True
                            task.updated_at = datetime.now().isoformat()
                            self.todo.save_data()
                            print("Subtask completed!")
                            return
                    print("Subtask not found!")
                except ValueError:
                    print("Please enter a valid subtask ID (number)!")
            
            elif choice == '3':
                try:
                    subtask_id = int(input("Enter subtask ID to delete: ").strip())
                    for i, subtask in enumerate(task.subtasks):
                        if subtask['id'] == subtask_id:
                            del task.subtasks[i]
                            task.updated_at = datetime.now().isoformat()
                            self.todo.save_data()
                            print("Subtask deleted!")
                            return
                    print("Subtask not found!")
                except ValueError:
                    print("Please enter a valid subtask ID (number)!")
        except ValueError:
            print("Please enter a valid task ID (number)!")
    
    def export_tasks_menu(self):
        print("\n" + "-" * 40)
        print("EXPORT TASKS")
        print("-" * 40)
        
        filename = input("Export filename (default: auto-generated): ").strip()
        if not filename:
            filename = None
        
        self.todo.export_to_text(filename)
    
    def save_and_exit(self):
        self.todo.save_data()
        print(f"\nData saved successfully! Goodbye, {self.todo.username}!")

if __name__ == "__main__":
    try:
        app = TodoApp()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
