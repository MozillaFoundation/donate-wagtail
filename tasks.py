from sys import platform
import re

from invoke import task

# Workaround for homebrew installation of Python (https://bugs.python.org/issue22490)
import os
os.environ.pop('__PYVENV_LAUNCHER__', None)

ROOT = os.path.dirname(os.path.realpath(__file__))

# Python commands's outputs are not rendering properly. Setting pty for *Nix system and
# "PYTHONUNBUFFERED" env var for Windows at True.
if platform == 'win32':
    PLATFORM_ARG = dict(env={'PYTHONUNBUFFERED': 'True'})
else:
    PLATFORM_ARG = dict(pty=True)


def create_docker_env_file(env_file):
    """Create or update an .env to work with a docker environment"""
    with open(env_file, 'r') as f:
        env_vars = f.read()
    # update the DATABASE_URL env
    new_db_url = "DATABASE_URL=postgres://donate:mozilla@postgres:5432/donate"
    old_db_url = re.search('DATABASE_URL=.*', env_vars)
    env_vars = env_vars.replace(old_db_url.group(0), new_db_url)
    # update the ALLOWED_HOSTS env
    new_hosts = "ALLOWED_HOSTS=*"
    old_hosts = re.search('ALLOWED_HOSTS=.*', env_vars)
    env_vars = env_vars.replace(old_hosts.group(0), new_hosts)
    # Update REDIS_URL env
    new_redis_url = "REDIS_URL=redis://redis:6379/0"
    old_redis_url = re.search('REDIS_URL=.*', env_vars)
    env_vars = env_vars.replace(old_redis_url.group(0), new_redis_url)

    # create the new env file
    with open('.env', 'w') as f:
        f.write(env_vars)


def docker_create_super_user(ctx):
    # Windows doesn't support pty, skipping this step
    if platform == 'win32':
        print("\nPTY is not supported on Windows.\n"
              "To create an admin user:\n"
              "docker-compose run --rm backend pipenv run python manage.py createsuperuser\n")
    else:
        print("* Creating superuser.")
        ctx.run(
            "docker-compose run --rm backend pipenv run python manage.py createsuperuser",
            pty=True
        )


@task
def docker_manage(ctx, command):
    """Shorthand to manage.py. inv docker-manage \"[COMMAND] [ARG]\""""
    with ctx.cd(ROOT):
        ctx.run(f"docker-compose run --rm backend pipenv run python manage.py {command}", **PLATFORM_ARG)


@task
def docker_pipenv(ctx, command):
    """Shorthand to pipenv. inv docker-pipenv \"[COMMAND] [ARG]\""""
    with ctx.cd(ROOT):
        ctx.run(f"docker-compose run --rm backend pipenv {command}")


@task
def docker_npm(ctx, command):
    """Shorthand to npm. inv docker-npm \"[COMMAND] [ARG]\""""
    with ctx.cd(ROOT):
        ctx.run(f"docker-compose run --rm watch-static-files npm {command}")


@task
def docker_migrate(ctx):
    """Updates database schema"""
    docker_manage(ctx, "migrate --no-input")


@task
def docker_makemigrations(ctx):
    """Creates new migration(s) for apps"""
    docker_manage(ctx, "makemigrations")


@task
def docker_makemessages(ctx):
    """Extract all template messages in .po files for localization"""
    ctx.run("./translation-management.sh import")
    docker_manage(ctx, "makemessages --keep-pot --no-wrap")
    docker_manage(ctx, "makemessages -d djangojs --keep-pot --no-wrap --ignore=node_modules")
    os.replace("donate/locale/django.pot", "donate/locale/templates/LC_MESSAGES/django.pot")
    os.replace("donate/locale/djangojs.pot", "donate/locale/templates/LC_MESSAGES/djangojs.pot")
    ctx.run("./translation-management.sh export")


@task
def docker_compilemessages(ctx):
    """Compile the latest translations"""
    docker_manage(ctx, "compilemessages")


@task
def docker_test_python(ctx):
    """Run python tests"""
    print("* Running flake8")
    ctx.run("docker-compose run --rm backend pipenv run flake8 tasks.py donate/", **PLATFORM_ARG)
    print("* Running tests")
    docker_manage(ctx, "test --settings=donate.settings --configuration=Testing")


@task
def docker_test_node(ctx):
    """Run node tests"""
    print("* Running tests")
    ctx.run("docker-compose run --rm watch-static-files npm run test", **PLATFORM_ARG)


@task
def docker_new_db(ctx):
    """Delete your database and create a new one with fake data"""
    print("* Stopping services first")
    ctx.run("docker-compose down")
    print("* Deleting database")
    ctx.run("docker volume rm donate-wagtail_postgres_data")
    print("* Applying database migrations.")
    docker_migrate(ctx)
    print("* Creating fake data")
    docker_manage(ctx, "load_fake_data")
    docker_create_super_user(ctx)


@task(aliases=["docker-catchup"])
def docker_catch_up(ctx):
    """Rebuild images and apply migrations"""
    print("* Stopping services first")
    ctx.run("docker-compose down")
    print("* Rebuilding images and install dependencies")
    ctx.run("docker-compose build")
    print("* Applying database migrations.")
    docker_migrate(ctx)


@task
def docker_new_env(ctx):
    """Get a new dev environment and a new database with fake data"""
    with ctx.cd(ROOT):
        print("* Setting default environment variables")
        if os.path.isfile(".env"):
            print("* Updating your .env")
            create_docker_env_file(".env")
        else:
            print("* Creating a new .env")
            create_docker_env_file("env.default")
        print("* Stopping project's containers and delete volumes if necessary")
        ctx.run("docker-compose down --volumes")
        print("* Building Docker images")
        ctx.run("docker-compose build --no-cache backend watch-static-files", **PLATFORM_ARG)
        ctx.run("docker-compose build backend-worker", **PLATFORM_ARG)
        print("* Applying database migrations.")
        docker_migrate(ctx)
        print("* Creating fake data")
        docker_manage(ctx, "load_fake_data")
        docker_create_super_user(ctx)

        print("\n* Start your dev server with:\n docker-compose up")
