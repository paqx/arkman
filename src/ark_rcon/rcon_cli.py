import re
from dataclasses import dataclass

from rcon.source import Client


@dataclass
class Player:
    """
    Represents a player connected to an ARK server.

    Parameters
    ----------
    name : str
        The player's in-game name.
    steam_id : str
        The player's Steam ID.
    """
    name: str
    steam_id: str


class ArkRcon:
    """
    Provides an interface to managers with an ARK server using RCON protocol.

    Parameters
    ----------
    host : str
        The hostname or IP address of the ARK server.
    port : int
        The RCON port for the server.
    password : str
        The RCON password for authentication.

    Attributes
    ----------
    host : str
        The server host address.
    port : int
        The server RCON port.
    password : str
        The RCON password.
    """
    _PLAYER_PATTERN = r"""^\s*\d+\.\s+(?P<name>.*?),\s*(?P<steam_id>\d+)\s*$"""

    PLAYER_RE = re.compile(_PLAYER_PATTERN)

    def __init__(self, host: str, port: int, password: str):
        """
        Initialize the ArkRcon instance.

        Parameters
        ----------
        host : str
            The server's host or IP address.
        port : int
            The server's RCON port.
        password : str
            The RCON password.
        """
        self.host = host
        self.port = port
        self.password = password

    def _run_command(self, command: str) -> str:
        """
        Send a command to the ARK server via RCON and return the response.

        Parameters
        ----------
        command : str
            The command to execute on the server.

        Returns
        -------
        str
            The command output as returned by the server.
        """
        with Client(self.host, self.port, passwd=self.password) as client:
            return client.run(command)

    def list_players(self) -> list[Player]:
        """
        Get a list of players currently connected to the server.

        Returns
        -------
        list of Player
            List of Player objects representing currently connected players.
        """
        response = self._run_command("listplayers")
        players = []

        for line in response.splitlines():
            match = self.PLAYER_RE.match(line)

            if match:
                player = Player(
                    name=match.group("name").strip(),
                    steam_id=match.group("steam_id").strip(),
                )
                players.append(player)

        return players
