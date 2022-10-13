from typing import (
    Optional, 
    Union
)

class DotEnv:
    path_env_file = ".env"

    def __init__(self, env_file: Optional[str]=".env") -> None:
        self.path_env_file = env_file # type: ignore

    @classmethod
    def get(cls, var_name: str) -> Optional[Union[str, int]]:
        with open(cls.path_env_file, "r", encoding="UTF-8") as f:
            for line in f:
                line: str = line.replace("\n", "").strip() # type: ignore
                
                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=", maxsplit=1)

                if key.strip() == var_name.strip():
                    if value.isdigit():
                        value = int(value) # type: ignore
                    return value
            return None
