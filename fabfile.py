__author__ = 'igor'


from fabric.api import local, prefix, run, cd, settings
import os
from clavutich.settings import BASE_DIR, PROJECT_NAME
from fabric.state import env
from clavutich.local_settings import HOSTS
env.user = 'root'
env.skip_bad_hosts = True
env.warn_only = False
env.parallel = True
env.shell = "/bin/bash -l -i -c"
REQUIREMENTS_FILE = 'requirements.txt'


def deploy():
    """
    deploy project on remote server
    :return:
    """
    local_act()
    update_requirements()
    remote_act()


def remote_act():
    """
    run remote acts
    :return: None
    """
    for host, dir_name in HOSTS:
        with settings(host_string=host):
            with cd(dir_name):
                run("git reset --hard")
                run("kill -9 $(ps -ef|grep -v grep |grep '%s' | awk '{print $2}')" % PROJECT_NAME)
                run("%s" % PROJECT_NAME)
                run("./manage.py loaddata db.json")


def local_act():
    """
    prepare deploy
    :return: None
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % PROJECT_NAME)
    activate_env = os.path.expanduser(os.path.join(BASE_DIR, ".env/bin/activate_this.py"))
    execfile(activate_env, dict(__file__=activate_env))
    # local("./manage.py test")
    local("./manage.py makemigrations")
    local("./manage.py migrate")
    local('pip freeze ' + REQUIREMENTS_FILE)
    # local("%s && %s%s" % ('source .env/bin/activate', 'pip freeze > ', REQUIREMENTS_FILE))
    local("./manage.py collectstatic --noinput")
    local("git add .")
    local("git commit -a -F git_commit_message")
    current_branch = local("git symbolic-ref --short -q HEAD", capture=True)

    if current_branch != 'master':
        local("git checkout master")
        local("git merge %s" % current_branch)
        local("git branch -d %s" % current_branch)

    local("git push bit")
    local("git push production")


def update_requirements():
    """
    install external requirements on remote host
    :return: None
    """
    for host, dir_name in HOSTS:
        with settings(host_string=host):
            run('apt-get install libjpeg-dev')

            with cd(dir_name):
                with prefix('source .env/bin/activate'):
                    run('pip install -r %s' % REQUIREMENTS_FILE)


