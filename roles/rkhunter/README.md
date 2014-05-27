# Ansible role: rkhunter

Ansible role for installing and using rkhunter.

**IMPORTANT**: rkhunter references known-good values and system states, so it is best to install and configure this after most software on the system has been isntalled.

Adapted from this blog post: https://www.digitalocean.com/community/articles/how-to-use-rkhunter-to-guard-against-rootkits-on-an-ubuntu-vps

## Usage


```yaml
- name: Set up security software
  hosts: all
  roles:
    # ...
    - role: rkhunter
    # ...
```

## Variables

The `rkhunter_propupd` variable controls whether or not rkhunter will update its database of baseline file properties. 

```yaml
rkhunter_propupd: yes
```

**IMPORTANT**: `rkhunter_propupd` should only be set to `yes` when the current config files are known to be good.

To receive emails when rkhunter detects a potential threat, change the `rkhunter_mail_on_warnings` variable.

```yaml
rkhunter_mail_on_warnings: ""
```

All other variables are documented in `rkhunter/defaults/main.yml`.


## Updating baseline file properties

When software changes are made on the target machine, rkhunter may report differences in its next run. To update rkhunter to the new file properties, run the following ad-hoc ansible command.

```
ansible GROUPNAME -i INVENTORY_FILE -a "rkhunter --propupd" --sudo --ask-sudo-pass
```
