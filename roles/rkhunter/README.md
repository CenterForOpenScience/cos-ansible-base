# Ansible role: rkhunter

Ansible role for installing and using rkhunter.

Adapted from this blog post: https://www.digitalocean.com/community/articles/how-to-use-rkhunter-to-guard-against-rootkits-on-an-ubuntu-vps

## Variables

To receive emails when rkhunter detects a potential threat, change the `rkhunter_mail_on_warnings` variable.

```yaml
rkhunter_mail_on_warnings: ""
```

All other variables are documented in `rkhunter/defaults/main.yml`
