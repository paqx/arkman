import re
from dataclasses import dataclass
from typing import Union

from rcon.source import Client

from config import Server


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
    Manages an ARK server via the RCON protocol.

    Parameters
    ----------
    server : Server or dict
        An object containing the ARK server connection details. Must provide at 
        least `host`, `password`, and `port` attributes or keys.

    Attributes
    ----------
    name : str
        A name for the ARK server. Defaults to 'UnnamedServer' if not provided.
    host : str
        The server's host or IP address.
    port : int
        The RCON port of the server.
    password : str
        The RCON admin password.
    """

    _PLAYER_PATTERN = r"""^\s*\d+\.\s+(?P<name>.*?),\s*(?P<steam_id>\d+)\s*$"""
    PLAYER_RE = re.compile(_PLAYER_PATTERN)

    def __init__(self, server: Union[Server, dict]):
        """
        Initialize ArkRcon with the given server credentials.

        Accepts either a Server instance or a dictionary. The dictionary must 
        provide:
            - 'host': str – server host or IP
            - 'password': str – RCON admin password
            - 'port': int – RCON connection port
        Optionally:
            - 'name': str – name for the server (default: 'UnnamedServer')

        Parameters
        ----------
        server : Server or dict
            The server credentials.

        Raises
        ------
        ValueError
            If required attributes are missing.
        """
        if isinstance(server, Server):
            self.name = server.name
            self.host = server.host
            self.password = server.admin_password
            self.port = server.rcon_port
        elif isinstance(server, dict):
            try:
                self.name = server.get('name', 'UnnamedServer')
                self.host = server['host']
                self.password = server['password']
                self.port = server['port']
            except KeyError as e:
                raise ValueError(
                    f"Missing required server attribute: {e}") from e
        else:
            raise ValueError(
                "Server must be a Server instance or a dict with keys: 'host', "
                "'password', 'port'")

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
        response = self._run_command("ListPlayers")
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

    def broadcast(self, message: Union[str, list[str]]) -> str:
        """
        Broadcast a message to all players on the ARK server.

        Parameters
        ----------
        message : str or list of str
            The message to broadcast. If a list is passed, each item will 
            become is a separate line.

        Returns
        -------
        str
            The response from the server.
        """
        if isinstance(message, list):
            message_str = '\n'.join(message)
        else:
            message_str = message

        command = f'Broadcast {message_str}'
        return self._run_command(command)

    def save_world(self) -> str:
        """
        Saves the current world state on the ARK server.

        Returns
        -------
        str
            The response from the server.
        """
        command = 'SaveWorld'
        return self._run_command(command)

    def kick_player(self, player_or_steam_id: Union[Player, str | int]) -> str:
        """
        Kicks a single player from the ARK server.

        Parameters
        ----------
        player_or_steam_id : Player or str|int
            The Player object or their steam_id.

        Returns
        -------
        str
            The server's response to the KickPlayer command.
        """
        if isinstance(player_or_steam_id, Player):
            steam_id = player_or_steam_id.steam_id
        else:
            steam_id = player_or_steam_id

        return self._run_command(f"KickPlayer {steam_id}")

    def kick_all_players(self) -> list[tuple[Player, str]]:
        """
        Kicks all currently connected players from the ARK server.

        Returns
        -------
        list of tuple(Player, str)
            Each tuple contains the Player object and the server's response to 
            the KickPlayer command.
        """
        results = []
        players = self.list_players()

        for player in players:
            response = self.kick_player(player)
            results.append((player, response))

        return results
