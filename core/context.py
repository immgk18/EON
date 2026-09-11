class Context:
    """Stores the current EON session context."""

    def __init__(self):
        self.history = []
        self.current_task = None
        self.variables = {}

    def add_message(self, role, message):
        self.history.append({
            "role": role,
            "message": message
        })

    def set_task(self, task):
        self.current_task = task

    def clear(self):
        self.history.clear()
        self.current_task = None
        self.variables.clear()

    def get_history(self):
        return self.history
