import argparse
import ftplib
import os
from pathlib import Path

from src.ark_config import ArkConfig
from config import CFG


REMOTE_FILES = {
    '/ShooterGame/Saved/Config/WindowsServer': [
        'Game.ini',
        'GameUserSettings.ini',
    ],
}


def _handler_pull(args):
    for server in CFG.servers:
        print("="*60)
        print(f"Connecting to server: {server.name} ({server.host})")
        print("="*60)

        try:
            ftp = ftplib.FTP(server.host, server.user, server.password)
        except Exception as e:
            print(
                f"Could not connect to {server.name} ({server.host}): {e}\n")
            continue

        for remote_dir, filenames in REMOTE_FILES.items():
            print(f"\nRemote directory: {remote_dir}")

            try:
                ftp.cwd(remote_dir)
            except Exception as e:
                print(f"Failed to change directory: {e}")
                continue

            local_dir = os.path.join('./configs/merged', server.name)
            os.makedirs(local_dir, exist_ok=True)

            for filename in filenames:
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

    print("="*60)


def _handler_merge(args):
    for server in CFG.servers:
        for filename in REMOTE_FILES['/ShooterGame/Saved/Config/WindowsServer']:
            basename = Path(filename).stem
            base_yaml_path = os.path.join(
                './configs/base', f'{basename}.yml')

            if not os.path.isfile(base_yaml_path):
                print(f"Base YAML config does not exist: {base_yaml_path}")
                continue

            config = ArkConfig.from_yaml_file(base_yaml_path)

            patch_yaml_path = os.path.join(
                f'./configs/patches/{server.name}', f'{basename}.yml')

            if os.path.isfile(patch_yaml_path):
                config_patch = ArkConfig.from_yaml_file(patch_yaml_path)
                config = config.merge(config_patch)

            ini_dir = os.path.join('./configs/merged', server.name)
            os.makedirs(ini_dir, exist_ok=True)
            ini_path = os.path.join(ini_dir, filename)
            config.sort()
            config.write(ini_path)


def _handler_push(args):
    for server in CFG.servers:
        print("="*60)
        print(f"Connecting to server: {server.name} ({server.host})")
        print("="*60)

        try:
            ftp = ftplib.FTP(server.host, server.user, server.password)
        except Exception as e:
            print(
                f"Could not connect to {server.name} ({server.host}): {e}\n")
            continue

        for remote_dir, filenames in REMOTE_FILES.items():
            print(f"\nRemote directory: {remote_dir}")

            try:
                ftp.cwd(remote_dir)
            except Exception as e:
                print(f"Failed to change directory: {e}")
                continue

            local_dir = os.path.join('./configs/merged', server.name)

            for filename in filenames:
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

    print("="*60)


def _handler_make(args):
    if args.server_name == 'all':
        server_names = [server.name for server in CFG.servers]
    else:
        server_names = [args.server_name]

    for server_name in server_names:
        for filename in REMOTE_FILES['/ShooterGame/Saved/Config/WindowsServer']:
            ini_path = os.path.join(
                './configs/merged', server_name, filename)

            basename = Path(filename).stem
            yaml_path = os.path.join(
                './configs/base', f'{basename}.{server_name}.yml')

            if not os.path.isfile(ini_path):
                print(f"INI config does not exist: {ini_path}")
                continue

            config = ArkConfig()
            config.read(ini_path)

            if args.sort:
                config.sort()

            config.to_yaml_file(yaml_path)


def main():
    parser = argparse.ArgumentParser(
        'Ark Manager', description='A console utility for managing ARK Survival Evolved server settings')
    subparsers = parser.add_subparsers(required=True)

    # Pull command
    parser_pull = subparsers.add_parser(
        'pull', help='Download configs from servers')
    parser_pull.set_defaults(func=_handler_pull)

    # Merge command
    parser_merge = subparsers.add_parser(
        'merge', help='Generate merged INI configs for all maps from the base and YAML config and YAML patches')
    parser_merge.set_defaults(func=_handler_merge)

    # Push command
    parser_push = subparsers.add_parser(
        'push', help='Upload configs to servers')
    parser_push.set_defaults(func=_handler_push)

    # Make command
    parser_make = subparsers.add_parser(
        'make', help='Make YAML configs from merged INI configs')
    make_choices = [server.name for server in CFG.servers]
    make_choices.append('all')
    parser_make.add_argument(
        'server_name', choices=make_choices)
    parser_make.add_argument(
        '-s', '--sort',
        action='store_true',
        default=True,
        help='Sort each section of the config by keys')
    parser_make.set_defaults(func=_handler_make)

    args = parser.parse_args()
    args.func(args)
