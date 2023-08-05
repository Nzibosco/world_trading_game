from abc import ABC, abstractmethod


class Action(ABC):
    """Base class for all actions."""

    @abstractmethod
    def execute(self, world_state):
        """
        Execute the action on the world state.
        This should be implemented in the child classes.
        """
        pass
