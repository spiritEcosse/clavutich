__author__ = 'igor'


from fabric.api import local, prefix, run, cd, settings, put
import os
from clavutich.settings import BASE_DIR, PROJECT_NAME
from fabric.state import env
from clavutich.settings_local import MY_SERVER, PRODUCTION_SERVER
env.user = 'root'
# 'clavutic@46.105.135.208',
env.hosts = ['78.24.216.187']
env.skip_bad_hosts = True
env.warn_only = False
env.parallel = False
env.shell = "/bin/bash -l -i -c"
REQUIREMENTS_FILE = 'requirements.txt'
media = 'media/'


def deploy():
    """
    deploy project on remote server
    :return:
    """
    local_act()
    remote_act()


def remote_act():
    """
    run remote acts
    :return: None
    """
    run("apt-get install libmemcached-dev")
    run("git reset --hard")

    project_dir = run("path_project_clavutich")

    with cd(project_dir.split()[0]):
        with prefix('env_activate_clavutich'):
            run('pip install -r %s' % REQUIREMENTS_FILE)
            run("./manage.py migrate")
            # run("./manage.py flush --noinput")
            # run("./manage.py loaddata db.json")
            # run("./manage.py clear_cache")
            run("reload_project_clavutich")


def local_act():
    """
    prepare deploy
    :return: None
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % PROJECT_NAME)
    activate_env = os.path.expanduser(os.path.join(BASE_DIR, ".env/bin/activate_this.py"))
    execfile(activate_env, dict(__file__=activate_env))

    # local("find %s -type d -exec sh -c ' ls \"$0\"/*.jpeg 2>/dev/null && jpegoptim --strip-all -v -t \"$0\"/*.jpeg ' {} \;" % BASE_DIR)
    # local("find %s -type d -exec sh -c ' ls \"$0\"/*.jpg 2>/dev/null && jpegoptim --strip-all -v -t \"$0\"/*.jpg ' {} \;" % BASE_DIR)
    # local("find %s -type d -exec sh -c ' ls \"$0\"/*.png 2>/dev/null && optipng -o5 \"$0\"/*.png ' {} \;" % BASE_DIR)
    # local("find %s -type d -exec sh -c ' ls \"$0\"/*.png 2>/dev/null && optipng -o5 \"$0\"/*.png ' {} \;" % os.path.join(BASE_DIR, "static/src/images/"))

    # project_dir = run("path_project_clavutich")

    # with cd(project_dir.split()[0]):
    #     put(os.path.join(BASE_DIR, media), '.')

    local("./manage.py test")
    local("grunt default")
    local("./manage.py makemigrations")
    local("./manage.py migrate")
    # local("./manage.py dumpdata --indent 4 --natural-primary --natural-foreign -e contenttypes -e auth.Permission -e sessions -e admin > db.json")
    local('pip freeze > ' + REQUIREMENTS_FILE)
    local("./manage.py collectstatic --noinput -c")
    local("git add .")
    status = local("git status -s", capture=True)

    if status:
        local("git commit -a -F git_commit_message")
        current_branch = local("git symbolic-ref --short -q HEAD", capture=True)

        if current_branch != 'master':
            local("git checkout master")
            local("git merge %s" % current_branch)
            local("git branch -d %s" % current_branch)

        local("git push bit")
        local("git push production")
        local("git push origin")

