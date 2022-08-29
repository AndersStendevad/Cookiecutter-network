""" tests for cookiecutter """

import pytest
import requests
import socket

from subprocess import run, Popen, CompletedProcess
from time import sleep

def test_bake_project(bake):
    """check if cookiecutter will even bake"""
    pass


def test_pytest_in_baked_project(bake, helper):
    """check pytest in baked project"""
    helper.install_package(".")
    helper.check_result(run("tox -e pytest", shell=True, capture_output=True))


def test_pre_commit_in_baked_project(bake, helper):
    """check pre-commit in baked project"""
    helper.check_result(
        run("pre-commit run --all-files", shell=True, capture_output=True)
    )


def test_docs(bake, helper):
    """check if docs are generated"""
    helper.check_result(run("tox -e docs", shell=True, capture_output=True))


def test_lint(bake, helper):
    """check lint in baked project"""
    helper.check_result(run("tox -e lint", shell=True, capture_output=True))

@pytest.mark.skip(reason="Too slow")
def test_lab(bake, helper):
    """check lab in baked project"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if not s.connect_ex(('localhost', 8888)):
            raise Exception("8888 port is in use!")
    sleep(0.5)
    p = Popen(["tox", "-e lab"])
    sleep(45)
    requests.get("http://0.0.0.0:8888")
    p.terminate()
