from typing import Optional
from dataclasses import dataclass, field

# pylint: disable=invalid-name


@dataclass
class ItemEntry:
    """
    Represents an item entry.

    Parameters
    ----------
    EntryWeight : Optional[float]
        Probability that this item will be chosen (1.0 = 100%).
    ItemEntryName : Optional[str]
        Name identifier for this item entry.
    Items : Optional[list[str]]
        List of specific item blueprint paths.
    ItemClassStrings : Optional[list[str]]
        List of item class names (alternative to Items).
    ItemsWeights : Optional[list[float]]
        Weights for individual items when multiple are specified.
    MinQuantity : float
        Minimum quantity of this item to spawn (default 1.0).
    MaxQuantity : float
        Maximum quantity of this item to spawn (default 1.0).
    MinQuality : float
        Minimum quality of this item (default 1.0).
    MaxQuality : float
        Maximum quality of this item (default 1.0).
    bForceBlueprint : bool
        Whether to always spawn as blueprint (default False).
    ChanceToBeBlueprintOverride : float
        Chance to spawn as blueprint when bForceBlueprint is False (default 0.0).
    ChanceToActuallyGiveItem : Optional[float]
        Final chance to actually include this item if selected.

    Notes
    -----
    Either Items or ItemClassStrings must be specified, but not both.
    ItemsWeights must match the length of Items or ItemClassStrings if provided.
    """
    EntryWeight: Optional[float] = None
    ItemEntryName: Optional[str] = None
    Items: Optional[list[str]] = None
    ItemClassStrings: Optional[list[str]] = None
    ItemsWeights: Optional[list[float]] = None
    MinQuantity: float = 1.0
    MaxQuantity: float = 1.0
    MinQuality: float = 1.0
    MaxQuality: float = 1.0
    bForceBlueprint: bool = False
    ChanceToBeBlueprintOverride: float = 0.0
    ChanceToActuallyGiveItem: Optional[float] = None

    def __post_init__(self):
        if self.Items is not None and self.ItemClassStrings is not None:
            raise ValueError(
                "ItemEntry cannot have both Items and ItemClassStrings")
        if self.Items is None and self.ItemClassStrings is None:
            raise ValueError(
                "ItemEntry must have either Items or ItemClassStrings")

        if self.ItemsWeights is not None:
            if self.ItemClassStrings is not None:
                expected_items_weights_num = len(self.ItemClassStrings)
            else:
                expected_items_weights_num = len(self.Items)

            if len(self.ItemsWeights) != expected_items_weights_num:
                raise ValueError(
                    "ItemsWeights must have the same length as Items or ItemClassStrings")

    def dump(self) -> str:
        """
        Return the object as a string suitable for use as a value in ARK server 
        configuration INI files.
        """
        parts = []

        if self.EntryWeight is not None:
            parts.append(f"EntryWeight={self.EntryWeight:.6f}")
        if self.ItemEntryName is not None:
            parts.append(f'ItemEntryName="{self.ItemEntryName}"')

        if self.ItemClassStrings is not None:
            item_class_strings = ",".join(
                f"'{s}'" for s in self.ItemClassStrings)
            parts.append(f'ItemClassStrings=({item_class_strings})')
        else:
            items = ",".join(
                f"BlueprintGeneratedClass'{s}'" for s in self.Items)
            parts.append(f'Items=({items})')

        if self.ItemsWeights is not None:
            items_weights = ",".join(f"{w:.6f}" for w in self.ItemsWeights)
            parts.append(f'ItemsWeights=({items_weights})')

        parts.extend([
            f"MinQuantity={self.MinQuantity:.6f}",
            f"MaxQuantity={self.MaxQuantity:.6f}",
            f"MinQuality={self.MinQuality:.6f}",
            f"MaxQuality={self.MaxQuality:.6f}",
            f"bForceBlueprint={self.bForceBlueprint}",
            "ChanceToBeBlueprintOverride="
            f"{self.ChanceToBeBlueprintOverride:.6f}"
        ])

        if self.ChanceToActuallyGiveItem is not None:
            parts.append(
                "ChanceToActuallyGiveItem="
                f"{self.ChanceToActuallyGiveItem:.6f}")

        return f"({','.join(parts)})"


@dataclass
class ItemSet:
    """
    Represents a set of items that can appear in a supply crate.

    Parameters
    ----------
    SetName : Optional[str]
        Name identifier for this item set.
    MinNumItems : Optional[int]
        Minimum number of items to select from this set.
    MaxNumItems : Optional[int]
        Maximum number of items to select from this set.
    NumItemsPower : Optional[float]
        Quality multiplier (recommended to keep at 1.0).
    SetWeight : Optional[float]
        Probability this set will be chosen (1.0 = 100%).
    bItemsRandomWithoutReplacement : Optional[bool]
        Whether to prevent duplicate items from this set.
    ItemEntries : list[ItemEntry]
        List of possible items in this set.

    Notes
    -----
    The actual number of items selected will be between MinNumItems and MaxNumItems.
    """
    SetName: Optional[str] = None
    MinNumItems: Optional[int] = None
    MaxNumItems: Optional[int] = None
    NumItemsPower: Optional[float] = None
    SetWeight: Optional[float] = None
    bItemsRandomWithoutReplacement: Optional[bool] = None
    ItemEntries: list[ItemEntry] = field(default_factory=list)

    def dump(self) -> str:
        """
        Return the object as a string suitable for use as a value in ARK server 
        configuration INI files.
        """
        parts = []

        if self.SetName is not None:
            parts.append(f'SetName="{self.SetName}"')

        if self.MinNumItems is not None:
            parts.append(f"MinNumItems={self.MinNumItems}")

        if self.MaxNumItems is not None:
            parts.append(f"MaxNumItems={self.MaxNumItems}")

        if self.NumItemsPower is not None:
            parts.append(f"NumItemsPower={self.NumItemsPower:.6f}")

        if self.SetWeight is not None:
            parts.append(f"SetWeight={self.SetWeight:.6f}")

        if self.bItemsRandomWithoutReplacement is not None:
            parts.append(
                "bItemsRandomWithoutReplacement="
                f"{self.bItemsRandomWithoutReplacement}")

        item_entries = ",".join(entry.dump() for entry in self.ItemEntries)
        parts.append(f"ItemEntries=({item_entries})")

        return f"({','.join(parts)})"


@dataclass
class Quantity:
    """
    Represents quantity restrictions for an item class.

    Parameters
    ----------
    MaxItemQuantity : int
        Maximum quantity allowed for this item.
    bIgnoreMultiplier : bool
        Whether to ignore global quantity multipliers.
    """
    MaxItemQuantity: int
    bIgnoreMultiplier: bool

    def dump(self) -> str:
        """
        Return the object as a string suitable for use as a value in ARK server 
        configuration INI files.
        """
        return (
            f"("
            f"MaxItemQuantity={self.MaxItemQuantity},"
            f"bIgnoreMultiplier={self.bIgnoreMultiplier}"
            f")"
        )


@dataclass
class ConfigOverrideSupplyCrateItems:
    """
    Configuration override for supply crate items.

    Parameters
    ----------
    SupplyCrateClassString : str
        Class name of the supply crate to modify (e.g., "SupplyCrate_Level03_C").
    MinItemSets : int
        Minimum number of item sets to include.
    MaxItemSets : int
        Maximum number of item sets to include.
    NumItemSetsPower : float
        Quality multiplier (recommended to keep at 1.0).
    bSetsRandomWithoutReplacement : bool
        Whether to prevent duplicate sets.
    ItemSets : list[ItemSet]
        List of possible item sets for this crate.
    bAppendItemSets : Optional[bool]
        Whether to append to existing sets instead of replacing.
    bAppendPreventIncreasingMinMaxItemSets : Optional[bool]
        Whether to prevent increasing min/max when appending.
    """
    SupplyCrateClassString: str
    MinItemSets: int
    MaxItemSets: int
    NumItemSetsPower: float
    bSetsRandomWithoutReplacement: bool
    ItemSets: list[ItemSet]
    bAppendItemSets: Optional[bool] = None
    bAppendPreventIncreasingMinMaxItemSets: Optional[bool] = None

    def dump(self) -> str:
        """
        Return the object as a string suitable for use as a value in ARK server 
        configuration INI files.
        """
        parts = [
            f'SupplyCrateClassString="{self.SupplyCrateClassString}"',
            f"MinItemSets={self.MinItemSets}",
            f"MaxItemSets={self.MaxItemSets}",
            f"NumItemSetsPower={self.NumItemSetsPower:.6f}",
            "bSetsRandomWithoutReplacement="
            f"{self.bSetsRandomWithoutReplacement}"
        ]

        if self.bAppendItemSets is not None:
            parts.append(f"bAppendItemSets={self.bAppendItemSets}")

        item_sets = ",".join(set.dump() for set in self.ItemSets)
        parts.append(f"ItemSets=({item_sets})")

        if self.bAppendPreventIncreasingMinMaxItemSets is not None:
            parts.append(
                "bAppendPreventIncreasingMinMaxItemSets="
                f"{self.bAppendPreventIncreasingMinMaxItemSets}")

        return f"({','.join(parts)})"


@dataclass
class ConfigOverrideItemMaxQuantity:
    """
    Configuration override for maximum item quantities.

    Parameters
    ----------
    ItemClassString : str
        Class name of the item to modify (e.g., "PrimalItemResource_Stone_C").
    Quantity : Quantity
        Quantity restrictions for this item.
    """
    ItemClassString: str
    Quantity: Quantity

    def dump(self) -> str:
        """
        Return the object as a string suitable for use as a value in ARK server 
        configuration INI files.
        """
        quantity = self.Quantity.dump()
        return (
            f"("
            f'ItemClassString="{self.ItemClassString}",'
            f"Quantity={quantity}"
            f")"
        )
