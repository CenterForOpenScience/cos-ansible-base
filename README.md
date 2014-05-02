cos-ansible-base
================


## Vagrant

Once you have Vagrant and ansible installed, follow these steps:

1. Generate your ssh key with `ssh-keygen`

```bash
$ ssh-keygen
...
```

2. Copy `group_vars/testbox.example` to `group_vars/testbox`

```bash
$ cp group_vars/testbox.example group_vars/testbox
```


3. Modify the `key` variable in the `keys` dictionary of `group_vars/testbox`. You can either paste in your key as a string, or use a file, like so:

```yaml
# in group_vars/testbox
# ...

# add your key here
keys:
    - user: vagrant
      key: "{{ lookup('file', '/Users/your-username/.ssh/id_rsa.pub') }}"
```

3. Run `$ vagrant up`. This will start the VM provision it with the `vagrant.yml` playbook.

```bash
$ vagrant up
```
