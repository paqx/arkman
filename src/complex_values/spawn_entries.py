from dataclasses import dataclass, field
from typing import Optional, Self

from .complex_value import ComplexValue

# pylint: disable=invalid-name


@dataclass
class NPCsSpawnOffset(ComplexValue):
    """
    Represents a 3D vector offset (X, Y, Z) in Unreal units.

    Parameters
    ----------
    X : float
        Offset along the X axis (Unreal units).
    Y : float
        Offset along the Y axis (Unreal units).
    Z : float
        Offset along the Z axis (Unreal units).

    Example:
    --------
    NPCsSpawnOffsets=(
        (X=0.0, Y=0.0, Z=0.0),
        (X=0.0, Y=250.0, Z=0.0)
    )
    """
    X: float = 0.0
    Y: float = 0.0
    Z: float = 0.0

    def __str__(self) -> str:
        return f'(X={self.X:.1f},Y={self.Y:.1f},Z={self.Z:.1f})'

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            X=data.get("X", 0.0),
            Y=data.get("Y", 0.0),
            Z=data.get("Z", 0.0)
        )


@dataclass
class NPCDifficultyLevelRange(ComplexValue):
    """
    Represents a difficulty entry for NPCs spawned by an NPCSpawnEntry.

    Parameters
    ----------
    EnemyLevelsMin : List[float]
        The minimum base levels for the dino(s).
    EnemyLevelsMax : List[float]
        The maximum base levels for the dino(s).
    GameDifficulties : List[float]
        The difficulty offsets for each corresponding range.

    Example:
    --------
    NPCDifficultyLevelRanges=(
        (
            EnemyLevelsMin=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
            EnemyLevelsMax=(30.0, 30.0, 30.0, 30.0, 30.0, 30.0),
            GameDifficulties=(0.0, 1.0, 2.0, 3.0, 4.0, 5.0)
        )
    )
    """
    EnemyLevelsMin: list[float] = field(default_factory=list)
    EnemyLevelsMax: list[float] = field(default_factory=list)
    GameDifficulties: list[float] = field(default_factory=list)

    def __str__(self) -> str:
        min_levels = ",".join(f"{x:.1f}" for x in self.EnemyLevelsMin)
        max_levels = ",".join(f"{x:.1f}" for x in self.EnemyLevelsMax)
        difficulties = ",".join(f"{x:.1f}" for x in self.GameDifficulties)
        return (
            "("
            f"EnemyLevelsMin=({min_levels}),"
            f"EnemyLevelsMax=({max_levels}),"
            f"GameDifficulties=({difficulties})"
            ")"
        )

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            EnemyLevelsMin=data.get("EnemyLevelsMin", []),
            EnemyLevelsMax=data.get("EnemyLevelsMax", []),
            GameDifficulties=data.get("GameDifficulties", []),
        )


@dataclass
class NPCSpawnEntry(ComplexValue):
    """
    Represents an individual spawn entry for a dino in a spawn container.

    Parameters
    ----------
    AnEntryName : Optional[str]
        Unique name for this spawn entry.
    NPCsToSpawnStrings : Optional[list[str]]
        List of dino class strings to spawn.
    NPCsSpawnOffsets : Optional[list[NPCsSpawnOffset]]
        Sets the offset in Unreal units from the spawn point.
    NPCsToSpawnPercentageChance : Optional[list[float]]
        Sets the probability (0.0-1.0) for each dino in this entry to spawn.
    EntryWeight : Optional[float]
        The relative probability (0.0-1.0) that this entry will be selected.
    ManualSpawnPointSpreadRadius : Optional[float]
        Sets the group spawn radius in Unreal units.
    NPCDifficultyLevelRanges : Optional[list[NPCDifficultyLevelRange]]
        List of difficulty/level ranges for each dino spawned in this entry.
    RandGroupSpawnOffsetZMin : Optional[float]
        Sets the minimum offset in Z (vertical) for spawn group (Unreal units).
    RandGroupSpawnOffsetZMax : Optional[float]
        Sets the maximum offset in Z (vertical) for spawn group (Unreal units).
    NPCOverrideLevel : Optional[list[int]]
        Forces specific spawn levels for each spawned dino.
    NPCMinLevelOffset : Optional[list[float]]
        Offset added to the minimum spawn level.
    NPCMaxLevelOffset : Optional[list[float]]
        Offset added to the maximum spawn level.
    NPCMinLevelMultiplier : Optional[list[float]]
        Multiplier for minimum spawn level.
    NPCMaxLevelMultiplier : Optional[list[float]]
        Multiplier for maximum spawn level.
    bAddLevelOffsetBeforeMultiplier : Optional[int]
        If 1, add level offsets before applying multipliers (default: 0).

    Examples & Descriptions
    -----------------------
    - Set spawn distance:
        NPCsSpawnOffsets=(
            (X=0.0, Y=0.0, Z=0.0),
            (X=0.0, Y=250.0, Z=0.0)
        )
        # Each tuple sets offset from spawn point

    - Set per-entry spawn chance:
        NPCsToSpawnPercentageChance=(1.0, 0.5)
        # Probability 1.0 for first, 0.5 for second dino

    - Set group spread radius:
        ManualSpawnPointSpreadRadius=650.0

    - Set difficulty/level ranges:
        NPCDifficultyLevelRanges=(
            (
                EnemyLevelsMin=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0), 
                EnemyLevelsMax=(30.0, 30.0, 30.0, 30.0, 30.0, 30.0), 
                GameDifficulties=(0.0, 1.0, 2.0, 3.0, 4.0, 5.0)
            ),
            (
                EnemyLevelsMin=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0), 
                EnemyLevelsMax=(30.0, 30.0, 30.0, 30.0, 30.0, 30.0), 
                GameDifficulties=(0.0, 1.0, 2.0, 3.0, 4.0, 5.0)
            )
        )

    - Set spawn Z height offsets (useful for flyers, water creatures):
        RandGroupSpawnOffsetZMin=1200.0
        RandGroupSpawnOffsetZMax=5000.0

    - Override levels (force "Parasaur at level 1"):
        NPCOverrideLevel=(1)

    - Set all to spawn at max level and adjust offsets:
        NPCOverrideLevel=(1)
        NPCMinLevelOffset=(30.0)
        NPCMaxLevelOffset=(30.0)

    - Double max level change:
        NPCMinLevelMultiplier=(1.0)
        NPCMaxLevelMultiplier=(2.0)

    - Increase minimum level by 150 and double:
        bAddLevelOffsetBeforeMultiplier=1
        NPCMinLevelOffset=(30.0)
        NPCMaxLevelOffset=(30.0)
        NPCMinLevelMultiplier=(1.0)
        NPCMaxLevelMultiplier=(2.0)
    """
    AnEntryName: Optional[str] = None
    NPCsToSpawnStrings: Optional[list[str]] = None
    NPCsSpawnOffsets: Optional[list[NPCsSpawnOffset]] = None
    NPCsToSpawnPercentageChance: Optional[list[float]] = None
    EntryWeight: Optional[float] = None
    ManualSpawnPointSpreadRadius: Optional[float] = None
    NPCDifficultyLevelRanges: Optional[list[NPCDifficultyLevelRange]] = None
    RandGroupSpawnOffsetZMin: Optional[float] = None
    RandGroupSpawnOffsetZMax: Optional[float] = None
    NPCOverrideLevel: Optional[list[int]] = None
    NPCMinLevelOffset: Optional[list[float]] = None
    NPCMaxLevelOffset: Optional[list[float]] = None
    NPCMinLevelMultiplier: Optional[list[float]] = None
    NPCMaxLevelMultiplier: Optional[list[float]] = None
    bAddLevelOffsetBeforeMultiplier: Optional[int] = None

    def __str__(self) -> str:
        parts = []

        if self.AnEntryName is not None:
            parts.append(f'AnEntryName="{self.AnEntryName}"')

        if self.NPCsToSpawnStrings is not None:
            npcs = ",".join(f'"{s}"' for s in self.NPCsToSpawnStrings)
            parts.append(f'NPCsToSpawnStrings=({npcs})')

        if self.NPCsSpawnOffsets is not None:
            offsets = ",".join(f'"{o}"' for o in self.NPCsSpawnOffsets)
            parts.append(f'NPCsSpawnOffsets=({offsets})')

        if self.NPCsToSpawnPercentageChance is not None:
            chance = ",".join(
                f"{c:.3f}" for c in self.NPCsToSpawnPercentageChance)
            parts.append(f'NPCsToSpawnPercentageChance=({chance})')

        if self.EntryWeight is not None:
            parts.append(f'EntryWeight={self.EntryWeight:.6f}')

        if self.ManualSpawnPointSpreadRadius is not None:
            parts.append(
                'ManualSpawnPointSpreadRadius='
                f'{self.ManualSpawnPointSpreadRadius:.1f}')

        if self.NPCDifficultyLevelRanges is not None:
            ranges = ",".join(
                f"{r}" for r in self.NPCDifficultyLevelRanges)
            parts.append(f'NPCDifficultyLevelRanges=({ranges})')

        if self.RandGroupSpawnOffsetZMin is not None:
            parts.append(
                f'RandGroupSpawnOffsetZMin={self.RandGroupSpawnOffsetZMin:.1f}')

        if self.RandGroupSpawnOffsetZMax is not None:
            parts.append(
                f'RandGroupSpawnOffsetZMax={self.RandGroupSpawnOffsetZMax:.1f}')

        if self.NPCOverrideLevel is not None:
            level = ",".join(l for l in self.NPCOverrideLevel)
            parts.append(f'NPCOverrideLevel=({level})')

        if self.NPCMinLevelOffset is not None:
            offset = ",".join(f"{x:.1f}" for x in self.NPCMinLevelOffset)
            parts.append(f'NPCMinLevelOffset=({offset})')

        if self.NPCMaxLevelOffset is not None:
            offset = ",".join(f"{x:.1f}" for x in self.NPCMaxLevelOffset)
            parts.append(f'NPCMaxLevelOffset=({offset})')

        if self.NPCMinLevelMultiplier is not None:
            mult = ",".join(f"{x:.1f}" for x in self.NPCMinLevelMultiplier)
            parts.append(f'NPCMinLevelMultiplier=({mult})')

        if self.NPCMaxLevelMultiplier is not None:
            mult = ",".join(f"{x:.1f}" for x in self.NPCMaxLevelMultiplier)
            parts.append(f'NPCMaxLevelMultiplier=({mult})')

        if self.bAddLevelOffsetBeforeMultiplier is not None:
            parts.append(
                'bAddLevelOffsetBeforeMultiplier='
                f'{self.bAddLevelOffsetBeforeMultiplier}')

        return f'({",".join(parts)})'

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        spawn_offsets = data.get("NPCsSpawnOffsets", [])

        if all(isinstance(o, dict) for o in spawn_offsets):
            spawn_offsets_objs = [NPCsSpawnOffset.from_dict(
                o) for o in spawn_offsets]
        elif all(isinstance(o, NPCsSpawnOffset) for o in spawn_offsets):
            spawn_offsets_objs = spawn_offsets
        else:
            raise ValueError(
                "NPCsSpawnOffsets attribute must be a list of NPCsSpawnOffsets "
                " instances or a list of dictionaries representing "
                f"NPCsSpawnOffsets, not {type(spawn_offsets)}")

        difficulty_ranges = data.get("NPCDifficultyLevelRanges", [])

        if all(isinstance(r, dict) for r in difficulty_ranges):
            difficulty_ranges_objs = [
                NPCDifficultyLevelRange.from_dict(r) for r in difficulty_ranges]
        elif all(isinstance(r, NPCDifficultyLevelRange) for r in difficulty_ranges):
            difficulty_ranges_objs = difficulty_ranges
        else:
            raise ValueError(
                "NPCDifficultyLevelRanges must be a list of "
                "NPCDifficultyLevelRange instances or dictionaries, not "
                f"{type(difficulty_ranges)}"
            )

        return cls(
            AnEntryName=data.get("AnEntryName"),
            NPCsToSpawnStrings=data.get("NPCsToSpawnStrings"),
            NPCsSpawnOffsets=spawn_offsets_objs,
            NPCsToSpawnPercentageChance=data.get(
                "NPCsToSpawnPercentageChance"),
            EntryWeight=data.get("EntryWeight"),
            ManualSpawnPointSpreadRadius=data.get(
                "ManualSpawnPointSpreadRadius"),
            NPCDifficultyLevelRanges=difficulty_ranges_objs,
            RandGroupSpawnOffsetZMin=data.get("RandGroupSpawnOffsetZMin"),
            RandGroupSpawnOffsetZMax=data.get("RandGroupSpawnOffsetZMax"),
            NPCOverrideLevel=data.get("NPCOverrideLevel"),
            NPCMinLevelOffset=data.get("NPCMinLevelOffset"),
            NPCMaxLevelOffset=data.get("NPCMaxLevelOffset"),
            NPCMinLevelMultiplier=data.get("NPCMinLevelMultiplier"),
            NPCMaxLevelMultiplier=data.get("NPCMaxLevelMultiplier"),
            bAddLevelOffsetBeforeMultiplier=data.get(
                "bAddLevelOffsetBeforeMultiplier"),
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


@dataclass
class DinoSpawnWeightMultiplier(ComplexValue):
    """
    Represents a configuration entry that customizes the spawning rate
    for a specific creature type.

    Parameters
    ----------
    DinoNameTag : str
        Creature tag to adjust.
    SpawnWeightMultiplier : Optional[float]
        Weight factor for this type. Higher values increase spawn frequency.
    OverrideSpawnLimitPercentage : Optional[bool]
        If True, use the specified SpawnLimitPercentage.
    SpawnLimitPercentage : Optional[float]
        Maximum percentage among all spawns for this type within a spawn region.
    """
    DinoNameTag: str
    SpawnWeightMultiplier: Optional[float] = None
    OverrideSpawnLimitPercentage: Optional[bool] = None
    SpawnLimitPercentage: Optional[float] = None

    def __str__(self) -> str:
        parts = [f'DinoNameTag={self.DinoNameTag}']

        if self.SpawnWeightMultiplier is not None:
            parts.append(f'SpawnWeightMultiplier={self.SpawnWeightMultiplier}')

        if self.OverrideSpawnLimitPercentage is not None:
            parts.append(
                'OverrideSpawnLimitPercentage='
                f'{self.OverrideSpawnLimitPercentage}')

        if self.SpawnLimitPercentage is not None:
            parts.append(f'SpawnLimitPercentage={self.SpawnLimitPercentage}')

        return f'({",".join(parts)})'

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            DinoNameTag=data['DinoNameTag'],
            SpawnWeightMultiplier=data.get('SpawnWeightMultiplier'),
            OverrideSpawnLimitPercentage=data.get(
                'OverrideSpawnLimitPercentage'),
            SpawnLimitPercentage=data.get('SpawnLimitPercentage')
        )
