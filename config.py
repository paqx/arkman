import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Server:
    """Represents connection credentials of an ARK server"""
    name: str
    host: str
    user: str
    password: str
    admin_password: str
    rcon_port: int
    id_: Optional[int]


@dataclass
class Cfg:
    """Configuration container for ARK servers."""
    servers: list[Server]


_server_names = os.environ["SERVER_NAMES"].split(',')
_servers = []

for server_name in _server_names:
    name = server_name.strip()
    name_uc = name.upper()

    _servers.append(Server(
        name=name,
        host=os.environ[f"{name_uc}_HOST"],
        user=os.environ[f"{name_uc}_USER"],
        password=os.environ[f"{name_uc}_PASS"],
        admin_password=os.environ[f"{name_uc}_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ[f"{name_uc}_RCON_PORT"]),
        id_=os.environ.get(f"{name_uc}_SERVER_ID"),
    ))

CFG = Cfg(servers=_servers)


@dataclass
class ArkHoster:
    """
    Stores credentials and configuration needed to interact with the 
    ark-hoster.ru web panel.
    """
    email: str
    password: str
    base_url: str
    user_agent: str


_EMAIL = os.environ.get('ARK_HOSTER_EMAIL')
_USER_AGENT = f'arkman.py/1.0 (automation; contact: {_EMAIL})'

ARK_HOSTER = ArkHoster(
    email=_EMAIL,
    password=os.environ.get('ARK_HOSTER_PASSWORD'),
    base_url='https://panel.ark-hoster.ru',
    user_agent=_USER_AGENT,
)
