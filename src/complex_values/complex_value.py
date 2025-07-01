from abc import ABC, abstractmethod


class ComplexValue(ABC):
    """
    Base class for complex values.
    """
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """Create an object from a dictionary."""

    @abstractmethod
    def __str__(self) -> str:
        """
        Return the object as a string suitable for use as a value in ARK server 
        configuration INI files.
        """
