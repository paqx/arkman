import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Server:
    name: str
    host: str
    user: str
    password: str


@dataclass
class Cfg:
    servers: list[Server]


_servers = [
    Server(
        name="Aberration",
        host=os.environ["ABERRATION_HOST"],
        user=os.environ["ABERRATION_USER"],
        password=os.environ["ABERRATION_PASS"],
    ),
    Server(
        name="Crystal_Isles",
        host=os.environ["CRYSTAL_ISLES_HOST"],
        user=os.environ["CRYSTAL_ISLES_USER"],
        password=os.environ["CRYSTAL_ISLES_PASS"],
    ),
    Server(
        name="Extinction",
        host=os.environ["EXTINCTION_HOST"],
        user=os.environ["EXTINCTION_USER"],
        password=os.environ["EXTINCTION_PASS"],
    ),
    Server(
        name="Fjordur",
        host=os.environ["FJORDUR_HOST"],
        user=os.environ["FJORDUR_USER"],
        password=os.environ["FJORDUR_PASS"],
    ),
    Server(
        name="Gen_1",
        host=os.environ["GEN_1_HOST"],
        user=os.environ["GEN_1_USER"],
        password=os.environ["GEN_1_PASS"],
    ),
    Server(
        name="Gen_2",
        host=os.environ["GEN_2_HOST"],
        user=os.environ["GEN_2_USER"],
        password=os.environ["GEN_2_PASS"],
    ),
    Server(
        name="Island",
        host=os.environ["ISLAND_HOST"],
        user=os.environ["ISLAND_USER"],
        password=os.environ["ISLAND_PASS"],
    ),
    Server(
        name="Ragnarok",
        host=os.environ["RAGNAROK_HOST"],
        user=os.environ["RAGNAROK_USER"],
        password=os.environ["RAGNAROK_PASS"],
    ),
]

cfg = Cfg(servers=_servers)
