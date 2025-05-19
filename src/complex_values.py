from abc import ABC, abstractmethod
from typing import Optional, Self
from dataclasses import dataclass, field

# pylint: disable=invalid-name


@dataclass
class ItemEntry:
    """
    Represents an item entry in a supply crate.

    Parameters
    ----------
    ItemEntryName : Optional[str]
        Name identifier for this item entry.
    EntryWeight : Optional[float]
        Probability that this item will be chosen (1.0 = 100%).
    Items : Optional[list[str]]
        List of specific item blueprint paths.
    ItemClassStrings : Optional[list[str]]
        List of item class names.
    ItemsWeights : Optional[list[float]]
        Weights for individual items when multiple are specified.
    ItemsMinQuantities : Optional[list[float]]
        Minimum quantities for individual items when multiple are specified.
    ItemsMaxQuantities : Optional[list[float]]
        Maximum quantities for individual items when multiple are specified.
    GiveRequiresMinimumCharacterLevel : Optional[int]
        Minimum character level required to receive this item.
    GiveExtraItemQuantityPercentByOwnerCharacterLevel : Optional[float]
        Extra item quantity percentage based on owner's character level.
    MinQuantity : float
        Minimum quantity of this item to spawn (default 1.0).
    MaxQuantity : float
        Maximum quantity of this item to spawn (default 1.0).
    QuantityPower : float
        Power value for quantity distribution (default 1.0).
    MinQuality : float
        Minimum quality of this item (default 1.0).
    MaxQuality : float
        Maximum quality of this item (default 1.0).
    QualityPower : float
        Power value for quality distribution (default 1.0).
    bForceBlueprint : bool
        Whether to always spawn as blueprint (default False).
    ChanceToBeBlueprintOverride : float
        Chance to spawn as blueprint when bForceBlueprint is False (default 0.0).
    ChanceToActuallyGiveItem : Optional[float]
        Final chance to actually include this item if selected.
    RequiresMinQuality : Optional[float]
        Minimum required quality to receive this item.
    bActualItemRandomWithoutReplacement : bool
        Whether to select items randomly without replacement (default False).
    """
    ItemEntryName: Optional[str] = None
    EntryWeight: Optional[float] = None
    Items: Optional[list[str]] = None
    ItemClassStrings: Optional[list[str]] = None
    ItemsWeights: Optional[list[float]] = None
    ItemsMinQuantities: Optional[list[float]] = None
    ItemsMaxQuantities: Optional[list[float]] = None
    GiveRequiresMinimumCharacterLevel: Optional[int] = None
    GiveExtraItemQuantityPercentByOwnerCharacterLevel: Optional[float] = None
    MinQuantity: float = 1.0
    MaxQuantity: float = 1.0
    QuantityPower: float = 1.0
    MinQuality: float = 1.0
    MaxQuality: float = 1.0
    QualityPower: float = 1.0
    bForceBlueprint: bool = False
    ChanceToBeBlueprintOverride: float = 0.0
    ChanceToActuallyGiveItem: Optional[float] = None
    RequiresMinQuality: Optional[float] = None
    bActualItemRandomWithoutReplacement: bool = False

    def __post_init__(self):
        if not self.Items and not self.ItemClassStrings:
            raise ValueError(
                "ItemEntry must have Items or ItemClassStrings")

    def __str__(self) -> str:
        """
        Return the object as a string suitable for use as a value in ARK server 
        configuration INI files.
        """
        parts = []

        if self.ItemEntryName is not None:
            parts.append(f'ItemEntryName="{self.ItemEntryName}"')

        if self.EntryWeight is not None:
            parts.append(f"EntryWeight={self.EntryWeight}")

        if self.ItemClassStrings is not None:
            item_class_strings = ",".join(
                f"'{s}'" for s in self.ItemClassStrings)
            parts.append(f'ItemClassStrings=({item_class_strings})')

        if self.Items is not None:
            items = ",".join(
                f"BlueprintGeneratedClass'{i}'" for i in self.Items)
            parts.append(f'Items=({items})')

        if self.ItemsWeights is not None:
            items_weights = ",".join(f"{iw}" for iw in self.ItemsWeights)
            parts.append(f'ItemsWeights=({items_weights})')

        if self.ItemsMinQuantities is not None:
            items_min_quantities = ",".join(
                f"{q}" for q in self.ItemsMinQuantities)
            parts.append(f'ItemsMinQuantities=({items_min_quantities})')

        if self.ItemsMaxQuantities is not None:
            items_max_quantities = ",".join(
                f"{q}" for q in self.ItemsMaxQuantities)
            parts.append(f'ItemsMaxQuantities=({items_max_quantities})')

        if self.GiveRequiresMinimumCharacterLevel is not None:
            parts.append(
                f"GiveRequiresMinimumCharacterLevel={self.GiveRequiresMinimumCharacterLevel}")

        if self.GiveExtraItemQuantityPercentByOwnerCharacterLevel is not None:
            parts.append(
                "GiveExtraItemQuantityPercentByOwnerCharacterLevel="
                f"{self.GiveExtraItemQuantityPercentByOwnerCharacterLevel}")

        parts.extend([
            f"MinQuantity={self.MinQuantity}",
            f"MaxQuantity={self.MaxQuantity}",
            f"QuantityPower={self.QuantityPower}",
            f"MinQuality={self.MinQuality}",
            f"MaxQuality={self.MaxQuality}",
            f"QualityPower={self.QualityPower}",
            f"bForceBlueprint={self.bForceBlueprint}",
            f"ChanceToBeBlueprintOverride={self.ChanceToBeBlueprintOverride}"
        ])

        if self.ChanceToActuallyGiveItem is not None:
            parts.append(
                f"ChanceToActuallyGiveItem={self.ChanceToActuallyGiveItem}")

        if self.RequiresMinQuality is not None:
            parts.append(f"RequiresMinQuality={self.RequiresMinQuality}")

        parts.append(
            "bActualItemRandomWithoutReplacement="
            f"{self.bActualItemRandomWithoutReplacement}")

        return f"({','.join(parts)})"

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create an instance of ItemEntry from a dictionary."""
        return cls(
            ItemEntryName=data.get("ItemEntryName"),
            EntryWeight=data.get("EntryWeight"),
            Items=data.get("Items"),
            ItemClassStrings=data.get("ItemClassStrings"),
            ItemsWeights=data.get("ItemsWeights"),
            ItemsMinQuantities=data.get("ItemsMinQuantities"),
            ItemsMaxQuantities=data.get("ItemsMaxQuantities"),
            GiveRequiresMinimumCharacterLevel=data.get(
                "GiveRequiresMinimumCharacterLevel"),
            GiveExtraItemQuantityPercentByOwnerCharacterLevel=data.get(
                "GiveExtraItemQuantityPercentByOwnerCharacterLevel"
            ),
            MinQuantity=data.get("MinQuantity", 1.0),
            MaxQuantity=data.get("MaxQuantity", 1.0),
            QuantityPower=data.get("QuantityPower", 1.0),
            MinQuality=data.get("MinQuality", 1.0),
            MaxQuality=data.get("MaxQuality", 1.0),
            QualityPower=data.get("QualityPower", 1.0),
            bForceBlueprint=data.get("bForceBlueprint", False),
            ChanceToBeBlueprintOverride=data.get(
                "ChanceToBeBlueprintOverride", 0.0),
            ChanceToActuallyGiveItem=data.get("ChanceToActuallyGiveItem"),
            RequiresMinQuality=data.get("RequiresMinQuality"),
            bActualItemRandomWithoutReplacement=data.get(
                "bActualItemRandomWithoutReplacement", False
            ),
        )


@dataclass
class ItemSet:
    """
    Represents a set of items that can appear in a supply crate.

    Parameters
    ----------
    SetName : Optional[str]
        Name identifier for this item set.
    ItemEntries : list[ItemEntry]
        List of possible items in this set.
    MinNumItems : Optional[float]
        Minimum number of items to select from this set.
    MaxNumItems : Optional[float]
        Maximum number of items to select from this set.
    NumItemsPower : Optional[float]
        Quality multiplier (recommended to keep at 1.0).
    SetWeight : Optional[float]
        Probability this set will be chosen (1.0 = 100%).
    bItemsRandomWithoutReplacement : Optional[bool]
        Whether to prevent duplicate items from this set.

    Notes
    -----
    The actual number of items selected will be between MinNumItems and MaxNumItems.
    """
    SetName: Optional[str] = None
    ItemEntries: list[ItemEntry] = field(default_factory=list)
    MinNumItems: Optional[float] = None
    MaxNumItems: Optional[float] = None
    NumItemsPower: Optional[float] = 1.0
    SetWeight: Optional[float] = None
    bItemsRandomWithoutReplacement: Optional[bool] = None

    def __str__(self) -> str:
        """
        Return the object as a string suitable for use as a value in ARK server 
        configuration INI files.
        """
        parts = []

        if self.SetName is not None:
            parts.append(f'SetName="{self.SetName}"')

        item_entries = ",".join(f"{entry}" for entry in self.ItemEntries)
        parts.append(f"ItemEntries=({item_entries})")

        if self.MinNumItems is not None:
            parts.append(f"MinNumItems={self.MinNumItems}")

        if self.MaxNumItems is not None:
            parts.append(f"MaxNumItems={self.MaxNumItems}")

        if self.NumItemsPower is not None:
            parts.append(f"NumItemsPower={self.NumItemsPower}")

        if self.SetWeight is not None:
            parts.append(f"SetWeight={self.SetWeight}")

        if self.bItemsRandomWithoutReplacement is not None:
            parts.append(
                "bItemsRandomWithoutReplacement="
                f"{self.bItemsRandomWithoutReplacement}")

        return f"({','.join(parts)})"

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create an instance of ItemSet from a dictionary."""
        item_entries = data.get("ItemEntries", [])

        if all(isinstance(item, dict) for item in item_entries):
            item_entries_list = [ItemEntry.from_dict(
                item_entry) for item_entry in item_entries]
        elif all(isinstance(item, ItemEntry) for item in item_entries):
            item_entries_list = item_entries
        else:
            raise ValueError(
                "ItemEntries must be a list of ItemEntries instances or "
                "dictionaries"
            )

        return cls(
            SetName=data.get("SetName"),
            ItemEntries=item_entries_list,
            MinNumItems=data.get("MinNumItems"),
            MaxNumItems=data.get("MaxNumItems"),
            NumItemsPower=data.get("NumItemsPower", 1.0),
            SetWeight=data.get("SetWeight"),
            bItemsRandomWithoutReplacement=data.get(
                "bItemsRandomWithoutReplacement")
        )


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

    def __str__(self) -> str:
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

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create an instance of Quantity from a dictionary."""
        return cls(
            MaxItemQuantity=data["MaxItemQuantity"],
            bIgnoreMultiplier=data["bIgnoreMultiplier"]
        )


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


@dataclass
class ConfigOverrideSupplyCrateItems(ComplexValue):
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

    def __str__(self) -> str:
        """
        Return the object as a string suitable for use as a value in ARK server 
        configuration INI files.
        """
        parts = [
            f'SupplyCrateClassString="{self.SupplyCrateClassString}"',
            f"MinItemSets={self.MinItemSets}",
            f"MaxItemSets={self.MaxItemSets}",
            f"NumItemSetsPower={self.NumItemSetsPower}",
            "bSetsRandomWithoutReplacement="
            f"{self.bSetsRandomWithoutReplacement}"
        ]

        if self.bAppendItemSets is not None:
            parts.append(f"bAppendItemSets={self.bAppendItemSets}")

        item_sets = ",".join(f"{item_set}" for item_set in self.ItemSets)
        parts.append(f"ItemSets=({item_sets})")

        if self.bAppendPreventIncreasingMinMaxItemSets is not None:
            parts.append(
                "bAppendPreventIncreasingMinMaxItemSets="
                f"{self.bAppendPreventIncreasingMinMaxItemSets}")

        return f"({','.join(parts)})"

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """
        Create an instance of ConfigOverrideSupplyCrateItems from a dictionary."""
        item_sets = data["ItemSets"]

        if all(isinstance(item, dict) for item in item_sets):
            item_sets_list = [ItemSet.from_dict(
                item_set) for item_set in item_sets]
        elif all(isinstance(item, ItemSet) for item in item_sets):
            item_sets_list = item_sets
        else:
            raise ValueError(
                "ItemSets attribute must be a list of ItemSet instances or a "
                f"list of dictionaries representing ItemSet, "
                f"not {type(item_sets)}")

        return cls(
            SupplyCrateClassString=data["SupplyCrateClassString"],
            MinItemSets=data["MinItemSets"],
            MaxItemSets=data["MaxItemSets"],
            NumItemSetsPower=data["NumItemSetsPower"],
            bSetsRandomWithoutReplacement=data["bSetsRandomWithoutReplacement"],
            ItemSets=item_sets_list,
            bAppendItemSets=data.get("bAppendItemSets"),
            bAppendPreventIncreasingMinMaxItemSets=data.get(
                "bAppendPreventIncreasingMinMaxItemSets"),
        )


@dataclass
class ConfigOverrideItemMaxQuantity(ComplexValue):
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

    def __str__(self) -> str:
        """
        Return the object as a string suitable for use as a value in ARK server 
        configuration INI files.
        """
        return (
            f"("
            f'ItemClassString="{self.ItemClassString}",'
            f"Quantity={self.Quantity}"
            f")"
        )

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """
        Create an instance of ConfigOverrideItemMaxQuantity from a dictionary."""
        quantity = data["Quantity"]

        if isinstance(quantity, dict):
            quantity_obj = Quantity.from_dict(quantity)
        elif isinstance(quantity, Quantity):
            quantity_obj = quantity
        else:
            raise ValueError(
                "Quantity attribute must be a Quantity instance or a "
                f"dictionary representing Quantity, not {type(quantity)}."
            )
        return cls(
            ItemClassString=data["ItemClassString"],
            Quantity=quantity_obj
        )
