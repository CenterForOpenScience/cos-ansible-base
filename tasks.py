#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getpass
import sys
import subprocess

from invoke import run, task

VAGRANT_INVENTORY = 'vagranthosts'
SITE_INVENTORY = 'hosts'

@task
def install_roles(force=False, ignore_errors=False):
    command = 'ansible-galaxy install -r roles.txt -p roles'
    if force:
        command += ' --force'
    if ignore_errors:
        command += ' --ignore-errors'
    run(command, pty=True)

@task
def provision(user, inventory=SITE_INVENTORY, sudo=True, ask_sudo_pass=True,
        verbose=False, extra=''):
    """Run the site.yml playbook given an inventory file and a user. Defaults
    to provisioning the vagrant box.
    """
    play(playbook='site.yml',
        inventory=inventory,
        user=user,
        sudo=sudo,
        ask_sudo_pass=ask_sudo_pass,
        verbose=verbose, extra=extra)

@task
def vprovision(user='vagrant', sudo=True, ask_sudo_pass=False,
        verbose=False, extra=''):
    """Provision the vagrant box using the site.yml playbook."""
    provision(user=user, inventory=VAGRANT_INVENTORY, sudo=sudo,
                ask_sudo_pass=ask_sudo_pass, verbose=verbose, extra=extra)

@task
def play(playbook, user, inventory=SITE_INVENTORY, sudo=True, ask_sudo_pass=True,
         verbose=False, extra=''):
    """Run a playbook. Defaults to using the "hosts" inventory"""
    print('[invoke] Playing {0!r} on {1!r} with user {2!r}...'.format(
        playbook, inventory, user)
    )
    cmd = 'ansible-playbook {playbook} -i {inventory} -u {user}'.format(**locals())
    if sudo:
        cmd += ' -s'
    if ask_sudo_pass:
        cmd += ' --ask-sudo-pass'
    if verbose:
        cmd += ' -vvvv'
    if extra:
        cmd += ' -e {0!r}'.format(extra)
    run(cmd, echo=True, pty=True)

@task
def vplay(playbook, user='vagrant', sudo=True, ask_sudo_pass=False,
        verbose=False, extra=''):
    """Run a playbook against the vagrant hosts."""
    play(playbook, inventory='vagranthosts', user=user,
        sudo=sudo, verbose=verbose, extra=extra, ask_sudo_pass=ask_sudo_pass)

@task
def vssh(user='vagrant'):
    # Use subprocess to ssh so that terminal will display correctly
    subprocess.call('ssh -p 2222 {0}@localhost'.format(user), shell=True)


@task
def rkhunter_propupd(group='vagrantbox', inventory='vagranthosts', user='vagrant'):
    """Update rkhunter's baseline file configuration database."""
    cmd = ('ansible {group} -i {inventory} -a '
        '"rkhunter --propupd" --sudo --ask-sudo-pass').format(
        group=group, inventory=inventory
        )
    run(cmd, echo=True)

@task
def genpass():
    from passlib.hash import sha256_crypt
    pw = getpass.getpass('Enter a password: ')
    pw2 = getpass.getpass('Enter password again: ')
    if pw != pw2:
        print("Passwords don't match.")
        sys.exit(1)
    print('')
    print(sha256_crypt.encrypt(pw))
