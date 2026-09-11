"""
EON Task Engine
===============
Goal, task, subtask, progress, and workflow management.

Pipeline:

Goal
  ↓
Plan
  ↓
Tasks
  ↓
Execution
  ↓
Verification
  ↓
Completion
"""


from datetime import datetime


# =============================================================
# TASK
# =============================================================

class Task:
    """Represents one EON task."""

    def __init__(
        self,
        task_id,
        title,
        description=""
    ):

        self.task_id = task_id
        self.title = title
        self.description = description

        self.status = "PENDING"

        self.result = None

        self.created_at = (
            datetime.now().isoformat()
        )

        self.started_at = None
        self.completed_at = None

        self.subtasks = []

        self.assigned_agent = None

        self.verification = None

    # =========================================================
    # START
    # =========================================================

    def start(self):

        self.status = "RUNNING"

        self.started_at = (
            datetime.now().isoformat()
        )

    # =========================================================
    # COMPLETE
    # =========================================================

    def complete(
        self,
        result=None
    ):

        self.status = "COMPLETED"

        self.result = result

        self.completed_at = (
            datetime.now().isoformat()
        )

    # =========================================================
    # FAIL
    # =========================================================

    def fail(
        self,
        result=None
    ):

        self.status = "FAILED"

        self.result = result

        self.completed_at = (
            datetime.now().isoformat()
        )

    # =========================================================
    # ADD SUBTASK
    # =========================================================

    def add_subtask(
        self,
        title,
        description=""
    ):

        subtask_id = (
            len(self.subtasks) + 1
        )

        subtask = {
            "id": subtask_id,
            "title": title,
            "description": description,
            "status": "PENDING",
            "result": None,
        }

        self.subtasks.append(
            subtask
        )

        return subtask

    # =========================================================
    # COMPLETE SUBTASK
    # =========================================================

    def complete_subtask(
        self,
        subtask_id,
        result=None
    ):

        for subtask in self.subtasks:

            if subtask["id"] == subtask_id:

                subtask["status"] = "COMPLETED"

                subtask["result"] = result

                return True

        return False

    # =========================================================
    # FAIL SUBTASK
    # =========================================================

    def fail_subtask(
        self,
        subtask_id,
        result=None
    ):

        for subtask in self.subtasks:

            if subtask["id"] == subtask_id:

                subtask["status"] = "FAILED"

                subtask["result"] = result

                return True

        return False

    # =========================================================
    # PROGRESS
    # =========================================================

    def progress(self):

        if not self.subtasks:

            if self.status == "COMPLETED":
                return 100

            if self.status == "RUNNING":
                return 50

            return 0

        completed = sum(
            1
            for subtask in self.subtasks
            if subtask["status"] == "COMPLETED"
        )

        return int(
            (completed / len(self.subtasks)) * 100
        )

    # =========================================================
    # VERIFY
    # =========================================================

    def verify(
        self,
        success,
        message=""
    ):

        self.verification = {
            "verified": bool(success),
            "message": message,
            "timestamp":
                datetime.now().isoformat(),
        }

        if success:

            self.complete(
                self.result
            )

        else:

            self.fail(
                message
            )

        return self.verification

    # =========================================================
    # ASSIGN AGENT
    # =========================================================

    def assign_agent(
        self,
        agent_id
    ):

        self.assigned_agent = agent_id

    # =========================================================
    # STATUS
    # =========================================================

    def status_info(self):

        return {
            "task_id":
                self.task_id,

            "title":
                self.title,

            "description":
                self.description,

            "status":
                self.status,

            "progress":
                self.progress(),

            "assigned_agent":
                self.assigned_agent,

            "subtasks":
                len(self.subtasks),

            "result":
                self.result,

            "verification":
                self.verification,

            "created_at":
                self.created_at,

            "started_at":
                self.started_at,

            "completed_at":
                self.completed_at,
        }

    # =========================================================
    # REPRESENTATION
    # =========================================================

    def __repr__(self):

        return (
            f"Task("
            f"{self.task_id}, "
            f"{self.title}, "
            f"{self.status}, "
            f"{self.progress()}%"
            f")"
        )


# =============================================================
# TASK ENGINE
# =============================================================

class TaskEngine:
    """Central task and goal manager for EON."""

    def __init__(self):

        self.tasks = {}

        self.next_id = 1

        self.current_goal = None

        self.goal_history = []

    # =========================================================
    # CREATE GOAL
    # =========================================================

    def create_goal(
        self,
        goal
    ):

        if not goal:
            return None

        self.current_goal = {
            "goal": goal,
            "created_at":
                datetime.now().isoformat(),
            "status": "ACTIVE",
        }

        self.goal_history.append(
            self.current_goal.copy()
        )

        return self.current_goal

    # =========================================================
    # COMPLETE GOAL
    # =========================================================

    def complete_goal(self):

        if self.current_goal is None:
            return False

        self.current_goal["status"] = "COMPLETED"

        return True

    # =========================================================
    # CREATE TASK
    # =========================================================

    def create_task(
        self,
        title,
        description=""
    ):

        task_id = self.next_id

        task = Task(
            task_id,
            title,
            description
        )

        self.tasks[task_id] = task

        self.next_id += 1

        return task

    # =========================================================
    # CREATE SUBTASK
    # =========================================================

    def create_subtask(
        self,
        task_id,
        title,
        description=""
    ):

        task = self.get_task(
            task_id
        )

        if task is None:
            return None

        return task.add_subtask(
            title,
            description
        )

    # =========================================================
    # START TASK
    # =========================================================

    def start_task(
        self,
        task_id
    ):

        task = self.get_task(
            task_id
        )

        if task is None:
            return False

        task.start()

        return True

    # =========================================================
    # COMPLETE TASK
    # =========================================================

    def complete_task(
        self,
        task_id,
        result=None
    ):

        task = self.get_task(
            task_id
        )

        if task is None:
            return False

        task.complete(
            result
        )

        return True

    # =========================================================
    # FAIL TASK
    # =========================================================

    def fail_task(
        self,
        task_id,
        result=None
    ):

        task = self.get_task(
            task_id
        )

        if task is None:
            return False

        task.fail(
            result
        )

        return True

    # =========================================================
    # VERIFY TASK
    # =========================================================

    def verify_task(
        self,
        task_id,
        success,
        message=""
    ):

        task = self.get_task(
            task_id
        )

        if task is None:
            return False

        return task.verify(
            success,
            message
        )

    # =========================================================
    # ASSIGN AGENT
    # =========================================================

    def assign_agent(
        self,
        task_id,
        agent_id
    ):

        task = self.get_task(
            task_id
        )

        if task is None:
            return False

        task.assign_agent(
            agent_id
        )

        return True

    # =========================================================
    # GET TASK
    # =========================================================

    def get_task(
        self,
        task_id
    ):

        return self.tasks.get(
            task_id
        )

    # =========================================================
    # PENDING
    # =========================================================

    def get_pending_tasks(self):

        return [
            task
            for task in self.tasks.values()
            if task.status == "PENDING"
        ]

    # =========================================================
    # RUNNING
    # =========================================================

    def get_running_tasks(self):

        return [
            task
            for task in self.tasks.values()
            if task.status == "RUNNING"
        ]

    # =========================================================
    # COMPLETED
    # =========================================================

    def get_completed_tasks(self):

        return [
            task
            for task in self.tasks.values()
            if task.status == "COMPLETED"
        ]

    # =========================================================
    # FAILED
    # =========================================================

    def get_failed_tasks(self):

        return [
            task
            for task in self.tasks.values()
            if task.status == "FAILED"
        ]

    # =========================================================
    # LIST TASKS
    # =========================================================

    def list_tasks(self):

        return list(
            self.tasks.values()
        )

    # =========================================================
    # TASK PROGRESS
    # =========================================================

    def get_progress(
        self,
        task_id
    ):

        task = self.get_task(
            task_id
        )

        if task is None:
            return None

        return task.progress()

    # =========================================================
    # ACTIVE TASKS
    # =========================================================

    def get_active_tasks(self):

        return [
            task
            for task in self.tasks.values()
            if task.status in {
                "PENDING",
                "RUNNING",
            }
        ]

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self):

        self.tasks.clear()

        self.current_goal = None

        self.goal_history.clear()

        self.next_id = 1

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        return {
            "goal":
                self.current_goal,

            "total_tasks":
                len(self.tasks),

            "pending":
                len(
                    self.get_pending_tasks()
                ),

            "running":
                len(
                    self.get_running_tasks()
                ),

            "completed":
                len(
                    self.get_completed_tasks()
                ),

            "failed":
                len(
                    self.get_failed_tasks()
                ),

            "active":
                len(
                    self.get_active_tasks()
                ),
        }
