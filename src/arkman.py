import argparse
import ftplib
import os

from config import cfg


REMOTE_FILES = {
    '/ShooterGame/Saved/Config/WindowsServer': [
        'Game.ini',
        'GameUserSettings.ini',
    ],
}


def pull_handler(args):
    for server in cfg.servers:
        ftp = ftplib.FTP(server.host, server.user, server.password)

        for remote_dir, filenames in REMOTE_FILES.items():
            print(f'PULLING FILES FOR {server.name}:')
            ftp.cwd(remote_dir)
            local_dir = os.path.join(
                f'./configs/compiled/{server.name}', os.path.relpath(remote_dir, '/'))
            os.makedirs(local_dir, exist_ok=True)

            for filename in filenames:
                local_path = os.path.join(local_dir, filename)

                with open(local_path, "wb") as f:
                    try:
                        print(f"Retrieving {remote_dir}/{filename}...")
                        ftp.retrbinary(f"RETR {filename}", f.write)
                        print('OK')
                    except Exception as e:
                        print(
                            f"Failed to retrieve {remote_dir}/{filename}: {e}")
            print(F'DONE {server.name}\n')
        ftp.quit()


def compile_handler(args):
    pass


def push_handler(args):
    pass


def main():
    parser = argparse.ArgumentParser(description='ARK Server Management Tool.')
    subparsers = parser.add_subparsers(
        dest='command', required=True, help='Available commands')

    # Pull command
    pull_parser = subparsers.add_parser(
        'pull', help='Fetch configs from servers')
    pull_parser.set_defaults(func=pull_handler)
    # Add pull-specific args here

    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Generate configs')
    compile_parser.set_defaults(func=compile_handler)
    # Add compile-specific args here

    # Push command
    push_parser = subparsers.add_parser('push', help='Send configs to servers')
    push_parser.set_defaults(func=push_handler)
    # Add push-specific args here

    # Parse the arguments
    args = parser.parse_args()
    args.func(args)
