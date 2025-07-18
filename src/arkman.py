import argparse

from config import CFG
from src import _ark_hoster
from src import _bak
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
        'config', help='Configuration management via FTP')
    parser_rcon = subparsers.add_parser(
        'rcon', help='Server management via RCON')
    parser_ark_hoster = subparsers.add_parser(
        'arkhoster', help='Server management via the web panel (this is specific to ark-hoster.ru)')
    parser_bak = subparsers.add_parser(
        'bak', help='Back-up management via FTP')

    # SUBCOMMAND: config
    config_subparsers = parser_config.add_subparsers(
        dest='action', required=True)

    # pull command
    parser_pull = config_subparsers.add_parser(
        'pull', help='Download configs from servers')
    parser_pull.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_pull.set_defaults(func=_config.pull)

    # push command
    parser_push = config_subparsers.add_parser(
        'push', help='Upload configs to servers')
    parser_push.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_push.set_defaults(func=_config.push)

    # load command
    parser_load = config_subparsers.add_parser(
        'load', help='Generate YAML configs from INI configs')
    parser_load.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_load.set_defaults(func=_config.load)

    # dump command
    parser_dump = config_subparsers.add_parser(
        'dump', help='Generate INI configs from YAML configs')
    parser_dump.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_dump.set_defaults(func=_config.dump)

    # load_supply_crates_from_csv command
    parser_load_supply_crates_from_csv = config_subparsers.add_parser(
        'load_supply_crates_from_csv',
        help='Generate ConfigOverrideSupplyCrateItems YAML configs from a '
        'CSV file')
    parser_load_supply_crates_from_csv.add_argument(
        '-i', '--input_file', help='Absolute path to the CSV input file'
    )
    parser_load_supply_crates_from_csv.add_argument(
        '-o', '--output_file',
        help='Relative path to the YAML output file (will be placed in '
        './config/includes)'
    )
    parser_load_supply_crates_from_csv.set_defaults(
        func=_config.load_supply_crates_from_csv)

    # SUBCOMMAND: rcon
    rcon_subparsers = parser_rcon.add_subparsers(dest='action', required=True)

    # list players command
    parser_list_players = rcon_subparsers.add_parser(
        'list_players', help='List players who are currently connected to servers')
    parser_list_players.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_list_players.set_defaults(func=_rcon.list_players)

    # kick player command
    parser_kick_player = rcon_subparsers.add_parser(
        'kick_player', help='Kick player from a server')
    parser_kick_player.add_argument(
        '-s', '--server', choices=server_names, required=True)
    parser_kick_player.add_argument('-i', '--steam_id', required=True)
    parser_kick_player.set_defaults(func=_rcon.kick_player)

    # broadcast command
    parser_broadcast = rcon_subparsers.add_parser(
        'broadcast', help='Broadcast a message to all players on the server'
    )
    parser_broadcast.add_argument(
        '-s', '--servers', nargs='+', choices=server_names,
        help='Specify which servers to broadcast to'
    )
    parser_broadcast.add_argument(
        '-m', '--message',
        nargs='+',
        help='The message to broadcast (for multi-line messages, provide several arguments)'
    )
    parser_broadcast.set_defaults(func=_rcon.broadcast)

    # save_world command
    parser_save_world = rcon_subparsers.add_parser(
        'save_world', help='Save the world on the servers'
    )
    parser_save_world.add_argument(
        '-s', '--servers', nargs='+', choices=server_names,
        help='Specify which servers to save the world on'
    )
    parser_save_world.set_defaults(func=_rcon.save_world)

    # kick_all_players command
    parser_kick_all_players = rcon_subparsers.add_parser(
        'kick_all_players', help='Kick all players from the servers'
    )
    parser_kick_all_players.add_argument(
        '-s', '--servers', nargs='+', choices=server_names,
        help='Specify which servers to kick all players from'
    )
    parser_kick_all_players.set_defaults(func=_rcon.kick_all_players)

    # SUBCOMMAND: ark_hoster
    ark_hoster_subparsers = parser_ark_hoster.add_subparsers(
        dest='action', required=True)

    # restart command
    restart_delays = [1, 2, 3, 4] + list(range(5, 31, 5))

    parser_restart = ark_hoster_subparsers.add_parser(
        'restart', help='Restart servers')
    parser_restart.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_restart.add_argument(
        '-d', '--delay',  default=15, type=int, choices=restart_delays,
        help='Delay in minutes before the restart (default: 15)')
    parser_restart.set_defaults(func=_ark_hoster.restart)

    # SUBCOMMAND: bak
    bak_subparsers = parser_bak.add_subparsers(
        dest='action', required=True)

    # make command
    parser_make_bak = bak_subparsers.add_parser(
        'make', help='Create compressed local backups.'
    )
    parser_make_bak.add_argument(
        '-s', '--servers', nargs='+', choices=server_names,
        help='Specify which servers to back up'
    )
    parser_make_bak.set_defaults(func=_bak.make)

    args = parser.parse_args()
    args.func(args)
