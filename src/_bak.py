import ftplib
import os
import re
from datetime import datetime
import gzip
from io import BytesIO
from typing import Optional

from ._utils import get_servers


REMOTE_DIR = '/ShooterGame/Saved/SavedArks'

EXTENSIONS = [
    'ark',
    'arkprofile',
    'arktribe',
    'arktributetribe',
    'profilebak',
    'tribebak',
]
EXT_PATTERN = r'\.(?:' + '|'.join(EXTENSIONS) + r')$'
EXT_RE = re.compile(EXT_PATTERN, re.IGNORECASE)

LAST_SAVE_PATTERN = r'^\w+(?:_P)?\.ark$'
LAST_SAVE_RE = re.compile(LAST_SAVE_PATTERN, re.IGNORECASE)


def ftp_mlsd_list(ftp: ftplib.FTP) -> dict[str, dict]:
    """Return a dict of files and their facts from FTP MLSD listing."""
    files = {}

    for name, facts in ftp.mlsd():
        if facts.get('type') == 'file':
            files[name] = facts

    return files


def should_fetch(local_dir: str, filename: str, facts: dict[str, str]):
    """Decide whether a remote file should be fetched and backed up."""
    if not EXT_RE.search(filename):
        return False

    local_path = os.path.join(local_dir, filename + '.gz')

    if not os.path.exists(local_path):
        return True

    if LAST_SAVE_RE.match(filename):
        ftp_time = datetime.strptime(
            facts["modify"][:14], "%Y%m%d%H%M%S").timestamp()
        local_mtime = os.path.getmtime(local_path)

        if abs(local_mtime - ftp_time) > 120:
            return True

        return False

    return False


def get_mtime_from_facts(facts: dict[str, str]) -> float:
    """Extract and return modification time from MLSD facts as a timestamp."""
    return datetime.strptime(facts["modify"][:14], "%Y%m%d%H%M%S").timestamp()


def ftp_download(ftp: ftplib.FTP, filename: str) -> bytes:
    """
    Download a file from FTP to memory and return its bytes.
    """
    buf = BytesIO()
    ftp.retrbinary(f"RETR {filename}", buf.write)
    return buf.getvalue()


def gzip_data(
    data: bytes,
    filename: Optional[str],
    mtime: Optional[float]
) -> bytes:
    """
    Compress data with gzip and return compressed bytes.
    """
    buf = BytesIO()
    kwargs = {}

    if filename is not None:
        kwargs['filename'] = filename
    if mtime is not None:
        kwargs['mtime'] = mtime

    with gzip.GzipFile(fileobj=buf, mode='wb', **kwargs) as gz:
        gz.write(data)

    return buf.getvalue()


def make(args):
    """
    Download files from remote servers via FTP and store local compressed 
    copies.
    """
    for server in get_servers(args.servers):
        print("=" * 60)
        print(f"Back up server: {server.name} ({server.host})")
        print("=" * 60)

        try:
            ftp = ftplib.FTP(server.host, server.user, server.password)

            try:
                ftp.cwd(REMOTE_DIR)
            except Exception as e:
                print(f"Failed to change directory: {e}")
                ftp.quit()
                continue

            local_dir = os.path.join('./bak', server.name)
            os.makedirs(local_dir, exist_ok=True)
            files = ftp_mlsd_list(ftp)

            for filename, facts in files.items():
                if should_fetch(local_dir, filename, facts):
                    print(f"- Backing up {filename}... ", end='')

                    try:
                        local_gz_file = os.path.join(
                            local_dir, filename + '.gz')
                        mtime = get_mtime_from_facts(facts)
                        data = ftp_download(ftp, filename)
                        gzipped_data = gzip_data(data, filename, mtime)

                        with open(local_gz_file, 'wb') as f:
                            f.write(gzipped_data)
                        os.utime(local_gz_file, (mtime, mtime))
                        print("Success")
                    except Exception as e:
                        print(f"Failed: {e}")
                else:
                    print(f"- Skipping {filename}")
        except Exception as e:
            print(f"Could not connect to {server.name} ({server.host}): {e}\n")
            continue
        finally:
            try:
                ftp.quit()
            except Exception:
                pass

        print(f"DONE backing up files for {server.name}\n")
