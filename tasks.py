"""
EON Task Engine
===============
Handles goals, tasks, subtasks, and task progress.
"""


class Task:
    """Represents a single task."""

    def __init__(self, task_id, title, description=""):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = "PENDING"
        self.result = None

    def start(self):
        self.status = "RUNNING"

    def complete(self, result=None):
        self.status = "COMPLETED"
        self.result = result

    def fail(self, result=None):
        self.status = "FAILED"
        self.result = result

    def __repr__(self):
        return (
            f"Task({self.task_id}, "
            f"{self.title}, "
            f"{self.status})"
        )


class TaskEngine:
    """EON's goal and task management system."""

    def __init__(self):
        self.tasks = {}
        self.next_id = 1
        self.current_goal = None

    def create_goal(self, goal):
        """Set the current EON goal."""

        self.current_goal = goal
        return goal

    def create_task(self, title, description=""):
        """Create a new task."""

        task_id = self.next_id

        task = Task(
            task_id,
            title,
            description
        )

        self.tasks[task_id] = task
        self.next_id += 1

        return task

    def start_task(self, task_id):
        """Start a task."""

        task = self.tasks.get(task_id)

        if task is None:
            return False

        task.start()
        return True

    def complete_task(self, task_id, result=None):
        """Mark a task as completed."""

        task = self.tasks.get(task_id)

        if task is None:
            return False

        task.complete(result)
        return True

    def fail_task(self, task_id, result=None):
        """Mark a task as failed."""

        task = self.tasks.get(task_id)

        if task is None:
            return False

        task.fail(result)
        return True

    def get_task(self, task_id):
        """Retrieve a task."""

        return self.tasks.get(task_id)

    def get_pending_tasks(self):
        """Return tasks that haven't been completed."""

        return [
            task
            for task in self.tasks.values()
            if task.status == "PENDING"
        ]

    def get_running_tasks(self):
        """Return currently running tasks."""

        return [
            task
            for task in self.tasks.values()
            if task.status == "RUNNING"
        ]

    def get_completed_tasks(self):
        """Return completed tasks."""

        return [
            task
            for task in self.tasks.values()
            if task.status == "COMPLETED"
        ]

    def list_tasks(self):
        """Return all tasks."""

        return list(self.tasks.values())

    def clear(self):
        """Clear all tasks."""

        self.tasks.clear()
        self.current_goal = None
        self.next_id = 1

    def status(self):
        """Return task engine status."""

        return {
            "goal": self.current_goal,
            "total_tasks": len(self.tasks),
            "pending": len(self.get_pending_tasks()),
            "running": len(self.get_running_tasks()),
            "completed": len(self.get_completed_tasks()),
        }
