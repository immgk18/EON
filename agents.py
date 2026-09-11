"""
EON Agents
==========
Multi-agent coordination layer for EON.
"""


class Agent:
    """Represents a specialized EON agent."""

    def __init__(self, name, role, description=""):
        self.name = name
        self.role = role
        self.description = description
        self.status = "IDLE"

    def execute(self, task):
        """Execute an assigned task."""

        if not task:
            return "No task was provided."

        self.status = "WORKING"

        result = (
            f"{self.name} is handling the task: "
            f"{task}"
        )

        self.status = "COMPLETED"

        return result


class AgentManager:
    """Manages EON's specialized agents."""

    def __init__(self):
        self.agents = {}

        self.register_default_agents()

    def register_default_agents(self):
        """Create EON's initial specialized agents."""

        self.register(
            "researcher",
            "Research Agent",
            "Finds and organizes information."
        )

        self.register(
            "coder",
            "Coding Agent",
            "Helps design, write, and analyze code."
        )

        self.register(
            "analyst",
            "Analysis Agent",
            "Analyzes information and identifies patterns."
        )

        self.register(
            "planner",
            "Planning Agent",
            "Breaks large goals into manageable tasks."
        )

        self.register(
            "document",
            "Document Agent",
            "Works with documents and structured information."
        )

    def register(self, agent_id, role, description=""):
        """Register a new agent."""

        if agent_id in self.agents:
            return False

        self.agents[agent_id] = Agent(
            name=agent_id,
            role=role,
            description=description
        )

        return True

    def remove(self, agent_id):
        """Remove an agent."""

        if agent_id not in self.agents:
            return False

        del self.agents[agent_id]
        return True

    def get(self, agent_id):
        """Get an agent by ID."""

        return self.agents.get(agent_id)

    def assign(self, agent_id, task):
        """Assign a task to a specific agent."""

        agent = self.get(agent_id)

        if agent is None:
            return f"Agent '{agent_id}' was not found."

        return agent.execute(task)

    def list_agents(self):
        """Return all registered agents."""

        return list(self.agents.values())

    def get_agent_names(self):
        """Return all agent IDs."""

        return list(self.agents.keys())

    def status(self):
        """Return the status of all agents."""

        return {
            agent_id: agent.status
            for agent_id, agent in self.agents.items()
        }
