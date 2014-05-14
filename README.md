# cos-ansible-base

## Requirements 

- ansible >= 1.6
- vagrant >= 1.5
- invoke (Python task execution library)

## Vagrant setup

Once you have Vagrant and ansible installed, follow these steps:

- Generate your ssh key with `ssh-keygen`

```bash
$ ssh-keygen
...
```

- Copy `group_vars/vagrantbox.example` to `group_vars/vagrantbox`

```bash
$ cp group_vars/vagrantbox.example group_vars/vagrantbox
```

- Modify `group_vars/vagrantbox` with your user and key info where you see "CHANGEME". You can either paste in your key as a string, or use a file, like so:

Example: 

```yaml
# in group_vars/vagrantbox
# ...

# --- users and groups

genericusers_groups:
    - name: "admin"
    - name: "vagrant"

genericusers_users:
  - name: "vagrant"
    pass: "satrF5fwANvrQ"
    comment: 'vagrant'
    uid: 1000
    shell: /bin/bash
    groups: ["vagrant", "admin"]
    append: no
    ssh_keys:
      - "{{ lookup('file', '/Users/sloria1/.ssh/id_rsa.pub') }}"
  - name: "sloria1"
    pass: "satrF5fwANvrQ"
    comment: "vagrant"
    uid: 2000
    shell: /bin/bash
    groups: ["vagrant", "admin"]
    append: yes
    # Set your key here
    # You can use a file like so:
    # "{{ lookup('file', '/Users/you/.ssh/id_rsa.pub') }}"
    ssh_keys:
      - "{{ lookup('file', '/Users/sloria1/.ssh/id_rsa.pub') }}"

# --- csf
csf_allowed_ips:
    - CHANGEME
csf_ui_user: FILLIN
csf_ui_password: FILLIN

```

- Run `$ vagrant up`. This will start the VM provision it with the `vagrant.yml` playbook.

```bash
$ vagrant up
```

### SSH

To ssh into your Vagrant box, you can run (must have invoke installed):

```bash
$ invoke vssh -u yourusername
```


### Installing roles

Ansible-galaxy roles should be enumerated in roles.txt and installed to the roles directory. To reinstall all roles, run

```bash
$ ansible-galaxy install -r roles.txt -p ./roles -f
```

Or, for short:

```bash
$ invoke install_roles -f
```


## Provisioning 

The `site.yml` playbook is responsible for provisioning all servers in an inventory.

Run it like so:

```bash
$ ansible-playbook site.yml -i vagrant -u sloria1 -s
```

The above command runs the `site.yml` playbook using the `vagrant` inventory file with user `sloria1` in sudo mode.

Or, if you prefer to use invoke:

```bash
$ invoke provision -i vagrant -u sloria1
```

NOTE: You can also just run `invoke provision` with no arguments to provision the vagrant box.

Many of the roles have variables use variables defined in their `defaults/main.yml` file. You can override these on the command line with the `-e` option:

```bash
$ ansible-playbook site.yml -i vagrant -u sloria1 -e "ssh_test=false"
```

The above would temporarily disable SSH configuration testing.




