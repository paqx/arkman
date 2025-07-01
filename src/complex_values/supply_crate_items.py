from typing import Optional, Self
from dataclasses import dataclass, field

from .complex_value import ComplexValue

# pylint: disable=invalid-name


@dataclass
class ItemEntry(ComplexValue):
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
    MinQuantity : Optional[float]
        Minimum quantity of this item to spawn.
    MaxQuantity : Optional[float]
        Maximum quantity of this item to spawn.
    QuantityPower : Optional[float]
        Power value for quantity distribution.
    MinQuality : Optional[float]
        Minimum quality of this item.
    MaxQuality : Optional[float]
        Maximum quality of this item.
    QualityPower : Optional[float]
        Power value for quality distribution.
    bForceBlueprint : Optional[bool]
        Whether to always spawn as blueprint.
    ChanceToBeBlueprintOverride : Optional[float]
        Chance to spawn as blueprint when bForceBlueprint is False.
    ChanceToActuallyGiveItem : Optional[float]
        Final chance to actually include this item if selected.
    RequiresMinQuality : Optional[float]
        Minimum required quality to receive this item.
    bActualItemRandomWithoutReplacement : Optional[bool]
        Whether to select items randomly without replacement.
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
    MinQuantity: Optional[float] = None
    MaxQuantity: Optional[float] = None
    QuantityPower: Optional[float] = None
    MinQuality: Optional[float] = None
    MaxQuality: Optional[float] = None
    QualityPower: Optional[float] = None
    bForceBlueprint: Optional[bool] = None
    ChanceToBeBlueprintOverride: Optional[float] = None
    ChanceToActuallyGiveItem: Optional[float] = None
    RequiresMinQuality: Optional[float] = None
    bActualItemRandomWithoutReplacement: Optional[bool] = None

    def __str__(self) -> str:
        parts = []

        if self.ItemEntryName is not None:
            parts.append(f'ItemEntryName="{self.ItemEntryName}"')

        if self.EntryWeight is not None:
            parts.append(f"EntryWeight={self.EntryWeight:.6f}")

        if self.Items is not None:
            items = ",".join(
                f"BlueprintGeneratedClass'{i}'" for i in self.Items)
            parts.append(f'Items=({items})')

        if self.ItemClassStrings is not None:
            item_class_strings = ",".join(
                f"'{s}'" for s in self.ItemClassStrings)
            parts.append(f'ItemClassStrings=({item_class_strings})')

        if self.ItemsWeights is not None:
            items_weights = ",".join(f"{iw:.6f}" for iw in self.ItemsWeights)
            parts.append(f'ItemsWeights=({items_weights})')

        if self.ItemsMinQuantities is not None:
            items_min_quantities = ",".join(
                f"{q:.6f}" for q in self.ItemsMinQuantities)
            parts.append(f'ItemsMinQuantities=({items_min_quantities})')

        if self.ItemsMaxQuantities is not None:
            items_max_quantities = ",".join(
                f"{q:.6f}" for q in self.ItemsMaxQuantities)
            parts.append(f'ItemsMaxQuantities=({items_max_quantities})')

        if self.GiveRequiresMinimumCharacterLevel is not None:
            parts.append(
                "GiveRequiresMinimumCharacterLevel="
                f"{self.GiveRequiresMinimumCharacterLevel}")

        if self.GiveExtraItemQuantityPercentByOwnerCharacterLevel is not None:
            parts.append(
                "GiveExtraItemQuantityPercentByOwnerCharacterLevel="
                f"{self.GiveExtraItemQuantityPercentByOwnerCharacterLevel:.6f}")

        if self.MinQuantity is not None:
            parts.append(f"MinQuantity={self.MinQuantity:.6f}")

        if self.MaxQuantity is not None:
            parts.append(f"MaxQuantity={self.MaxQuantity:.6f}")

        if self.QuantityPower is not None:
            parts.append(f"QuantityPower={self.QuantityPower:.6f}")

        if self.MinQuality is not None:
            parts.append(f"MinQuality={self.MinQuality:.6f}")

        if self.MaxQuality is not None:
            parts.append(f"MaxQuality={self.MaxQuality:.6f}")

        if self.QualityPower is not None:
            parts.append(f"QualityPower={self.QualityPower:.6f}")

        if self.bForceBlueprint is not None:
            parts.append(f"bForceBlueprint={self.bForceBlueprint}")

        if self.ChanceToBeBlueprintOverride is not None:
            parts.append(
                f"ChanceToBeBlueprintOverride={self.ChanceToBeBlueprintOverride:.6f}")

        if self.ChanceToActuallyGiveItem is not None:
            parts.append(
                f"ChanceToActuallyGiveItem={self.ChanceToActuallyGiveItem:.6f}")

        if self.RequiresMinQuality is not None:
            parts.append(f"RequiresMinQuality={self.RequiresMinQuality:.6f}")

        if self.bActualItemRandomWithoutReplacement is not None:
            parts.append(
                "bActualItemRandomWithoutReplacement="
                f"{self.bActualItemRandomWithoutReplacement}")

        return f"({','.join(parts)})"

    @classmethod
    def from_dict(cls, data: dict) -> Self:
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
            MinQuantity=data.get("MinQuantity"),
            MaxQuantity=data.get("MaxQuantity"),
            QuantityPower=data.get("QuantityPower"),
            MinQuality=data.get("MinQuality"),
            MaxQuality=data.get("MaxQuality"),
            QualityPower=data.get("QualityPower"),
            bForceBlueprint=data.get("bForceBlueprint"),
            ChanceToBeBlueprintOverride=data.get(
                "ChanceToBeBlueprintOverride"),
            ChanceToActuallyGiveItem=data.get("ChanceToActuallyGiveItem"),
            RequiresMinQuality=data.get("RequiresMinQuality"),
            bActualItemRandomWithoutReplacement=data.get(
                "bActualItemRandomWithoutReplacement"
            ),
        )


@dataclass
class ItemSet(ComplexValue):
    """
    Represents a set of items that can appear in a supply crate.

    Parameters
    ----------
    SetName : Optional[str]
        Name identifier for this item set.
    ItemEntries : Optional[list[ItemEntry]]
        List of possible items in this set.
    SetWeight : Optional[float]
        Probability this set will be chosen (1.0 = 100%).
    MinNumItems : Optional[float]
        Minimum number of items to select from this set.
    MaxNumItems : Optional[float]
        Maximum number of items to select from this set.
    NumItemsPower : Optional[float]
        Quality multiplier (recommended to keep at 1.0).
    bItemsRandomWithoutReplacement : Optional[bool]
        Whether to prevent duplicate items from this set.

    Notes
    -----
    The actual number of items selected will be between MinNumItems and MaxNumItems.
    """
    SetName: Optional[str] = None
    ItemEntries: Optional[list[ItemEntry]] = field(default_factory=list)
    SetWeight: Optional[float] = None
    MinNumItems: Optional[float] = None
    MaxNumItems: Optional[float] = None
    NumItemsPower: Optional[float] = None
    bItemsRandomWithoutReplacement: Optional[bool] = None

    def __str__(self) -> str:
        parts = []

        if self.SetName is not None:
            parts.append(f'SetName="{self.SetName}"')

        if self.ItemEntries is not None:
            item_entries = ",".join(f"{entry}" for entry in self.ItemEntries)
            parts.append(f"ItemEntries=({item_entries})")

        if self.SetWeight is not None:
            parts.append(f"SetWeight={self.SetWeight:.6f}")

        if self.MinNumItems is not None:
            parts.append(f"MinNumItems={self.MinNumItems:.6f}")

        if self.MaxNumItems is not None:
            parts.append(f"MaxNumItems={self.MaxNumItems:.6f}")

        if self.NumItemsPower is not None:
            parts.append(f"NumItemsPower={self.NumItemsPower:.6f}")

        if self.bItemsRandomWithoutReplacement is not None:
            parts.append(
                "bItemsRandomWithoutReplacement="
                f"{self.bItemsRandomWithoutReplacement}")

        return f"({','.join(parts)})"

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        item_entries = data.get("ItemEntries", [])

        if all(isinstance(item, dict) for item in item_entries):
            item_entries_objs = [ItemEntry.from_dict(
                item_entry) for item_entry in item_entries]
        elif all(isinstance(item, ItemEntry) for item in item_entries):
            item_entries_objs = item_entries
        else:
            raise ValueError(
                "ItemEntries must be a list of ItemEntries instances or "
                "dictionaries"
            )

        item_entries_objs = item_entries_objs if item_entries_objs else None

        return cls(
            SetName=data.get("SetName"),
            ItemEntries=item_entries_objs,
            SetWeight=data.get("SetWeight"),
            MinNumItems=data.get("MinNumItems"),
            MaxNumItems=data.get("MaxNumItems"),
            NumItemsPower=data.get("NumItemsPower"),
            bItemsRandomWithoutReplacement=data.get(
                "bItemsRandomWithoutReplacement")
        )


@dataclass
class ConfigOverrideSupplyCrateItems(ComplexValue):
    """
    Configuration override for supply crate items.

    Parameters
    ----------
    SupplyCrateClassString : Optional[str]
        Class name of the supply crate to modify (e.g., "SupplyCrate_Level03_C").
    MinItemSets : Optional[int]
        Minimum number of item sets to include.
    MaxItemSets : Optional[int]
        Maximum number of item sets to include.
    NumItemSetsPower : Optional[float]
        Quality multiplier (recommended to keep at 1.0).
    bSetsRandomWithoutReplacement : Optional[bool]
        Whether to prevent duplicate sets.
    ItemSets : Optional[list[ItemSet]]
        List of possible item sets for this crate.
    bAppendItemSets : Optional[bool]
        Whether to append to existing sets instead of replacing.
    bAppendPreventIncreasingMinMaxItemSets : Optional[bool]
        Whether to prevent increasing min/max when appending.
    """
    SupplyCrateClassString: Optional[str] = None
    MinItemSets: Optional[int] = None
    MaxItemSets: Optional[int] = None
    NumItemSetsPower: Optional[float] = None
    bSetsRandomWithoutReplacement: Optional[bool] = None
    ItemSets: Optional[list[ItemSet]] = field(default_factory=list)
    bAppendItemSets: Optional[bool] = None
    bAppendPreventIncreasingMinMaxItemSets: Optional[bool] = None

    def __str__(self) -> str:
        parts = []

        if self.SupplyCrateClassString is not None:
            parts.append(
                f'SupplyCrateClassString="{self.SupplyCrateClassString}"')

        if self.MinItemSets is not None:
            parts.append(f"MinItemSets={self.MinItemSets}")

        if self.MaxItemSets is not None:
            parts.append(f"MaxItemSets={self.MaxItemSets}")

        if self.NumItemSetsPower is not None:
            parts.append(f"NumItemSetsPower={self.NumItemSetsPower}")

        if self.bSetsRandomWithoutReplacement is not None:
            parts.append(
                "bSetsRandomWithoutReplacement="
                f"{self.bSetsRandomWithoutReplacement}")

        if self.ItemSets is not None:
            item_sets = ",".join(f"{item_set}" for item_set in self.ItemSets)
            parts.append(f"ItemSets=({item_sets})")

        if self.bAppendItemSets is not None:
            parts.append(f"bAppendItemSets={self.bAppendItemSets}")

        if self.bAppendPreventIncreasingMinMaxItemSets is not None:
            parts.append(
                "bAppendPreventIncreasingMinMaxItemSets="
                f"{self.bAppendPreventIncreasingMinMaxItemSets}")

        return f"({','.join(parts)})"

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        item_sets = data.get("ItemSets", [])

        if all(isinstance(item, dict) for item in item_sets):
            item_sets_objs = [ItemSet.from_dict(
                item_set) for item_set in item_sets]
        elif all(isinstance(item, ItemSet) for item in item_sets):
            item_sets_objs = item_sets
        else:
            raise ValueError(
                "ItemSets attribute must be a list of ItemSet instances or a "
                f"list of dictionaries representing ItemSet, "
                f"not {type(item_sets)}")

        item_sets_objs = item_sets_objs if item_sets_objs else None

        return cls(
            SupplyCrateClassString=data.get("SupplyCrateClassString"),
            MinItemSets=data.get("MinItemSets"),
            MaxItemSets=data.get("MaxItemSets"),
            NumItemSetsPower=data.get("NumItemSetsPower"),
            bSetsRandomWithoutReplacement=data.get(
                "bSetsRandomWithoutReplacement"),
            ItemSets=item_sets_objs,
            bAppendItemSets=data.get("bAppendItemSets"),
            bAppendPreventIncreasingMinMaxItemSets=data.get(
                "bAppendPreventIncreasingMinMaxItemSets"),
        )
