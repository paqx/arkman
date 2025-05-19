from typing import Self
from dataclasses import dataclass

from .complex_value import ComplexValue

# pylint: disable=invalid-name


@dataclass
class Quantity(ComplexValue):
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
        return (
            f"("
            f"MaxItemQuantity={self.MaxItemQuantity},"
            f"bIgnoreMultiplier={self.bIgnoreMultiplier}"
            f")"
        )

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            MaxItemQuantity=data.get("MaxItemQuantity"),
            bIgnoreMultiplier=data.get("bIgnoreMultiplier")
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
        return (
            f"("
            f'ItemClassString="{self.ItemClassString}",'
            f"Quantity={self.Quantity}"
            f")"
        )

    @classmethod
    def from_dict(cls, data: dict) -> Self:
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
            ItemClassString=data.get("ItemClassString"),
            Quantity=quantity_obj
        )
