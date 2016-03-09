# cos-ansible-base

- Issue/Task tracking: https://huboard.com/CenterForOpenScience/cos-ansible-base

## Requirements

- ansible >= 1.6
- virtualbox
- vagrant >= 1.6
- invoke (Python task execution library)
- python >= 2.7 or >= 3.4 with pip
- fwknop >= 2.6.5
- At least 2Gb of memory

### Installing Ansible and Vagrant on Mac OSX with homebrew

Virtualbox and Vagrant can be installed with homebrew cask. If you have homebrew installed, run the following from the project directory:

```sh
$ brew bundle
```

### Installing python requirements

Invoke can be installed with pip

```sh
$ pip install invoke
$ pip install -r requirements.txt
```


## Getting cos-ansible-base

To clone cos-ansible-base locally, run:

```sh
$ git clone https://github.com/CenterForOpenScience/cos-ansible-base --recursive
```

The ``--recursive`` option ensures that all submodules will be cloned.

## Vagrant setup

Once you have Vagrant and ansible installed, follow these steps:

- Generate your ssh key with `ssh-keygen`

```bash
$ ssh-keygen
```

- Run `vagrant up <machine_to_run>`. Then will start the VM provision with `invoke vprovision`. Use the `--limit` (or `-l`) option to limit to a specific group.

```bash
# Start the osf-staging server
$ vagrant up osf-staging
# Provision the osf-staging server
$ invoke vprovision --limit osf-staging
```


### SSH

To ssh into your Vagrant box, run ``vagrant ssh <box-name>``:

```bash
$ vagrant ssh osf-staging
```

## Generating passwords

To generate a password, run

```bash
$ invoke genpass
```

This crypted password can be used by the generic-users role in a group_vars file.

## Running playbooks

Playbooks can be run with the `ansible-playbook` command. You need to specify which inventory file with the `-i` option as well as a user with the `-u` option. Run in sudo mode with `-s`

```bash
$ ansible-playbook security.yml -i vagranthosts -u sloria -s
```

Or, using invoke for shorthand:

```bash
$ invoke play security.yml -i vagranthosts -u sloria
```

## Provisioning

The `site.yml` playbook is responsible for provisioning all servers in an inventory.

Run it like so:

```bash
$ ansible-playbook site.yml -i vagranthosts -u sloria -s
```

The above command runs the `site.yml` playbook using the `vagrant` inventory file with user `sloria` in sudo mode.

Or, if you prefer to use invoke:

```bash
$ invoke provision -i vagranthosts -u sloria
```

NOTE: You can also provision the vagrant box by running `invoke vprovision` with no arguments.

Many of the roles use variables defined in their `defaults/main.yml` file. You can override these on the command line with the `-e` option:

```bash
$ ansible-playbook site.yml -i vagranthosts -u sloria -e "ssh_test=false"
```

or, equivalently:

```bash
$ invoke provision -u sloria -e "ssh_test=false"
```

The above would temporarily disable SSH configuration testing.



## Setting up for Single Packet Authorization

If using encryption and HMAC keys, execute on client: 

```bash 
fwknop -A tcp/22 -a PUBLIC_CLIENT_IP -D TARGET_SERVER_IP --key-gen --use-hmac --save-rc-stanza
 ```

Print your newly generated keys:

 ```bash
 grep KEY ~/.fwknoprc
 ```
And add to Single Packet Authorization Server access configuration /etc/fwknop/access.conf:
 
 ```
 SOURCE              ANY
 KEY_BASE64          [KEY]
 HMAC_KEY_BASE64     [HMAC_KEY]
 ```
 

## Setting up for OSF deployment

You will need to set up agent forwarding in order to be able to properly authenticate with Github over SSH in ansible. To do so, add the following to your `~/.ssh/config/` file.


```
Host staging.osf.io
    HostName 66.228.46.171
    User sloria
    ForwardAgent yes

Host osf.io
    HostName 69.164.210.152
    User sloria
    ForwardAgent yes
```

## Deployment

The `deploy.yml` script is used to deploy the OSF.

To deploy on staging:

```bash
$ invoke deploy_staging -u sloria
```

You will be prompted for the branch to checkout on staging.


To deploy to production:

```bash
$ invoke deploy_production -u sloria
```

This will deploy to the production server, checking out the master
branch from Github.

### COS is Hiring!

Want to help save science? Want to get paid to develop free, open source software? [Check out our openings!](http://cos.io/jobs)
