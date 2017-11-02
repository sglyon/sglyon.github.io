from invoke import run, task

@task
def dev(ctx):
    run("hugo server")

@task
def publish(ctx):
    run("hugo")
    run("ghp-import -n -p public -b master")
