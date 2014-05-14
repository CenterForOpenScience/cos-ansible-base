#!/usr/bin/env python
# -*- coding: utf-8 -*-
from invoke import run, task

@task
def install_roles(force=False, ignore_errors=False):
    command = 'ansible-galaxy install -r roles.txt -p roles'
    if force:
        command += ' --force'
    if ignore_errors:
        command += ' --ignore-errors'
    run(command, pty=True)

@task
def provision(inventory='vagrant', user='vagrant', sudo=True, verbose=False):
    """Run the site.yml playbook given an inventory file and a user. Defaults
    to provisioning the vagrant box.
    """
    cmd = 'ansible-playbook site.yml -i {inventory} -u {user}'.format(**locals())
    if sudo:
        cmd += ' -s'
    if verbose:
        cmd += ' -vvvv'
    run(cmd, pty=True)

@task
def vssh(user='vagrant'):
    run('ssh -p 2222 {0}@localhost'.format(user), pty=True)
