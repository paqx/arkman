from dataclasses import dataclass, field
from typing import Optional, Self

from .complex_value import ComplexValue

# pylint: disable=invalid-name


@dataclass
class NPCSpawnEntry(ComplexValue):
    """
    Represents an individual spawn entry for a dino in a spawn container.

    Parameters
    ----------
    AnEntryName : Optional[str]
        Unique name given to this spawn entry.
    EntryWeight : Optional[float]
        The relative probability that this dino will be spawned (0.0 - 1.0).
    NPCsToSpawnStrings : Optional[list[str]]
        List of dino class strings to spawn.
    """
    AnEntryName: Optional[str] = None
    EntryWeight: Optional[float] = None
    NPCsToSpawnStrings: Optional[list[str]] = None

    def __str__(self) -> str:
        parts = []

        if self.AnEntryName is not None:
            parts.append(f'AnEntryName="{self.AnEntryName}"')

        if self.EntryWeight is not None:
            parts.append(f'EntryWeight={self.EntryWeight:.6f}')

        if self.NPCsToSpawnStrings is not None:
            npcs = ",".join(f'"{npc}"' for npc in self.NPCsToSpawnStrings)
            parts.append(f'NPCsToSpawnStrings=({npcs})')

        return f'({",".join(parts)})'

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            AnEntryName=data.get("AnEntryName"),
            EntryWeight=data.get("EntryWeight"),
            NPCsToSpawnStrings=data.get("NPCsToSpawnStrings"),
        )


@dataclass
class NPCSpawnLimit(ComplexValue):
    """
    Represents population limit for a dino in a spawn container.

    Parameters
    ----------
    NPCClassString : Optional[str]
        The class string of the dino whose limits are being set.
    MaxPercentageOfDesiredNumToAllow : Optional[float]
        The max % this dino can occupy of the container's total population.
    """
    NPCClassString: Optional[str] = None
    MaxPercentageOfDesiredNumToAllow: Optional[float] = None

    def __str__(self) -> str:
        parts = []

        if self.NPCClassString is not None:
            parts.append(f'NPCClassString="{self.NPCClassString}"')

        if self.MaxPercentageOfDesiredNumToAllow is not None:
            parts.append(
                "MaxPercentageOfDesiredNumToAllow="
                f"{self.MaxPercentageOfDesiredNumToAllow:.6f}")

        return f'({",".join(parts)})'

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            NPCClassString=data.get("NPCClassString"),
            MaxPercentageOfDesiredNumToAllow=data.get(
                "MaxPercentageOfDesiredNumToAllow"),
        )


@dataclass
class ConfigAddNPCSpawnEntriesContainer(ComplexValue):
    """
    Represents a configuration override for adding new dino spawn entries to an 
    existing container.

    Parameters
    ----------
    NPCSpawnEntriesContainerClassString : Optional[str]
        The container class being modified.
    NPCSpawnEntries : Optional[list[NPCSpawnEntry]]
        The list of new spawn entries.
    NPCSpawnLimits : Optional[list[NPCSpawnLimit]]
        Population limiters for the entries in this container.
    """
    NPCSpawnEntriesContainerClassString: Optional[str] = None
    NPCSpawnEntries: Optional[list[NPCSpawnEntry]] = field(
        default_factory=list)
    NPCSpawnLimits: Optional[list[NPCSpawnLimit]] = field(
        default_factory=list)

    def __str__(self) -> str:
        parts = []

        if self.NPCSpawnEntriesContainerClassString is not None:
            parts.append(
                'NPCSpawnEntriesContainerClassString='
                f'"{self.NPCSpawnEntriesContainerClassString}"')

        if self.NPCSpawnEntries is not None:
            spawn_entries = ",".join(str(e) for e in self.NPCSpawnEntries)
            parts.append(f'NPCSpawnEntries=({spawn_entries})')

        if self.NPCSpawnLimits is not None:
            spawn_limits = ",".join(str(l) for l in self.NPCSpawnLimits)
            parts.append(f'NPCSpawnLimits=({spawn_limits})')

        return f'({",".join(parts)})'

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        spawn_entries = data.get("NPCSpawnEntries", [])

        if all(isinstance(e, dict) for e in spawn_entries):
            spawn_entries_objs = [
                NPCSpawnEntry.from_dict(e) for e in spawn_entries]
        elif all(isinstance(e, NPCSpawnEntry) for e in spawn_entries):
            spawn_entries_objs = spawn_entries
        else:
            raise ValueError(
                "NPCSpawnEntries attribute must be a list of NPCSpawnEntry "
                "instances or dictionaries representing NPCSpawnEntry")

        spawn_limits = data.get("NPCSpawnLimits", [])

        if all(isinstance(l, dict) for l in spawn_limits):
            spawn_limits_objs = [
                NPCSpawnLimit.from_dict(l) for l in spawn_limits]
        elif all(isinstance(l, NPCSpawnLimit) for l in spawn_limits):
            spawn_limits_objs = spawn_limits
        else:
            raise ValueError(
                "NPCSpawnLimits attribute must be a list of NPCSpawnLimit "
                "instances or dictionaries representing NPCSpawnLimit")

        return cls(
            NPCSpawnEntriesContainerClassString=data.get(
                "NPCSpawnEntriesContainerClassString"),
            NPCSpawnEntries=spawn_entries_objs,
            NPCSpawnLimits=spawn_limits_objs,
        )
