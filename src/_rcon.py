from prettytable import PrettyTable

from src.ark_rcon import ArkRcon
from ._utils import servers


def list_players(args):
    """
    List players who are currently connected to servers.
    """
    for server in servers(args.servers):
        cli = ArkRcon(
            host=server.host,
            port=server.rcon_port,
            password=server.admin_password
        )

        print("=" * 60)
        print(f"Listing players: {server.name} ({server.host})")
        print("=" * 60)
        players = cli.list_players()

        if players:
            table = PrettyTable()
            table.field_names = ["Player Name", "Steam ID"]

            for player in players:
                table.add_row([player.name, player.steam_id])

            print(table)
            print('')
        else:
            print("No players currently connected.\n")
