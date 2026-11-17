import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from errors import ConfigurationError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = PROJECT_ROOT / ".env"
SEED_FILE_PATH = PROJECT_ROOT / "data" / "seed.cypher"
REQUIRED_VARIABLES = ("NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD")
DEFAULT_PERSON_NAME = "Ana"
MAX_PERSON_NAME_LENGTH = 50
PERSON_NAME_PATTERN = re.compile(r"[^\W\d_]+(?:[ '-][^\W\d_]+)*")
MINIMUM_LIKED_SCORE = 4
MAX_RECOMMENDATIONS = 5


@dataclass(frozen=True)
class Neo4jSettings:
    uri: str
    username: str
    password: str
    database: Optional[str]


def load_settings():
    load_dotenv(ENV_FILE_PATH)
    missing_variables = [name for name in REQUIRED_VARIABLES if not os.getenv(name)]
    if missing_variables:
        raise ConfigurationError(
            "Faltan variables en el archivo .env: " + ", ".join(missing_variables)
        )
    return Neo4jSettings(
        uri=os.environ["NEO4J_URI"],
        username=os.environ["NEO4J_USERNAME"],
        password=os.environ["NEO4J_PASSWORD"],
        database=os.getenv("NEO4J_DATABASE") or None,
    )
