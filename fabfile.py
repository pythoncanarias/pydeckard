from fabric.api import env, local, prefix, cd, run

env.hosts = ["production"]


def deploy():
    local("git push")
    with prefix("source ~/.virtualenvs/pydeckard/bin/activate"):
        with cd("~/pydeckard"):
            run("git pull")
            run("pip install -r requirements.txt")
            run("supctl restart pydeckard")
