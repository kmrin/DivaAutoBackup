import os
import yaml

from pydantic import BaseModel

from .helpers import get_base_path

conf_path = os.path.join(get_base_path(external=True), "config.yml")


class Config(BaseModel):
    first_time_experience: bool
    app_id: int
    exec_name: str
    backup_path: str
    appdata_std_path: str
    appdata_dml_path: str
    appdata_edn_path: str
    eden_project: bool
    steam_path: str
    linux_steam_library_paths: list[str]


def load_config() -> Config:
    with open(conf_path, "r") as f:
        return Config.model_validate(yaml.safe_load(f))


def write_config(config: Config) -> None:
    with open(conf_path, "w", encoding="utf-8") as f:
        yaml.dump(config.model_dump(), f, allow_unicode=True)


conf = load_config()
