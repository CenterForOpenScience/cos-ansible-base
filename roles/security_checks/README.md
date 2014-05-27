# Ansible role: security_checks

An ansible role for performing various vulnerability tests.


## CSF tests

CSF tests will be run in TESTING mode. TESTING mode will be disabled after the tests complete.

### Port scan tests

To enable port scan tests, define the following variables. In particular, the `check_portscan_hosts` variable should be a list of remote hosts to test.

```yaml
check_portscan: yes
# csf should hang connections if a portscan is detected; the port scan denial
# test will wait this number of seconds before declaring a port scan denied
check_portscan_timeout: 3
# Remote hosts to attempt a port scan
check_portscan_hosts:
    - 192.168.111.111
```

When CSF detects a port scan, it will hang the attacker's connection. The port scan denial test in this role will attempt to do a port scan, waiting `check_portscan_timeout` seconds to find an open port. If an open port is found, the task will fail.
