"""Parsing and validating the maze configuration file.
Provides utilities for reading the 'config.txt' file, validates its contents,
and returns a fully typed MazeConfig dataclass."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ConfigError(Exception):
    """
    Raised when the configuration file is invalid.
    """
    pass


@dataclass
class MazeConfig:
    """Validated configuration for the maze generator."""
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None
    algorithm: str
    forty_two: bool


class Parser:
    @staticmethod
    def parse_config(file_path: Path) -> dict[str, Any]:
        """Parsing config.txt into a dictionary of key-value pairs.
        Reads line by line from the config.txt file, 
        validating that each line follows the 'KEY=VALUE' format.
        It skips empty lines and comments starting wth '#'."""
        pairs: dict[str, Any] = {}
        source_name = file_path.name

        try:
            with file_path.open("r") as file:
                for lineno, line in enumerate(file, start=1):
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#"):
                        continue
                    if "=" not in stripped:
                        raise ConfigError(f"{source_name}:{lineno}: Expected"
                                          f"KEY=VALUE, got: {stripped!r}")

                    key, _, value = stripped.partition("=")
                    key = key.strip()
                    value = value.strip()
                    if not key:
                        raise ConfigError(f"{source_name}:{lineno}: Empty key"
                                          f"in line: {stripped!r}")
                    pairs[key.upper()] = value
        except FileNotFoundError as e:
            raise ConfigError(f"Could not find the file '{file_path}'") from e
        except OSError as e:
            raise ConfigError(f"Could not read the config"
                              f"file '{file_path}': {e}") from e
        return pairs

    @staticmethod
    def _require(pairs: dict[str, str], path: str, *keys: str) -> None:
        """Makes sure all required keys are present in the a config dictionary."""
        missing = set(keys) - pairs.keys()
        if missing:
            raise ConfigError(f"{path}: Missing requirement from the config"
                              f"keys: {', '.join(missing)}")

    @staticmethod
    def _parse_positive_int(value: str, key: str, path: str) -> int:
        """Parses a string into a positive integer."""
        try:
            val = int(value)
            if val <= 0:
                raise ValueError()
            return val
        except ValueError:
            raise ConfigError(f"{path}: Invalid value for {key}: Expected"
                              f"a positive int >_<. got '{value}' instead")

    @staticmethod
    def _parse_bool(value: str, key: str, path: str) -> bool:
        """Parses a string into a boolean."""
        normalized = value.upper()
        if normalized in ("TRUE", "YES", "1"):
            return True
        if normalized in ("FALSE", "NO", "0"):
            return False
        raise ConfigError(f"{path}: Invalid boolean value"
                          f"for {key}: '{value}'")

    @staticmethod
    def _parse_coordinates(value: str, key: str, path: str) -> tuple[int, int]:
        """Parses the Coordinates"""
        try:
            cleaned = value.strip("(){}[]")
            parts = cleaned.split(",")
            if len(parts) != 2:
                raise ValueError()
            return int(parts[0].strip()), int(parts[1].strip())
        except ValueError:
            raise ConfigError(f"{path}: Invalid coordinate format for {key}."
                              f"Expected 'X,Y', but got '{value}'")

    @staticmethod
    def _validate(pairs: dict[str, str], path: str,) -> MazeConfig:
        """Validates pairs - Responsible for parsing, validating, and extracting
        configuration parameters from a dict named pairs."""
        Parser._require(pairs, path, "WIDTH", "HEIGHT", "ENTRY", "EXIT",
                        "OUTPUT_FILE", "PERFECT")
        width = Parser._parse_positive_int(pairs["WIDTH"], "WIDTH", path)
        height = Parser._parse_positive_int(pairs["HEIGHT"], "HEIGHT", path)
        entry = Parser._parse_coordinates(pairs["ENTRY"], "ENTRY", path)
        exit = Parser._parse_coordinates(pairs["EXIT"], "EXIT", path)
        perfect = Parser._parse_bool(pairs["PERFECT"], "PERFECT", path)

        seed: int | None = None
        if "SEED" in pairs:
            seed = (int(pairs["SEED"]) if pairs["SEED"].lstrip("-").isdigit()
                    else None)
        algorithm = pairs.get("ALGORITHM", "backtracking").lower()
        forty_two = True
        if "FORTY_TWO" in pairs:
            forty_two = Parser._parse_bool(pairs["FORTY_TWO"], "FORTY_TWO",
                                           path)

        return MazeConfig(
            width=width,
            height=height,
            entry=entry,
            exit=exit,
            output_file=pairs["OUTPUT_FILE"],
            perfect=perfect,
            seed=seed,
            algorithm=algorithm,
            forty_two=forty_two
        )


def parse_config(file_path: Path | str = "config.txt") -> MazeConfig:
    """Loads and validates the maze config file (config.txt)"""
    path = Path(file_path)
    pairs = Parser.parse_config(path)
    return Parser._validate(pairs, str(path))
