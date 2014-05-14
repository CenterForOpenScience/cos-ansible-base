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
def provision(inventory='vagrant', user='vagrant', sudo=True, verbose=False, extra=''):
    """Run the site.yml playbook given an inventory file and a user. Defaults
    to provisioning the vagrant box.
    """
    play(playbook='site.yml',
        inventory=inventory,
        user=user,
        sudo=sudo,
        verbose=verbose, extra=extra)

@task
def play(playbook, inventory='vagrant', user='vagrant', sudo=True, verbose=False, extra=''):
    """Run a playbook. Defaults to using the vagrant inventory and vagrant user."""
    cmd = 'ansible-playbook {playbook} -i {inventory} -u {user}'.format(**locals())
    if sudo:
        cmd += ' -s'
    if verbose:
        cmd += ' -vvvv'
    if extra:
        cmd += ' -e {0}'.format(extra)
    run(cmd, pty=True)


@task
def vssh(user='vagrant'):
    run('ssh -p 2222 {0}@localhost'.format(user), pty=True)
