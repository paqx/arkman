import argparse

from config import CFG
from src import _config
from src import _rcon


def main():
    """
    Main function to handle command line arguments and call appropriate handlers.
    """
    server_names = [server.name for server in CFG.servers]

    parser = argparse.ArgumentParser(
        description='A console utility for managing ARK server settings'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # COMMANDS
    parser_config = subparsers.add_parser(
        'config', help='Configuration management')
    parser_rcon = subparsers.add_parser(
        'rcon', help='Server management via RCON')

    # SUBCOMMAND: config
    config_subparsers = parser_config.add_subparsers(
        dest='action', required=True)

    # Pull command
    parser_pull = config_subparsers.add_parser(
        'pull', help='Download configs from servers')
    parser_pull.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_pull.set_defaults(func=_config.pull)

    # Push command
    parser_push = config_subparsers.add_parser(
        'push', help='Upload configs to servers')
    parser_push.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_push.set_defaults(func=_config.push)

    # Load command
    parser_load = config_subparsers.add_parser(
        'load', help='Generate YAML configs from INI configs')
    parser_load.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_load.set_defaults(func=_config.load)

    # Dump command
    parser_dump = config_subparsers.add_parser(
        'dump', help='Generate INI configs from YAML configs')
    parser_dump.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_dump.set_defaults(func=_config.dump)

    # SUBCOMMAND: rcon
    rcon_subparsers = parser_rcon.add_subparsers(dest='action', required=True)

    # RCON command
    parser_list_players = rcon_subparsers.add_parser(
        'list_players', help='List players who are currently connected to servers')
    parser_list_players.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_list_players.set_defaults(func=_rcon.list_players)

    args = parser.parse_args()
    args.func(args)
