from prettytable import PrettyTable

from src.ark_rcon import ArkRcon
from ._utils import get_servers


def list_players(args):
    """
    List players who are currently connected to servers and print totals.
    """
    total_players = 0

    for server in get_servers(args.servers):
        ark_rcon = ArkRcon(server)

        print("=" * 60)
        print(f"Listing players: {server.name} ({server.host})")
        print("=" * 60)
        players = ark_rcon.list_players()

        num_players = len(players)
        total_players += num_players

        if players:
            table = PrettyTable()
            table.field_names = ["Player Name", "Steam ID"]

            for player in players:
                table.add_row([player.name, player.steam_id])

            print(table)
            print(f'Total players on this server: {num_players}\n')
        else:
            print("No players currently connected.\n")

    print("=" * 60)
    print(f"Total players on all servers: {total_players}\n")


def broadcast(args):
    """
    Broadcast a message to all players on the servers.
    """
    if len(args.message) == 1:
        message = args.message[0]
    else:
        message = args.message

    for server in get_servers(args.servers):
        ark_rcon = ArkRcon(server)

        print("=" * 60)
        print(f"Broadcasting to: {server.name} ({server.host})")
        print("=" * 60)
        response = ark_rcon.broadcast(message)
        print(response)
        print('')


def save_world(args):
    """
    Save the world on the servers.
    """
    for server in get_servers(args.servers):
        ark_rcon = ArkRcon(server)

        print("=" * 60)
        print(f"Saving world on: {server.name} ({server.host})")
        print("=" * 60)
        response = ark_rcon.save_world()
        print(response)
        print('')


def kick_all_players(args):
    """
    Kick all players from the servers.
    """
    for server in get_servers(args.servers):
        ark_rcon = ArkRcon(server)

        print("=" * 60)
        print(f"Kicking all players on: {server.name} ({server.host})")
        print("=" * 60)

        results = ark_rcon.kick_all_players()

        if results:
            for player, response in results:
                print(f"Kicked {player.name} ({player.steam_id}): {response}")
        else:
            print("No players currently connected.")

        print('')
