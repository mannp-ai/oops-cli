import pytest
from oops.matcher import Matcher
import os
import json

def test_matcher_git_conflict():
    matcher = Matcher()
    command = "git merge feature"
    stderr = "CONFLICT (content): Merge conflict in file.txt"
    match = matcher.match(command, stderr)
    assert match is not None
    assert match["id"] == "git-merge-conflict"

def test_matcher_docker_daemon():
    matcher = Matcher()
    command = "docker run hello-world"
    stderr = "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?"
    match = matcher.match(command, stderr)
    assert match is not None
    assert match["id"] == "docker-daemon-off"

def test_matcher_dns_failure():
    matcher = Matcher()
    command = "curl google.com"
    stderr = "curl: (6) Could not resolve host: google.com"
    match = matcher.match(command, stderr)
    assert match is not None
    assert match["id"] == "dns-failure"

def test_matcher_apt_lock():
    matcher = Matcher()
    command = "apt update"
    stderr = "E: Could not get lock /var/lib/dpkg/lock"
    match = matcher.match(command, stderr)
    assert match is not None
    assert match["id"] == "apt-lock"
    assert "Apt is currently locked" in match["what"]

def test_matcher_permission_denied_bias_fix():
    matcher = Matcher()
    command = "ssh user@host"
    stderr = "Permission denied (publickey)"
    match = matcher.match(command, stderr)
    assert match is not None
    # Should match ssh-pubkey-denied instead of permission-denied-sudo
    assert match["id"] == "ssh-pubkey-denied"
    assert "ssh-add" in match["fix"]
