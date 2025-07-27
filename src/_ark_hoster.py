import sys
import re
import time
import os
import json
from concurrent.futures import ThreadPoolExecutor

import requests
from rcon.exceptions import EmptyResponse

from config import ArkHoster, ARK_HOSTER
from src.ark_rcon import ArkRcon
from ._utils import get_servers

M_RESTART_DEFAULT = "Server will be restarted in {minutes} min. {seconds} sec."
M_RESTART = os.environ.get('ARK_HOSTER_M_RESTART')

if M_RESTART is not None:
    M_RESTART = M_RESTART.replace('\\n', '\n')
else:
    M_RESTART = M_RESTART_DEFAULT


def _web_login(
    session: requests.Session,
    ark_hoster: ArkHoster
) -> dict[str, str]:
    """Login to Ark Hoster panel and return headers with csrf token

    Parameters
    ----------
    session : requests.Session
        HTTP session
    ark_hoster : ArkHoster
        ArkHoster credentials

    Returns
    -------
    dict
        HTTP headers for authenticated requests
    """
    base_url = ark_hoster.base_url
    login_page = f'{base_url}/main/index/'
    response = session.get(login_page)

    match = re.search(
        r'<meta name="CSRF_TOKEN" content="([^"]+)"', response.text)
    if not match:
        raise Exception('Failed to retrieve a CSRF token')

    csrf_token = match.group(1)
    login_url = f'{base_url}/account/login/ajax'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': base_url.replace("https://", ""),
        'Origin': base_url,
        'Referer': login_page,
        'User-Agent': ark_hoster.user_agent,
        'X-CSRF-Token': csrf_token,
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'email': ark_hoster.email,
        'password': ark_hoster.password,
        'google_code_auth': '',
        'g-recaptcha-response': '',
        'remember_auth_user': 'remember-me',
    }
    response = session.post(login_url, data=data, headers=headers)

    if not response.ok:
        raise Exception(f'Login failed: {response.text}')

    return headers


def _send_restart_request(
    server_id: str,
    session: requests.Session,
    headers: dict[str, str],
    base_url: str
) -> tuple[str, int, str]:
    """Perform HTTP request to restart the server

    Parameters
    ----------
    server_id : str
        Server ID
    session : requests.Session
        Authenticated HTTP session
    headers : dict
        HTTP headers with CSRF
    base_url : str
        Panel base URL

    Returns
    -------
    tuple of (server_id, http_code, response_text)
    """
    restart_url = f'{base_url}/servers/control/action/{server_id}/restart'
    response = session.post(restart_url, headers=headers)
    return server_id, response.status_code, response.text


def restart(args):
    """
    Restart the servers by sending HTTP requests to the ark-hoster.ru web panel.
    """
    servers = get_servers(args.servers)
    ark_rcons = [ArkRcon(s) for s in servers]
    delay_seconds: int = args.delay * 60

    print(
        f"Scheduled server restart: {', '.join([s.name for s in servers])} "
        f"in {args.delay} minutes.\n"
        "You can cancel by pressing Ctrl+C."
    )

    dispatched_notifications = set()
    interactive = sys.stdin.isatty()

    for seconds_left in range(delay_seconds, 0, -1):
        mins, secs = divmod(seconds_left, 60)
        should_notify = False

        if seconds_left > 300 and seconds_left % 300 == 0:
            notification_time = seconds_left
            should_notify = True
        elif 60 < seconds_left <= 300 and seconds_left % 60 == 0:
            notification_time = seconds_left
            should_notify = True
        elif seconds_left <= 60 and seconds_left % 20 == 0:
            notification_time = seconds_left
            should_notify = True
        else:
            notification_time = None

        if should_notify and notification_time not in dispatched_notifications:
            dispatched_notifications.add(notification_time)

            prefix = '\n' if interactive else ''
            print(f'{prefix}Dispatching notifications...')
            message = M_RESTART.format(minutes=mins, seconds=secs)

            for ark_rcon in ark_rcons:
                try:
                    print(f'Broadcasting on {ark_rcon.name}...')
                    ark_rcon.broadcast(message)
                except ConnectionRefusedError:
                    print('Connection refused.\n')
                except EmptyResponse:
                    print('Failed to execute RCON command.\n')

        if seconds_left == 30:
            for ark_rcon in ark_rcons:
                try:
                    print(f'Saving world on {ark_rcon.name}...')
                    ark_rcon.save_world()

                    print(f'Kicking all players from {ark_rcon.name}...')
                    ark_rcon.kick_all_players()
                except ConnectionRefusedError:
                    print(f'Connection refused by {ark_rcon.name}.\n')
                except EmptyResponse:
                    print(
                        f'Failed to execute RCON command on {ark_rcon.name}.\n')

        countdown_msg = f"Restarting in {mins:02d}:{secs:02d}"

        if interactive:
            print(f"\r{countdown_msg} ", end='', flush=True)
        else:
            if seconds_left % 30 == 0:
                print(countdown_msg)

        time.sleep(1)

    print("\nRestarting servers...")

    session = requests.Session()
    headers = _web_login(session, ARK_HOSTER)

    with ThreadPoolExecutor(max_workers=len(servers)) as executor:
        futures = [
            executor.submit(
                _send_restart_request,
                s.id_,
                session,
                headers,
                ARK_HOSTER.base_url
            ) for s in servers
        ]

        for future in futures:
            server_id, code, text = future.result()
            msg = f"Server {server_id} responded with code {code}: "

            if not text or not text.strip():
                msg += "(empty response body)"
            else:
                try:
                    data = json.loads(text)

                    if 'success' in data:
                        msg += data['success']
                    elif 'error' in data:
                        msg += data['error']
                    else:
                        msg += "(no success or error message in response)"
                except Exception as e:
                    msg += f"(could not parse response: {e}): {text}"

            print(msg)
