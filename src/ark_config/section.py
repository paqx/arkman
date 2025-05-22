import re
from collections import UserDict
from typing import Optional

from src.complex_values import (
    ComplexValue,
    ConfigAddNPCSpawnEntriesContainer,
    ConfigOverrideItemMaxQuantity,
    ConfigOverrideSupplyCrateItems,
    DinoSpawnWeightMultiplier,
)
from .config_values import ArkConfigValue, ArkConfigPrimitiveValue


class ArkConfigSection(UserDict[str, Optional[ArkConfigValue]]):
    """
    Represents a section of an Ark Survival Evolved configuration file.

    This class can handle keys that appear multiple times in a section.
    Each key's value is parsed and stored as one of the following types:
    str, int, float, or bool.
    """

    _BOOL_PATTERN = r"""
        ^               # Start of string
        (?P<bool>       # Named capture group 'bool'
            true        # Literal 'true'
            |           # OR
            false       # Literal 'false'
        )               # End of capture group
        $               # End of string
    """

    _INT_PATTERN = r"""
        ^               # Start of string
        (?P<int>        # Named capture group 'int'
            [+-]?       # Optional + or - sign
            \d+         # One or more digits
        )               # End of capture group
        $               # End of string
    """

    _FLOAT_PATTERN = r"""
        ^               # Start of string
        (?P<float>      # Named capture group 'float'
            [+-]?       # Optional + or - sign
            \d*         # Zero or more digits (optional before decimal)
            \.          # Decimal point
            \d+         # One or more digits (required after decimal)
        )               # End of capture group
        $               # End of string
    """

    BOOL_RE = re.compile(_BOOL_PATTERN, re.IGNORECASE | re.VERBOSE)
    INT_RE = re.compile(_INT_PATTERN, re.VERBOSE)
    FLOAT_RE = re.compile(_FLOAT_PATTERN, re.VERBOSE)

    ALLOWED_TYPES = (str, int, float, bool, dict, ComplexValue)
    COMPLEX_VALUE_MAP = {
        'ConfigOverrideSupplyCrateItems': ConfigOverrideSupplyCrateItems,
        'ConfigOverrideItemMaxQuantity': ConfigOverrideItemMaxQuantity,
        'ConfigAddNPCSpawnEntriesContainer': ConfigAddNPCSpawnEntriesContainer,
        'DinoSpawnWeightMultiplier': DinoSpawnWeightMultiplier,
    }

    def __setitem__(self, key: str, item):
        """
        Set an option in the section.

        Ensures the item is of an allowed type or list of allowed types.

        Parameters
        ----------
        key : str
            The key of the option to set.
        item : Any
            The value to associate with the key.

        Raises
        ------
        TypeError
            If the item is not of the allowed type or list of allowed types.
        ValueError
            If a complex value has an invalid type.
        """
        is_allowed_type = isinstance(item, self.ALLOWED_TYPES)
        is_allowed_list = (
            isinstance(item, list) and
            all(isinstance(x, self.ALLOWED_TYPES) for x in item)
        )

        if not (is_allowed_type or is_allowed_list):
            raise TypeError(
                "Value must be str, int, float, bool, dict, ComplexValue, or a "
                f"list of these types, not {type(item).__name__} for key {key}"
            )

        if isinstance(item, list) and key in self.COMPLEX_VALUE_MAP:
            complex_item = []
            cls = self._get_complex_value_cls(key)

            for i in item:
                if isinstance(i, (str, ComplexValue)):
                    complex_item.append(i)
                elif isinstance(i, dict):
                    complex_item.append(cls.from_dict(i))
                else:
                    raise ValueError(
                        f"Invalid type {type(i)} for complex value {key}")

            item = complex_item
        elif isinstance(item, str):
            item = self._parse_value(item)

        if key in self.data:
            existing = self.data[key]

            if isinstance(existing, list):
                if isinstance(item, list):
                    existing.extend(item)
                else:
                    existing.append(item)
            else:
                if isinstance(item, list):
                    self.data[key] = [existing, *item]
                else:
                    self.data[key] = [existing, item]
        else:
            self.data[key] = item

    def __repr__(self) -> str:
        """Return a string representation of the section.

        Returns
        -------
        str
            The string representation of the section.
        """
        return f"ArkConfigSection({self.data!r})"

    def _get_complex_value_cls(self, key: str) -> type[ComplexValue]:
        """Get class of a complex value by key.

        Parameters
        ----------
        key : str
            The key to retrieve the class for.

        Returns
        -------
        type[ComplexValue]
            The class of the complex value.
        """
        return self.COMPLEX_VALUE_MAP[key]

    def _parse_value(self, value: str) -> ArkConfigPrimitiveValue:
        """
        Parse a string value to its respective type (bool, int, float), or
        fall back to str.

        Parameters
        ----------
        value : str
            The string to parse.

        Returns
        -------
        ArkConfigPrimitiveValue
            The parsed value.
        """
        value = value.strip()

        bool_match = self.BOOL_RE.match(value)
        if bool_match:
            return bool_match.group('bool').lower() == 'true'

        float_match = self.FLOAT_RE.match(value)
        if float_match:
            return float(float_match.group('float'))

        int_match = self.INT_RE.match(value)
        if int_match:
            return int(int_match.group('int'))

        return value

    def dump(self) -> str:
        """Return the section's key-value pairs as an INI-formatted string.

        Returns
        -------
        str
            An INI-formatted string representation of the section.
        """
        lines = []

        for key, item in self.data.items():
            if isinstance(item, list):
                for value in item:
                    lines.append(f'{key}={value}')
            else:
                lines.append(f'{key}={item}')

        return '\n'.join(lines)
