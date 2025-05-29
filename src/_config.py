import ftplib
import os
import sys
from dataclasses import asdict
from pathlib import Path

import yaml

from src.ark_config import ArkConfig, csv_to_supply_crate_items
from ._utils import get_servers


REMOTE_FILES = {
    '/ShooterGame/Saved/Config/WindowsServer': [
        ('Game.ini', 'utf-8'),
        ('GameUserSettings.ini', 'utf-16'),
    ],
}


def pull(args):
    """
    Pull configuration files from remote servers.
    """
    for server in get_servers(args.servers):
        print("=" * 60)
        print(f"Pulling from server: {server.name} ({server.host})")
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


def push(args):
    """
    Push local configuration files to remote servers.
    """
    for server in get_servers(args.servers):
        print("=" * 60)
        print(f"Pushing to server: {server.name} ({server.host})")
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


def load(args):
    """
    Create YAML configs from INI configs.
    """
    for server in get_servers(args.servers):
        print("=" * 60)
        print(f"Loading server: {server.name} ({server.host})")
        print("=" * 60)

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

        print(f"DONE loading server: {server.name}\n")


def dump(args):
    """
    Create INI configs from YAML configs.
    """
    for server in get_servers(args.servers):
        print("=" * 60)
        print(f"Dumping server: {server.name} ({server.host})")
        print("=" * 60)

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

        print(f"DONE dumping server: {server.name}\n")


def load_supply_crates_from_csv(args):
    """
    Create ConfigOverrideSupplyCrateItems YAML configs from a CSV file.
    """
    def dict_without_nones(value) -> dict:
        return {k: v for k, v in value if v is not None}

    if not os.path.isfile(args.input_file):
        print(f"Error: CSV file '{args.input_file}' does not exist.")
        sys.exit(1)

    output_file = os.path.join('./configs/yml/includes', args.output_file)
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)
    supply_crate_items = csv_to_supply_crate_items(args.input_file)
    data = [asdict(
        i, dict_factory=dict_without_nones) for i in supply_crate_items]

    print(f"Saving configuration to YAML: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)

    print("DONE")
