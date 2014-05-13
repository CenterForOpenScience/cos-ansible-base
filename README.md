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

- Copy `group_vars/testbox.example` to `group_vars/testbox`

```bash
$ cp group_vars/testbox.example group_vars/testbox
```

- Modify `group_vars/testbox` with your user and key info where you see "CHANGEME". You can either paste in your key as a string, or use a file, like so:

Example: 

```yaml
# in group_vars/testbox
# ...

user: 
  # ....
  - name: sloria
    passwd: owijoai2123
    comment: secret
    uid: 2000
    shell: /bin/bash
    groups:
    - adm
    - sudo
    - admin
    - staff
    append: yes

# add your key here
keys:
    - user: vagrant
      key: "{{ lookup('file', '/Users/sloria/.ssh/id_vagrant.pub') }}"
    - user: sloria
      key: "{{ lookup('file', '/Users/sloria/.ssh/id_rsa.pub') }}"

# You should also enter CSF settings in this file
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



