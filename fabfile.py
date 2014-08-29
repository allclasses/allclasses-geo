from fabric.api import cd, env, local, put, sudo, run, task, \
    settings as fab_settings
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
    run("rm -rf pipeline_monitor")
    run("tar -zxf build.tar.gz")
    run("rm build.tar.gz")

    # Copy over settings that we don't want checked into the source.
    print green("Copying settings")
    put("geo/settings/deployment.py", "geo/settings/local.py")

    with cd('geo'):
        # Make sure puppet is installed, and run it
        print green("Provisioning")
        sudo("apt-get install puppet")
        sudo(
            "puppet apply puppet/manifest.pp --modulepath=puppet/modules/ "
            "--hiera_config puppet/hiera.yaml",
            quiet=True  # Noisy scripts
        )

        # Build python dependency libraries
        print green("Building virtualenv")
        run("sh reset_environment.sh", quiet=True)

    # Bounce or start the supervisor processes
    print green("Restarting supervisor")
    with fab_settings(warn_only=True, hide="everything"):
        running = run("ps -aux | grep [s]upervisord")
    if running:
        sudo("killall -1 supervisord")
    else:
        sudo("supervisord -c /etc/supervisord.conf")

    print green("Finished deployment")
