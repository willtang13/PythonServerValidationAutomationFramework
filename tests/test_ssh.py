
import os
import getpass

import paramiko
import pytest


@pytest.fixture(scope="module")
def ssh_client():
    """Setup and teardown the SSH connection."""

    key_path = os.path.expanduser(
        "~/.ssh/serverlab_ed25519"
    )

    passphrase = getpass.getpass("SSH key passphrase: ")

    client = paramiko.SSHClient()
    client.load_host_keys(
        os.path.expanduser("~/.ssh/known_hosts")
    )
    client.set_missing_host_key_policy(
        paramiko.RejectPolicy()
    )

    try:
        client.connect(
            hostname="127.0.0.1",
            port=2222,
            username="will",
            key_filename=key_path,
            passphrase=passphrase,
            look_for_keys=False,
            allow_agent=False,
            timeout=10,
        )

        yield client

    finally:
        client.close()


def test_hostname(ssh_client):
    """TC001: Validate server hostname."""

    stdin, stdout, stderr = ssh_client.exec_command(
        "hostname",
        timeout=10,
    )

    exit_code = stdout.channel.recv_exit_status()
    output = stdout.read().decode("utf-8").strip()
    error = stderr.read().decode("utf-8").strip()

    assert exit_code == 0, error
    assert output == "serverlab-ubuntu"
