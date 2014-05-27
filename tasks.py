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
def provision(inventory='vagranthosts', user='vagrant', sudo=True, verbose=False, extra=''):
    """Run the site.yml playbook given an inventory file and a user. Defaults
    to provisioning the vagrant box.
    """
    play(playbook='site.yml',
        inventory=inventory,
        user=user,
        sudo=sudo,
        verbose=verbose, extra=extra)

@task
def play(playbook, inventory='vagranthosts', user='vagrant', sudo=True, verbose=False, extra=''):
    """Run a playbook. Defaults to using the vagrant inventory and vagrant user."""
    print('[invoke] Playing {0!r} on {1!r} with user {2!r}...'.format(playbook, inventory, user))
    cmd = 'ansible-playbook {playbook} -i {inventory} -u {user}'.format(**locals())
    if sudo:
        cmd += ' -s'
    if verbose:
        cmd += ' -vvvv'
    if extra:
        cmd += ' -e {0!r}'.format(extra)
    print('[invoke] {0!r}'.format(cmd))
    run(cmd, pty=True)


@task
def vssh(user='vagrant'):
    run('ssh -p 2222 {0}@localhost'.format(user), pty=True)


@task
def rkhunter_propupd(group='vagrantbox', inventory='vagranthosts', user='vagrant'):
    """Update rkhunter's baseline file configuration database."""
    cmd = ('ansible {group} -i {inventory} -a '
        '"rkhunter --propupd" --sudo --ask-sudo-pass').format(
        group=group, inventory=inventory
        )
    print('[invoke] {0!r}'.format(cmd))
    run(cmd)
