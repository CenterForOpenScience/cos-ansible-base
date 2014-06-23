# cos-ansible-base

- Issue/Task tracking: https://huboard.com/CenterForOpenScience/cos-ansible-base

## Requirements 

- ansible >= 1.6
- virtualbox
- vagrant >= 1.5
- invoke (Python task execution library)

### Installing Ansible and Vagrant on Mac OSX with homebrew

Virtualbox and Vagrant can be installed with homebrew cask. If you have homebrew installed, run the following in the project directory

```sh
$ brew bundle
```

### Installing python requirements

Invoke can be installed with pip

```sh
$ pip install invoke
$ pip install -r requirements.txt
```

## Vagrant setup

Once you have Vagrant and ansible installed, follow these steps:

- Generate your ssh key with `ssh-keygen`

```bash
$ ssh-keygen
```

- Modify `group_vars/vagrantbox` as needed.



- Run `$ vagrant up`. This will start the VM provision it with the `vagrant.yml` playbook.

```bash
$ vagrant up
```

### SSH

To ssh into your Vagrant box, you can run (must have invoke installed):

```bash
$ invoke vssh -u yourusername
```

## Running playbooks

Playbooks can be run with the `ansible-playbook` command. You need to specify which inventory file with the `-i` option as well as a user with the `-u` option. Run in sudo mode with `-s`

```bash
$ ansible-playbook security.yml -i vagrant -u sloria -s
```

Or, using invoke for shorthand:

```bash
$ invoke play security.yml -i vagrant -u sloria
```

## Provisioning 

The `site.yml` playbook is responsible for provisioning all servers in an inventory.

Run it like so:

```bash
$ ansible-playbook site.yml -i vagrant -u sloria -s
```

The above command runs the `site.yml` playbook using the `vagrant` inventory file with user `sloria1` in sudo mode.

Or, if you prefer to use invoke:

```bash
$ invoke provision -i vagrant -u sloria
```

NOTE: You can also provision the vagrant box by running `invoke provision` with no arguments.

Many of the roles have variables use variables defined in their `defaults/main.yml` file. You can override these on the command line with the `-e` option:

```bash
$ ansible-playbook site.yml -i vagrant -u sloria -e "ssh_test=false"
```

or, equivalently:

```bash
$ invoke provision -u sloria -e "ssh_test=false"
```

The above would temporarily disable SSH configuration testing.




