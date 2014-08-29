from fabric.api import cd, env, local, put, sudo, run, task
from fabric.context_managers import hide, settings as fab_settings
from fabric.colors import green
import tempfile

env.use_ssh_config = True


@task
def deploy():
    # Compress the build
    tgz = tempfile.NamedTemporaryFile(suffix=".tar.gz")
    local("git archive --prefix=geo/ HEAD -o '%s'" % tgz.name)
    env.tgz_name = tgz.name

    print green("Starting deployment")

    # Put the build onto the server
    print green("Pushing the build")
    put(env.tgz_name, 'build.tar.gz')
    run("rm -rf geo")
    run("tar -zxf build.tar.gz")
    run("rm build.tar.gz")

    # Copy over settings that we don't want checked into the source.
    print green("Copying settings")
    put("geo/settings/deployment.py", "geo/geo/settings/local.py")

    with cd('geo'):
        # Make sure puppet is installed, and run it
        print green("Provisioning")
        sudo("apt-get -y install puppet")
        sudo("puppet apply puppet/manifest.pp --modulepath=puppet/modules/ "
             "--hiera_config puppet/hiera.yaml")

        # Build python dependency libraries
        print green("Building virtualenv")
        run("sh reset_environment.sh", quiet=True)

    # Bounce or start the supervisor processes
    print green("Restarting supervisor")
    with fab_settings(hide('running'), warn_only=True):
        running = run("ps aux | grep [s]upervisord")
    if running:
        sudo("killall -1 supervisord")
    else:
        sudo("supervisord -c /etc/supervisord.conf")

    print green("Finished deployment")


@task
def clear_cache():
    with cd("geo"):
        run('virtualenv/bin/python -c "from geo.cache import clear; clear()"')


@task
def get_api_key(name):
    with cd("geo"):
        run('virtualenv/bin/python -c '
            '"from geo import signer; print signer.sign(\\\\"%s\\\\")"' % name)
