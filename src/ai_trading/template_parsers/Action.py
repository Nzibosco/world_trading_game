from abc import ABC, abstractmethod

class Action(ABC):
    """Base class for all actions."""

    def __init__(self, country):
        self.country = country  # Country where the action takes place

    @abstractmethod
    def execute(self, world_state):
        """
        Execute the action on the world state.
        This should be implemented in the child classes.
        """
        pass
