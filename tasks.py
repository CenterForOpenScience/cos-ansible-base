from invoke import run, task

cmd = 'ansible-playbook {playbook} --extra-vars "host={host} user={user}" -i {hosts} {more}'

@task
def users():
    run(cmd.format(
        playbook='add_users.yml',
        host='vagrant1',
        user='vagrant',
        hosts='vagrant_hosts',
        more='--ask-pass'
    ))

@task
def vagrant():
    run(cmd.format(
        playbook='test.yml',
        host='vagrant1',
        user='jspies',
        hosts='vagrant_hosts',
        more=''
    ))

@task
def check():
    run(cmd.format(
        playbook='security_check.yml',
        host='vagrant1',
        user='jspies',
        hosts='vagrant_hosts',
        more='--ask-sudo-pass'
    ))

@task
def secure():
    run(cmd.format(
        playbook='secure_ubuntu.yml',
        host='vagrant1',
        user='jspies',
        hosts='vagrant_hosts',
        more='--ask-sudo-pass'
    ))