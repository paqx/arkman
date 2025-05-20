import re
from collections import UserDict, defaultdict
from collections.abc import Mapping
from dataclasses import asdict
from typing import Union, Self, Literal, Optional
from os import PathLike, environ, path

import yaml

from src.complex_values import (
    ComplexValue,
    ConfigOverrideSupplyCrateItems,
    ConfigOverrideItemMaxQuantity,
    ConfigAddNPCSpawnEntriesContainer,
)

ArkConfigPrimitiveValue = Union[str, int, float, bool]
ArkConfigComplexValue = Union[
    ConfigOverrideSupplyCrateItems,
    ConfigOverrideItemMaxQuantity,
    ConfigAddNPCSpawnEntriesContainer
]
ArkConfigValue = Union[
    Union[ArkConfigPrimitiveValue, ArkConfigComplexValue],
    list[Union[ArkConfigPrimitiveValue, ArkConfigComplexValue]]
]


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

    ALLOWED_TYPES = (str, int, float, bool, Mapping, ComplexValue)
    COMPLEX_VALUE_MAP = {
        'ConfigOverrideSupplyCrateItems': ConfigOverrideSupplyCrateItems,
        'ConfigOverrideItemMaxQuantity': ConfigOverrideItemMaxQuantity,
        'ConfigAddNPCSpawnEntriesContainer': ConfigAddNPCSpawnEntriesContainer,
    }

    def __setitem__(self, key: str, item):
        """
        Set an option in the section.

        Ensures the item is of an allowed type or list of allowed types.
        """
        is_allowed_type = isinstance(item, self.ALLOWED_TYPES)
        is_allowed_list = (
            isinstance(item, list) and
            all(isinstance(x, self.ALLOWED_TYPES) for x in item)
        )

        if not (is_allowed_type or is_allowed_list):
            raise TypeError(
                "Value must be str, int, float, bool, Mapping, ComplexValue, "
                f"or a list of these types, not {type(item).__name__} for key "
                f"{key}"
            )

        if isinstance(item, list) and key in self.COMPLEX_VALUE_MAP:
            complex_item = []
            cls = self._get_complex_value_cls(key)

            for i in item:
                if isinstance(i, (str, ComplexValue)):
                    complex_item.append(i)
                elif isinstance(i, Mapping):
                    complex_item.append(cls.from_dict(i))
                else:
                    raise ValueError(
                        f"Invalid type {type(i)} for complex value {key}")

            item = complex_item
        elif isinstance(item, str):
            item = self._parse_value(item)

        # Handle existing keys
        if key in self.data:
            existing = self.data[key]

            if isinstance(existing, list):
                # If existing is a list, append the new item(s)
                if isinstance(item, list):
                    existing.extend(item)
                else:
                    existing.append(item)
            else:
                # If existing is not a list, create a new list with both values
                if isinstance(item, list):
                    self.data[key] = [existing, *item]
                else:
                    self.data[key] = [existing, item]
        else:
            # New key - store directly
            self.data[key] = item

    def __repr__(self):
        """Return a string representation of the section."""
        return f"ArkConfigSection({self.data!r})"

    def _get_complex_value_cls(self, key: str) -> type[ComplexValue]:
        """Get class of a complex value by key"""
        return self.COMPLEX_VALUE_MAP[key]

    def _parse_value(self, value: str) -> ArkConfigPrimitiveValue:
        """
        Parse a string value to its respective type (bool, int, float), or
        fall back to str.
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
        """Return the section's key-value pairs as an INI-formatted string."""
        lines = []

        for key, item in self.data.items():
            if isinstance(item, list):
                for value in item:
                    lines.append(f'{key}={value}')
            else:
                lines.append(f'{key}={item}')

        return '\r\n'.join(lines)


class ArkConfig:
    """
    A custom INI-style parser for Ark Survival Evolved configuration files.

    This parser can handle sections with duplicate keys.
    """

    _SECTION_PATTERN = r"""\[(?P<section_name>.+)\]"""
    _OPTION_PATTERN = r"""(?P<option>.*?)\s*(?P<vi>{delim})\s*(?P<value>.*)$"""
    _ENV_PATTERN = r"""\$\{(?P<env>[A-Za-z_][A-Za-z0-9_]*)\}"""

    SECTION_RE = re.compile(_SECTION_PATTERN)
    OPTION_RE = re.compile(_OPTION_PATTERN.format(delim="="))
    ENV_RE = re.compile(_ENV_PATTERN)

    def __init__(self, encoding: Optional[Literal['utf-8', 'utf-16']] = None):
        """Initialize a new empty configuration."""
        self.encoding = encoding
        self._config: defaultdict[str, ArkConfigSection] = defaultdict(
            ArkConfigSection)

    def __repr__(self):
        """Return a string representation of the configuration."""
        config = ', '.join(
            f"{section_name!r}: {section!r}" for section_name, section in self._config.items()
        )
        return f"ArkConfig(encoding={self.encoding!r}, config={{{config}}})"

    def __getitem__(self, section_name: str) -> ArkConfigSection:
        """Return the section by its name."""
        if section_name not in self._config:
            raise KeyError(f"Section '{section_name}' not found")

        return self._config[section_name]

    def __setitem__(self, section_name: str, value):
        """
        Set a configuration section by name.

        Accepts either an ArkConfigSection or a dictionary of options.
        """
        if isinstance(value, ArkConfigSection):
            self._config[section_name] = value
        elif isinstance(value, dict):
            self._config[section_name] = ArkConfigSection(value)
        else:
            raise ValueError(
                f"Value must be an ArkConfigSection or a dictionary of options, not {type(value)}."
            )

    @property
    def section_names(self) -> list[str]:
        """Return a list of section names in the configuration."""
        return list(self._config.keys())

    def _expand_env_vars(self):
        """Expand environment variables in the configuration."""
        for section_name, section in self._config.items():
            for key, value in section.items():
                if not isinstance(value, str):
                    continue

                value = value.strip()
                env_match = self.ENV_RE.match(value)

                if not env_match:
                    continue

                env_key = env_match.group('env')
                env_value = environ[env_key]
                self._config[section_name].data[key] = env_value

    def read(self, filepath: str | PathLike):
        """
        Read and parse an Ark config INI file.

        Parameters
        ----------
        filepath : str or PathLike
            The path to the INI file to read.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.encoding = 'utf-8'
        except UnicodeError:
            with open(filepath, 'r', encoding='utf-16') as f:
                lines = f.readlines()
                self.encoding = 'utf-16'

        section_name = None
        self._config.clear()

        for line in lines:
            line = line.strip()

            if not line or line.startswith(';'):
                continue

            section_match = self.SECTION_RE.match(line)
            if section_match:
                section_name = section_match.group('section_name')
                continue

            if section_name is None:
                raise ValueError(f'No section for option: {line}')

            option_match = self.OPTION_RE.match(line)
            if option_match:
                option = option_match.group('option').strip()

                if option_match.group('value'):
                    value = option_match.group('value').strip()
                else:
                    value = ''

                self._config[section_name][option] = value

    def write(self, filepath: str | PathLike):
        """
        Dump and write the configuration to an INI file.

        Parameters
        ----------
        filepath : str or PathLike
            The path to the INI file to write.
        """
        with open(filepath, 'w', encoding=self.encoding) as f:
            f.write(self.dump())

    def merge(self, other: Self) -> Self:
        """
        Merge the current configuration with another, with the other taking
        precedence for duplicates.

        Parameters
        ----------
        other : ArkConfig
            Another ArkConfig instance to merge with.

        Returns
        -------
        ArkConfig
            A new ArkConfig instance containing the merged configuration.
        """
        encoding = other.encoding or self.encoding
        merged = ArkConfig(encoding=encoding)
        section_names = {
            k: None for k in self.section_names + other.section_names}

        for section_name in section_names:
            merged[section_name] = self[section_name] | other[section_name]

        return merged

    def dump(self) -> str:
        """Return the configuration as an INI-formatted string."""
        lines = []

        for section_name, section in self._config.items():
            lines.append(f'[{section_name}]')
            lines.append(section.dump())
            lines.append('')

        return '\r\n'.join(lines)

    def to_dict(self) -> dict[str, dict[str, ArkConfigValue]]:
        """Return the configuration as a nested dictionary."""
        result = {}

        for section_name, section in self._config.items():
            section_dict = {}

            for key, value in section.items():
                if isinstance(value, ComplexValue):
                    section_dict[key] = asdict(value)
                elif isinstance(value, list):
                    section_dict[key] = [asdict(item) if isinstance(
                        item, ComplexValue) else item for item in value]
                else:
                    section_dict[key] = value
            result[section_name] = section_dict

        return result

    def to_yaml(self) -> str:
        """Return the configuration as a YAML-formatted string."""
        return yaml.safe_dump(
            self.to_dict(), allow_unicode=True, sort_keys=False)

    def to_yaml_file(self, filepath: str | PathLike):
        """
        Write the configuration as a YAML-formatted string to a file.

        Parameters
        ----------
        filepath : str or PathLike
            The path to the YAML file to write.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_yaml())

    @classmethod
    def from_dict(cls, data: dict[str, dict[str, ArkConfigValue]]) -> Self:
        """
        Create an ArkConfig instance from a nested dictionary structure.

        Parameters
        ----------
        data : dict
            A dictionary where each key is a section name and each value is
            another dictionary of configuration options.

        Returns
        -------
        ArkConfig
            An instance of ArkConfig created from the provided dictionary.
        """
        config = cls()

        for section_name, section_dict in data.items():
            config[section_name] = section_dict

        return config

    @classmethod
    def from_yaml(cls, yaml_text: str) -> Self:
        """
        Create an ArkConfig instance from a YAML string.

        Parameters
        ----------
        yaml_text : str
            A YAML-formatted string representing the configuration.

        Returns
        -------
        ArkConfig
            An instance of ArkConfig created from the provided YAML string.
        """
        yaml.add_constructor(
            '!include', cls._include_constructor, Loader=yaml.SafeLoader)
        data = yaml.safe_load(yaml_text)

        if not isinstance(data, dict):
            raise ValueError("YAML root must be a mapping")

        instance = cls.from_dict(data)
        instance._expand_env_vars()
        return instance

    @classmethod
    def from_yaml_file(cls, filepath: str | PathLike) -> Self:
        """
        Create an ArkConfig instance from a YAML file.

        Parameters
        ----------
        filepath : str or PathLike
            The path to the YAML file to read.

        Returns
        -------
        ArkConfig
            An instance of ArkConfig created from the provided YAML file.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            yaml_text = f.read()

        return cls.from_yaml(yaml_text)

    @staticmethod
    def _include_constructor(loader, node):
        """Handle !include statements in YAML."""
        include_filename = loader.construct_scalar(node)
        include_path = path.join(
            './configs/yml/includes', include_filename)

        if not path.isfile(include_path):
            raise FileNotFoundError(
                f"Include file does not exist: {include_path}")

        with open(include_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
