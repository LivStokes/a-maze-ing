"""
Parsing and validating the maze configuration file.
Provides utilities for reading the 'config.txt' file, validates its contents, and returns a fully typed MazeConfig dataclass.
"""
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
    """
    Validated configuration for the maze generator.

    @dataclass
        Used to prevent repetitive code by generating '__init__' behind the scene.

    Attributes
    ----------
    width : int
        The number of columns in the maze.
    height : int
        The number of rows in the maze.
    entry : tuple[int, int]
        The 'x,y' coordinates of the maze entry point.
    exit : tuple[int, int]
        The 'x,y' coordinates of the maze exit point.
    output_file : str
        The file path where the generated maze will be written.
    perfect : bool
        Generates a perfect maze if 'True', else it generates an imperfect maze if 'False'.
    seed : int or None
        The random seed for reproducable maze generation, 'None' if no seed specified.
    algorithm : str
        The maze generation algorithm to use.
    imperfect_rate : float
        The proportion of walls removed when generating an imperfect maze.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None
    algorithm: str
    imperfect_rate: float

def parse_config(file_path: Path) -> dict[str, Any]:
    """
    Parsing config.txt into a dictionary of key-value pairs.

    This reads line by line from the config.txt file, validating that each line follows the 'KEY=VALUE' format.
    It skips empty lines and comments starting wth '#'.

    Parameters
    ----------
    file_path : Path
        Path to the configuration file to parse from.

    Returns
    -------
    dict[str, Any]
        A dictionary that maps keys to its corresponding value.

    Raises
    ------
    ConfigError
        If the file is not found, cannot be read, contains a line without an '=', or contains a line with an empty key.
    """
    pairs: dict[str, Any] = {}
    source_name = file_path.name

    try:
        with file_path.open("r") as file:
            for lineno, line in enumerate(file, start=1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if "=" not in stripped:
                    raise ConfigError(f"{source_name}:{lineno}: Expected KEY=VALUE, got: {stripped!r}")

                key, _, value = stripped.partition("=")
                key = key.strip()
                value = value.strip()
                if not key:
                    raise ConfigError(f"{source_name}:{lineno}: Empty key in line: {stripped!r}")
                pairs[key] = value
    except FileNotFoundError as e:
        raise ConfigError(f"Could not find the file '{file_path}'") from e
    except OSError as e:
        raise ConfigError(f"Could not read the config file '{file_path}': {e}") from e
    return pairs

def _require(pairs: dict[str, str], path: str, *keys: str) -> None:
    """
    Makes sure all required keys are present in the a config dictionary.

    Parameters
    ----------
    pairs : dict[str, str]
        The parsed configuration dictionary to validate.
    path : str
        The config file path.
    *keys : str
        One or more key names that must be present in pairs.

    Returns
    -------
    None

    Raises
    ------
    ConfigError
        Used if one or more of the required keys are are missing from pairs.
    """
    missing = set(keys) - pairs.keys()
    if missing:
        raise ConfigError(f"{path}: Missing requirement from the config keys: {', '.join(missing)}")

def _parse_positive_int(value: str, key: str, path: str) -> int:
    """
    Parses a string into a positive integer.

    Parameters
    ----------
    value : str
        The string value to parse, read from the config file.
    key : str
        The config key associated with this value.
    path : str
        The config file path.

    Returns
    -------
    int
        The parsed integure is returned, which is > 0.

    Raises
    ------
    ConfigError
        Used if path is invalid (non positive int value)
    """
    try:
        val = int(value)
        if val <= 0:
            raise ValueError()
        return val
    except ValueError:
            raise ConfigError(f"{path}: Invalid value for {key}: Expected a positive int >_<. got '{value}' instead")

def _parse_bool(value: str, key: str, path: str) -> bool:
    """
    Parses a string into a boolean.

    Parameters
    ----------
    value : str
        The string value to parse, read from the config file.
    key : str
        The config key associated with this value.
    path : str
        The config file path.

    Returns
    -------
    boolean
        True if it is a boolean
        False if it is not a boolean

    Raises
    ------
    ConfigError
        Used if path is invalid (non boolean value).
    """
    normalized = value.upper()
    if normalized in ("TRUE", "YES", "1"):
        return True
    if normalized in ("FALSE", "NO", "0"):
        return False
            raise ConfigError(f"{path}: Invalid boolean value for {key}: '{value}'")

def _parse_coordinates(value: str, key: str, path:str) -> tuple[int, int]:
    """
    Parses the Coordinates

    Parameters
    ----------
    value : str
        The string value to parse, read from the config file.
    key : str
        The config key associated with this value.
    path : str
        The config file path.

    Returns
    -------
    tuple[int, int]

    Raises
    ------
    ConfigError
        Used if path is invalid (non integer 'X,Y' value).
    """
    try:
        cleaned = value.strip("(){}[]")
        parts = cleaned.split(",")
        if len(parts) != 2:
            raise Valueerror()
        return int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ConfigError(f"{path}: Invalid coordinate format for {key}. Expected 'X,Y', but got '{value}'")

def _validate(pairs: dict[str, str], path: str,) -> MazeConfig:
    """
    Validates pairs - Responsible for parsing, validating, and extracting configuration parameters from a dict named pairs.

    Parameters
    ----------
    pairs : dict[str, str]
        Raw key-value pairs parsed from the config file.
    path : str
        The config file path.

    Returns
    -------
    MazeConfig
        A validated configuration object ready to be consumed by the maze generator.

    Raises
    ------
    ConfigError
        Used if any required key is missing ('WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT').
    """
    _require(pairs, path, "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")
    width = _parse_positive_int(pairs["WIDTH"], "WIDTH", path)
    height = _parse_positive_int(pairs["HEIGHT"], "HEIGHT", path)
    entry = _parse_coordinates(pairs["ENTRY"], "ENTRY", path)
    exit = _parse_coordinates(pairs["EXIT"], "EXIT", path)
    perfect = _parse_bool(pairs["PERFECT"], "PERFECT", path)

    seed = None
    if "SEED" in pairs:
        seed = int(pairs["SEED"]) if pairs["SEED"].isdigit() else 0
    algorithm = pairs.get("ALGORITHM", "default")
    imperfect_rate = float(pairs.get("IMPERFECT_RATE", 0.0))
    pattern_file = pairs.get("PATTERN")
    pattern_lines = []
    if pattern_file:
        try:
            pattern_path = Path("patterns") / pattern_file
            pattern_lines = pattern_path.read_text().splitlines()
        except FileNotFoundError as e:
            raise ConfigError(f"Couldn't find pattern file '{pattern_file}'") from e

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        output_file=pairs["OUTPUT_FILE"],
        perfect=perfect,
        seed=seed,
        algorithm=algorithm,
        imperfect_rate=imperfect_rate
    )
