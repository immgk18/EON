"""
EON Agents
==========
Multi-agent coordination layer for EON.

Agents are specialized workers coordinated by EON.

Default agents:
- Researcher
- Coder
- Analyst
- Planner
- Document

The system supports:
- Agent registration
- Agent removal
- Task assignment
- Agent status
- Multi-agent workflows
- Execution history
"""


from datetime import datetime


# =============================================================
# AGENT
# =============================================================

class Agent:
    """Represents one specialized EON agent."""

    def __init__(
        self,
        name,
        role,
        description=""
    ):

        self.name = name
        self.role = role
        self.description = description

        self.status = "IDLE"

        self.current_task = None
        self.last_result = None

        self.tasks_completed = 0

        self.history = []

    # =========================================================
    # EXECUTE
    # =========================================================

    def execute(self, task):
        """Execute a task assigned to this agent."""

        if not task:

            return (
                f"{self.name}: "
                "No task was provided."
            )

        self.status = "WORKING"
        self.current_task = task

        started_at = datetime.now().isoformat()

        # -----------------------------------------------------
        # Placeholder execution layer
        # -----------------------------------------------------

        result = (
            f"{self.name} is handling the task: "
            f"{task}"
        )

        # -----------------------------------------------------
        # Complete
        # -----------------------------------------------------

        self.status = "COMPLETED"

        self.last_result = result

        self.tasks_completed += 1

        self.history.append(
            {
                "task": task,
                "result": result,
                "started_at": started_at,
                "completed_at":
                    datetime.now().isoformat(),
            }
        )

        self.current_task = None

        return result

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.status = "IDLE"
        self.current_task = None
        self.last_result = None

    # =========================================================
    # STATUS
    # =========================================================

    def status_info(self):

        return {
            "name":
                self.name,

            "role":
                self.role,

            "description":
                self.description,

            "status":
                self.status,

            "current_task":
                self.current_task,

            "tasks_completed":
                self.tasks_completed,
        }


# =============================================================
# AGENT MANAGER
# =============================================================

class AgentManager:
    """
    Central manager for EON's multi-agent system.

    The manager controls which agent receives which task.
    """

    def __init__(self):

        self.agents = {}

        self.workflow_history = []

        self.register_default_agents()

    # =========================================================
    # DEFAULT AGENTS
    # =========================================================

    def register_default_agents(self):

        self.register(
            "researcher",
            "Research Agent",
            "Finds, organizes, and summarizes information."
        )

        self.register(
            "coder",
            "Coding Agent",
            "Designs, writes, explains, and analyzes code."
        )

        self.register(
            "analyst",
            "Analysis Agent",
            "Analyzes information and identifies patterns."
        )

        self.register(
            "planner",
            "Planning Agent",
            "Breaks large goals into smaller tasks."
        )

        self.register(
            "document",
            "Document Agent",
            "Works with documents and structured information."
        )

    # =========================================================
    # REGISTER
    # =========================================================

    def register(
        self,
        agent_id,
        role,
        description=""
    ):

        if not agent_id:
            return False

        if agent_id in self.agents:
            return False

        self.agents[agent_id] = Agent(
            name=agent_id,
            role=role,
            description=description,
        )

        return True

    # =========================================================
    # REMOVE
    # =========================================================

    def remove(self, agent_id):

        if agent_id not in self.agents:
            return False

        del self.agents[
            agent_id
        ]

        return True

    # =========================================================
    # GET
    # =========================================================

    def get(self, agent_id):

        return self.agents.get(
            agent_id
        )

    # =========================================================
    # ASSIGN
    # =========================================================

    def assign(
        self,
        agent_id,
        task
    ):
        """Assign a task to a specific agent."""

        agent = self.get(
            agent_id
        )

        if agent is None:

            return (
                f"Agent '{agent_id}' "
                "was not found."
            )

        result = agent.execute(
            task
        )

        self.workflow_history.append(
            {
                "agent":
                    agent_id,

                "task":
                    task,

                "result":
                    result,

                "timestamp":
                    datetime.now().isoformat(),
            }
        )

        return result

    # =========================================================
    # AUTO SELECT
    # =========================================================

    def select_agent(self, task):
        """
        Select the most suitable agent based on keywords.

        This is a lightweight routing layer for now.
        The AI Brain can replace this with intelligent
        selection later.
        """

        if not task:
            return "planner"

        text = task.lower()

        # -----------------------------------------------------
        # Research
        # -----------------------------------------------------

        research_keywords = {
            "research",
            "find",
            "search",
            "investigate",
            "information",
            "study",
            "latest",
        }

        if any(
            word in text
            for word in research_keywords
        ):

            return "researcher"

        # -----------------------------------------------------
        # Coding
        # -----------------------------------------------------

        coding_keywords = {
            "code",
            "coding",
            "program",
            "python",
            "javascript",
            "html",
            "css",
            "bug",
            "debug",
            "function",
        }

        if any(
            word in text
            for word in coding_keywords
        ):

            return "coder"

        # -----------------------------------------------------
        # Analysis
        # -----------------------------------------------------

        analysis_keywords = {
            "analyze",
            "analysis",
            "compare",
            "calculate",
            "data",
            "pattern",
            "evaluate",
        }

        if any(
            word in text
            for word in analysis_keywords
        ):

            return "analyst"

        # -----------------------------------------------------
        # Documents
        # -----------------------------------------------------

        document_keywords = {
            "document",
            "pdf",
            "report",
            "write",
            "summarize",
            "notes",
        }

        if any(
            word in text
            for word in document_keywords
        ):

            return "document"

        # -----------------------------------------------------
        # Default
        # -----------------------------------------------------

        return "planner"

    # =========================================================
    # AUTO ASSIGN
    # =========================================================

    def auto_assign(self, task):
        """
        Automatically select an agent and assign the task.
        """

        agent_id = self.select_agent(
            task
        )

        result = self.assign(
            agent_id,
            task
        )

        return {
            "agent":
                agent_id,

            "task":
                task,

            "result":
                result,
        }

    # =========================================================
    # MULTI-AGENT WORKFLOW
    # =========================================================

    def run_workflow(self, task, agents=None):
        """
        Run a task through multiple agents.

        Example:

        Planner
            ↓
        Researcher
            ↓
        Analyst
            ↓
        Document
        """

        if not task:

            return {
                "status": "FAILED",
                "message": "No workflow task provided.",
            }

        if agents is None:

            agents = [
                "planner",
                "researcher",
                "analyst",
                "document",
            ]

        results = []

        for agent_id in agents:

            if agent_id not in self.agents:

                results.append(
                    {
                        "agent":
                            agent_id,

                        "status":
                            "NOT_FOUND",
                    }
                )

                continue

            result = self.assign(
                agent_id,
                task
            )

            results.append(
                {
                    "agent":
                        agent_id,

                    "status":
                        "COMPLETED",

                    "result":
                        result,
                }
            )

        workflow = {
            "task":
                task,

            "agents":
                agents,

            "results":
                results,

            "timestamp":
                datetime.now().isoformat(),
        }

        self.workflow_history.append(
            workflow
        )

        return workflow

    # =========================================================
    # LIST AGENTS
    # =========================================================

    def list_agents(self):

        return list(
            self.agents.values()
        )

    # =========================================================
    # AGENT NAMES
    # =========================================================

    def get_agent_names(self):

        return list(
            self.agents.keys()
        )

    # =========================================================
    # AGENT STATUS
    # =========================================================

    def get_status(self, agent_id):

        agent = self.get(
            agent_id
        )

        if agent is None:
            return None

        return agent.status_info()

    # =========================================================
    # ALL STATUS
    # =========================================================

    def status(self):

        return {
            agent_id:
                agent.status_info()

            for agent_id, agent
            in self.agents.items()
        }

    # =========================================================
    # WORKFLOW HISTORY
    # =========================================================

    def get_workflow_history(self):

        return self.workflow_history.copy()

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        for agent in self.agents.values():

            agent.reset()

        self.workflow_history.clear()
