import argparse
import ftplib
import os
from pathlib import Path

from src.ark_config import ArkConfig
from config import CFG

REMOTE_FILES = {
    '/ShooterGame/Saved/Config/WindowsServer': [
        ('Game.ini', 'utf-8'),
        ('GameUserSettings.ini', 'utf-16'),
    ],
}


def _handler_pull(args):
    """
    Pull configuration files from remote servers.
    """
    if args.servers is not None:
        servers = [s for s in CFG.servers if s.name in args.servers]
    else:
        servers = CFG.servers

    for server in servers:
        print("=" * 60)
        print(f"Connecting to server: {server.name} ({server.host})")
        print("=" * 60)

        try:
            ftp = ftplib.FTP(server.host, server.user, server.password)
        except Exception as e:
            print(
                f"Could not connect to {server.name} ({server.host}): {e}\n"
            )
            continue

        for remote_dir, filenames in REMOTE_FILES.items():
            print(f"\nRemote directory: {remote_dir}")

            try:
                ftp.cwd(remote_dir)
            except Exception as e:
                print(f"Failed to change directory: {e}")
                continue

            local_dir = os.path.join('./configs/ini', server.name)
            os.makedirs(local_dir, exist_ok=True)

            for filename, _ in filenames:
                local_path = os.path.join(local_dir, filename)
                print(f"- Downloading {remote_dir}/{filename}... ", end="")

                try:
                    with open(local_path, "wb") as f:
                        ftp.retrbinary(f"RETR {filename}", f.write)
                    print("Success")
                except Exception as e:
                    print(f"Failed: {e}")
            print(f"Finished directory: {remote_dir}")

        ftp.quit()
        print(f"DONE pulling files for {server.name}\n")

    print("=" * 60)


def _handler_push(args):
    """
    Push local configuration files to remote servers.
    """
    if args.servers is not None:
        servers = [s for s in CFG.servers if s.name in args.servers]
    else:
        servers = CFG.servers

    for server in servers:
        print("=" * 60)
        print(f"Connecting to server: {server.name} ({server.host})")
        print("=" * 60)

        try:
            ftp = ftplib.FTP(server.host, server.user, server.password)
        except Exception as e:
            print(
                f"Could not connect to {server.name} ({server.host}): {e}\n"
            )
            continue

        for remote_dir, filenames in REMOTE_FILES.items():
            print(f"\nRemote directory: {remote_dir}")

            try:
                ftp.cwd(remote_dir)
            except Exception as e:
                print(f"Failed to change directory: {e}")
                continue

            local_dir = os.path.join('./configs/ini', server.name)

            for filename, _ in filenames:
                local_path = os.path.join(local_dir, filename)
                print(
                    f"- Uploading {local_path} to {remote_dir}/{filename}... ", end="")

                if not os.path.isfile(local_path):
                    print(f"Local file does not exist: {local_path}")
                    continue

                try:
                    with open(local_path, "rb") as f:
                        ftp.storbinary(f"STOR {filename}", f)
                    print("Success")
                except Exception as e:
                    print(f"Failed: {e}")

            print(f"Finished directory: {remote_dir}")

        ftp.quit()
        print(f"DONE pushing files for {server.name}\n")

    print("=" * 60)


def _handler_load(args):
    """
    Create YAML configs from INI configs.
    """
    for server in CFG.servers:
        print(f"Processing server: {server.name}")
        filenames = REMOTE_FILES['/ShooterGame/Saved/Config/WindowsServer']

        for filename, encoding in filenames:
            ini_path = os.path.join('./configs/ini', server.name, filename)

            if not os.path.isfile(ini_path):
                print(f"INI config does not exist: {ini_path}")
                continue

            print(f"Reading INI config: {ini_path}")
            config = ArkConfig(encoding=encoding)
            config.read(ini_path)

            yml_dir = './configs/yml'
            os.makedirs(yml_dir, exist_ok=True)
            basename = Path(filename).stem
            yaml_path = os.path.join(
                yml_dir, f'{basename}.{server.name}.yml')

            print(f"Saving configuration to YAML: {yaml_path}")
            config.to_yaml_file(yaml_path)

        print(f"Completed processing server: {server.name}\n")


def _handler_dump(args):
    """
    Create INI configs from YAML configs.
    """
    for server in CFG.servers:
        print(f"Processing server: {server.name}")
        filenames = REMOTE_FILES['/ShooterGame/Saved/Config/WindowsServer']

        for filename, encoding in filenames:
            basename = Path(filename).stem
            yaml_path = os.path.join(
                './configs/yml', f'{basename}.{server.name}.yml')

            if not os.path.isfile(yaml_path):
                print(f"YAML config does not exist: {yaml_path}")
                continue

            print(f"Reading YAML config: {yaml_path}")
            config = ArkConfig.from_yaml_file(yaml_path)
            config.encoding = encoding

            ini_dir = os.path.join('./configs/ini', server.name)
            os.makedirs(ini_dir, exist_ok=True)
            ini_path = os.path.join(ini_dir, filename)

            print(f"Saving configuration to INI: {ini_path}")
            config.write(ini_path)

        print(f"Completed processing server: {server.name}\n")


def main():
    """
    Main function to handle command line arguments and call appropriate handlers.
    """
    server_names = [server.name for server in CFG.servers]

    parser = argparse.ArgumentParser(
        description='A console utility for managing ARK server settings'
    )
    subparsers = parser.add_subparsers(required=True)

    # Pull command
    parser_pull = subparsers.add_parser(
        'pull', help='Download configs from servers')
    parser_pull.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_pull.set_defaults(func=_handler_pull)

    # Push command
    parser_push = subparsers.add_parser(
        'push', help='Upload configs to servers')
    parser_push.add_argument(
        '-s', '--servers', nargs='+', choices=server_names)
    parser_push.set_defaults(func=_handler_push)

    # Load command
    parser_load = subparsers.add_parser(
        'load', help='Generate YAML configs from INI configs')
    parser_load.set_defaults(func=_handler_load)

    # Dump command
    parser_dump = subparsers.add_parser(
        'dump', help='Generate INI configs from YAML configs')
    parser_dump.set_defaults(func=_handler_dump)

    args = parser.parse_args()
    args.func(args)
