from invoke import run, task

cmd = 'ansible-playbook playbooks/{playbook} --extra-vars "host={host} user={user}" -i {hosts} {more}'

@task
def users():
    run(cmd.format(
        playbook='add_users.yml',
        host='vagrant1',
        user='vagrant',
        hosts='hosts_vagrant',
        more='--ask-pass'
    ))

@task
def vagrant(up=False):
    if up:
        run('vagrant up')
    run('ansible-playbook vagrant.yml -i vagrant -s', pty=True)

@task
def check():
    run(cmd.format(
        playbook='security_check.yml',
        host='vagrant1',
        user='jspies',
        hosts='hosts_vagrant',
        more='--ask-sudo-pass'
    ))

@task
def vssh(user='vagrant'):
    run('ssh -p 2222 {0}@localhost'.format(user), pty=True)

@task
def secure():
    run(cmd.format(
        playbook='secure_ubuntu.yml',
        host='vagrant1',
        user='jspies',
        hosts='hosts_vagrant',
        more='--ask-sudo-pass'
    ))
