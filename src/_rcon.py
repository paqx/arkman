from prettytable import PrettyTable
from rcon.exceptions import EmptyResponse

from src.ark_rcon import ArkRcon
from ._utils import get_servers


def list_players(args):
    """
    List players who are currently connected to servers and print totals.
    """
    total_players = 0

    for server in get_servers(args.servers):
        print("=" * 60)
        print(f"Listing players: {server.name} ({server.host})")
        print("=" * 60)

        try:
            ark_rcon = ArkRcon(server)
            players = ark_rcon.list_players()
        except EmptyResponse:
            print('Failed to execute RCON command.\n')
            continue

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


def kick_player(args):
    """
    Kick a player from a server.
    """
    servers = get_servers(args.server)

    if not servers:
        print(f'Incorrect server name: {args.server}')
        return

    print(f"Kicking player {args.steam_id} from {servers[0].name})")

    try:
        ark_rcon = ArkRcon(servers[0])
        response = ark_rcon.kick_player(args.steam_id)
    except EmptyResponse:
        print('Failed to execute RCON command.\n')

    print(f"Result: {response}")


def broadcast(args):
    """
    Broadcast a message to all players on the servers.
    """
    if len(args.message) == 1:
        message = args.message[0]
    else:
        message = args.message

    for server in get_servers(args.servers):
        try:
            ark_rcon = ArkRcon(server)
            response = ark_rcon.broadcast(message)
        except EmptyResponse:
            print('Failed to execute RCON command.\n')
            continue

        print("=" * 60)
        print(f"Broadcasting to: {server.name} ({server.host})")
        print("=" * 60)
        print(response)
        print('')


def save_world(args):
    """
    Save the world on the servers.
    """
    for server in get_servers(args.servers):
        try:
            ark_rcon = ArkRcon(server)
            response = ark_rcon.save_world()
        except EmptyResponse:
            print('Failed to execute RCON command.\n')
            continue

        print("=" * 60)
        print(f"Saving world on: {server.name} ({server.host})")
        print("=" * 60)
        print(response)
        print('')


def kick_all_players(args):
    """
    Kick all players from the servers.
    """
    for server in get_servers(args.servers):
        try:
            ark_rcon = ArkRcon(server)
            results = ark_rcon.kick_all_players()
        except EmptyResponse:
            print('Failed to execute RCON command.\n')
            continue

        print("=" * 60)
        print(f"Kicking all players on: {server.name} ({server.host})")
        print("=" * 60)

        if results:
            for player, response in results:
                print(f"Kicked {player.name} ({player.steam_id}): {response}")
        else:
            print("No players currently connected.")

        print('')
