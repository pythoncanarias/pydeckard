from fabric.api import env, local, cd, run

env.hosts = ["pythoncanarias.es"]


def deploy():
    local("git push")
    with cd("~/pydeckard"):
        run("git pull")
        run("pipenv install")
        run("supervisorctl restart pydeckard")
