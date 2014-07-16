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
def play(playbook, user, inventory=SITE_INVENTORY, sudo=True, ask_sudo_pass=True,
         verbose=False, extra='', key=None, limit=None):
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
    if limit:
        cmd += ' --limit={0}'.format(limit)
    if key:
        cmd += ' --private-key={0}'.format(key)
    if extra:
        cmd += ' -e {0!r}'.format(extra)
    run(cmd, echo=True, pty=True)


@task
def deploy(user, inventory=SITE_INVENTORY, verbose=False, extra='', limit=None,
           key=None):
    play(user=user,
         playbook='deploy.yml',
         inventory=inventory,
         verbose=verbose,
         limit=limit,
         key=key,
         extra=extra
    )


@task
def deploy_staging(user, inventory=SITE_INVENTORY, verbose=False, extra='', key=None):
    """Executes deploy.yml, limiting only to staging servers."""
    deploy(user=user, limit='osf-staging', inventory=inventory, verbose=verbose, extra=extra, key=key)


@task
def deploy_production(user, inventory=SITE_INVENTORY, verbose=False, extra='', key=None):
    """Executes deploy.yml, limiting only to production servers."""
    deploy(user=user, limit='osf-production', inventory=inventory, verbose=verbose, extra=extra, key=key)


@task
def provision(user, inventory=SITE_INVENTORY, sudo=True, ask_sudo_pass=True,
              verbose=False, extra='', key=None, limit=None):
    """Run the provision.yml playbook given an inventory file and a user. Defaults
    to provisioning the vagrant box.
    """
    play(playbook='provision.yml',
         inventory=inventory,
         user=user,
         sudo=sudo,
         ask_sudo_pass=ask_sudo_pass,
         verbose=verbose, extra=extra,
         key=key,
         limit=limit)


@task
def vplay(playbook, user='vagrant', sudo=True, ask_sudo_pass=False,
          verbose=False, extra='', key='~/.vagrant.d/insecure_private_key', limit=None):
    """Run a playbook against the vagrant hosts."""
    play(playbook,
         inventory='vagranthosts',
         user=user,
         sudo=sudo,
         verbose=verbose,
         extra=extra,
         ask_sudo_pass=ask_sudo_pass,
         key=key,
         limit=limit)

@task
def vprovision(user='vagrant', sudo=True, ask_sudo_pass=False,
        verbose=False, extra='', key='~/.vagrant.d/insecure_private_key', limit=None):
    """Provision the vagrant box using the provision.yml playbook."""
    provision(user=user,
        inventory=VAGRANT_INVENTORY,
        sudo=sudo,
        ask_sudo_pass=ask_sudo_pass,
        verbose=verbose,
        extra=extra,
        key=key,
        limit=limit
    )


@task
def vdeploy(user='vagrant', verbose=False, extra='', limit=None,
            key='~/.vagrant.d/insecure_private_key'):
    deploy(
        user=user,
        inventory=VAGRANT_INVENTORY,
        verbose=verbose,
        limit=limit,
        key=key,
        extra=extra
    )


@task
def vssh(user='vagrant', host='192.168.111.222'):
    # Use subprocess to ssh so that terminal will display correctly
    subprocess.call('ssh {0}@{1}'.format(user, host), shell=True)


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
