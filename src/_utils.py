from typing import Optional

from config import CFG, Server


def servers(server_names: Optional[Server] = None) -> list[Server]:
    """
    Get a list of servers by their names.

    Parameters
    ----------
    server_names : Optional[Server], default None
        A list of server names to filter the servers. If None, all servers are returned.

    Returns
    -------
    list of Server
        A list of Server objects matching the given names, or all servers if no 
        names are specified.
    """
    if server_names is not None:
        return [s for s in CFG.servers if s.name in server_names]

    return CFG.servers
