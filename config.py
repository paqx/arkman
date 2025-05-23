import os
from dataclasses import dataclass
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
    ),
    Server(
        name="Crystal_Isles",
        host=os.environ["CRYSTAL_ISLES_HOST"],
        user=os.environ["CRYSTAL_ISLES_USER"],
        password=os.environ["CRYSTAL_ISLES_PASS"],
        admin_password=os.environ["CRYSTAL_ISLES_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["CRYSTAL_ISLES_RCON_PORT"]),
    ),
    Server(
        name="Extinction",
        host=os.environ["EXTINCTION_HOST"],
        user=os.environ["EXTINCTION_USER"],
        password=os.environ["EXTINCTION_PASS"],
        admin_password=os.environ["EXTINCTION_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["EXTINCTION_RCON_PORT"]),
    ),
    Server(
        name="Fjordur",
        host=os.environ["FJORDUR_HOST"],
        user=os.environ["FJORDUR_USER"],
        password=os.environ["FJORDUR_PASS"],
        admin_password=os.environ["FJORDUR_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["FJORDUR_RCON_PORT"]),
    ),
    Server(
        name="Gen_1",
        host=os.environ["GEN_1_HOST"],
        user=os.environ["GEN_1_USER"],
        password=os.environ["GEN_1_PASS"],
        admin_password=os.environ["GEN_1_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["GEN_1_RCON_PORT"]),
    ),
    Server(
        name="Gen_2",
        host=os.environ["GEN_2_HOST"],
        user=os.environ["GEN_2_USER"],
        password=os.environ["GEN_2_PASS"],
        admin_password=os.environ["GEN_2_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["GEN_2_RCON_PORT"]),
    ),
    Server(
        name="Island",
        host=os.environ["ISLAND_HOST"],
        user=os.environ["ISLAND_USER"],
        password=os.environ["ISLAND_PASS"],
        admin_password=os.environ["ISLAND_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["ISLAND_RCON_PORT"]),
    ),
    Server(
        name="Ragnarok",
        host=os.environ["RAGNAROK_HOST"],
        user=os.environ["RAGNAROK_USER"],
        password=os.environ["RAGNAROK_PASS"],
        admin_password=os.environ["RAGNAROK_SERVER_ADMIN_PASS"],
        rcon_port=int(os.environ["RAGNAROK_RCON_PORT"]),
    ),
]

CFG = Cfg(servers=_servers)
