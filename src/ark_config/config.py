import re
from collections import defaultdict
from dataclasses import asdict
from os import PathLike, environ, path
from typing import Literal, Optional, Self

import yaml

from src.complex_values import ComplexValue
from .config_values import ArkConfigValue
from .section import ArkConfigSection


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
        """Initialize a new empty configuration.

        Parameters
        ----------
        encoding : Optional[Literal['utf-8', 'utf-16']]
            The encoding type for reading files.
        """
        self.encoding = encoding
        self._config: defaultdict[str, ArkConfigSection] = defaultdict(
            ArkConfigSection)

    def __repr__(self) -> str:
        """Return a string representation of the configuration.

        Returns
        -------
        str
            The string representation of the configuration.
        """
        config = ', '.join(
            f"{section_name!r}: {section!r}" for section_name, section in self._config.items()
        )
        return f"ArkConfig(encoding={self.encoding!r}, config={{{config}}})"

    def __getitem__(self, section_name: str) -> ArkConfigSection:
        """Return the section by its name.

        Parameters
        ----------
        section_name : str
            The name of the section to retrieve.

        Returns
        -------
        ArkConfigSection
            The requested section.

        Raises
        ------
        KeyError
            If the section is not found.
        """
        if section_name not in self._config:
            raise KeyError(f"Section '{section_name}' not found")

        return self._config[section_name]

    def __setitem__(self, section_name: str, value):
        """
        Set a configuration section by name.

        Accepts either an ArkConfigSection or a dictionary of options.

        Parameters
        ----------
        section_name : str
            The name of the section to set.
        value : ArkConfigSection or dict
            The value to assign to the section.

        Raises
        ------
        ValueError
            If the value is not an ArkConfigSection or a dictionary of options.
        """
        if isinstance(value, ArkConfigSection):
            self._config[section_name] = value
        elif isinstance(value, dict):
            self._config[section_name] = ArkConfigSection(value)
        else:
            raise ValueError(
                f"Value must be an ArkConfigSection or a dictionary of options, not {type(value)}."
            )

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

        Raises
        ------
        ValueError
            If the YAML root is not a mapping.
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
        """Handle !include statements in YAML.

        Parameters
        ----------
        loader : yaml.Loader
            The YAML loader.
        node : yaml.Node
            The YAML node to process.

        Returns
        -------
        Any
            The parsed data from the included YAML file.

        Raises
        ------
        FileNotFoundError
            If the include file does not exist.
        """
        include_filename = loader.construct_scalar(node)
        include_path = path.join(
            './configs/yml/includes', include_filename)

        if not path.isfile(include_path):
            raise FileNotFoundError(
                f"Include file does not exist: {include_path}")

        with open(include_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @property
    def section_names(self) -> list[str]:
        """Return a list of section names in the configuration.

        Returns
        -------
        list of str
            The section names.
        """
        return list(self._config.keys())

    def read(self, filepath: str | PathLike):
        """
        Read and parse an Ark config INI file.

        Parameters
        ----------
        filepath : str or PathLike
            The path to the INI file to read.

        Raises
        ------
        ValueError
            If no section is available for an option.
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
        with open(filepath, 'w', encoding=self.encoding, newline='\r\n') as f:
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
        """Return the configuration as an INI-formatted string.

        Returns
        -------
        str
            An INI-formatted string representation of the configuration.
        """
        lines = []

        for section_name, section in self._config.items():
            lines.append(f'[{section_name}]')
            lines.append(section.dump())
            lines.append('')

        return '\n'.join(lines)

    def to_dict(self) -> dict[str, dict[str, ArkConfigValue]]:
        """Return the configuration as a nested dictionary.

        Returns
        -------
        dict
            A nested dictionary representation of the configuration.
        """
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
        """Return the configuration as a YAML-formatted string.

        Returns
        -------
        str
            A YAML-formatted string representation of the configuration.
        """
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
                env_value = environ.get(env_key, '')
                self._config[section_name].data[key] = env_value
