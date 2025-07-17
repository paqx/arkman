import os
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Optional

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


_servers = [
    Server(
        name="Aberration",
        host=os.environ["ABERRATION_HOST"],
        user=os.environ["ABERRATION_USER"],
        password=os.environ["ABERRATION_PASS"],
        admin_password=os.environ["ABERRATION_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["ABERRATION_RCON_PORT"]),
        id_=os.environ.get("ABERRATION_SERVER_ID"),
    ),
    Server(
        name="Crystal_Isles",
        host=os.environ["CRYSTAL_ISLES_HOST"],
        user=os.environ["CRYSTAL_ISLES_USER"],
        password=os.environ["CRYSTAL_ISLES_PASS"],
        admin_password=os.environ["CRYSTAL_ISLES_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["CRYSTAL_ISLES_RCON_PORT"]),
        id_=os.environ.get("CRYSTAL_ISLES_SERVER_ID"),
    ),
    Server(
        name="Extinction",
        host=os.environ["EXTINCTION_HOST"],
        user=os.environ["EXTINCTION_USER"],
        password=os.environ["EXTINCTION_PASS"],
        admin_password=os.environ["EXTINCTION_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["EXTINCTION_RCON_PORT"]),
        id_=os.environ.get("EXTINCTION_SERVER_ID"),
    ),
    Server(
        name="Fjordur",
        host=os.environ["FJORDUR_HOST"],
        user=os.environ["FJORDUR_USER"],
        password=os.environ["FJORDUR_PASS"],
        admin_password=os.environ["FJORDUR_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["FJORDUR_RCON_PORT"]),
        id_=os.environ.get("FJORDUR_SERVER_ID"),
    ),
    Server(
        name="Gen_1",
        host=os.environ["GEN_1_HOST"],
        user=os.environ["GEN_1_USER"],
        password=os.environ["GEN_1_PASS"],
        admin_password=os.environ["GEN_1_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["GEN_1_RCON_PORT"]),
        id_=os.environ.get("GEN_1_SERVER_ID"),
    ),
    Server(
        name="Gen_2",
        host=os.environ["GEN_2_HOST"],
        user=os.environ["GEN_2_USER"],
        password=os.environ["GEN_2_PASS"],
        admin_password=os.environ["GEN_2_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["GEN_2_RCON_PORT"]),
        id_=os.environ.get("GEN_2_SERVER_ID"),
    ),
    Server(
        name="Island",
        host=os.environ["ISLAND_HOST"],
        user=os.environ["ISLAND_USER"],
        password=os.environ["ISLAND_PASS"],
        admin_password=os.environ["ISLAND_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["ISLAND_RCON_PORT"]),
        id_=os.environ.get("ISLAND_SERVER_ID"),
    ),
    Server(
        name="Ragnarok",
        host=os.environ["RAGNAROK_HOST"],
        user=os.environ["RAGNAROK_USER"],
        password=os.environ["RAGNAROK_PASS"],
        admin_password=os.environ["RAGNAROK_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["RAGNAROK_RCON_PORT"]),
        id_=os.environ.get("RAGNAROK_SERVER_ID"),
    ),
    Server(
        name="Valguero",
        host=os.environ["VALGUERO_HOST"],
        user=os.environ["VALGUERO_USER"],
        password=os.environ["VALGUERO_PASS"],
        admin_password=os.environ["VALGUERO_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["VALGUERO_RCON_PORT"]),
        id_=os.environ.get("VALGUERO_SERVER_ID"),
    ),
]

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
