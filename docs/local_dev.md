# Local Dev Documentation

This documentation is composed of four main sections:
- [How to install and use Docker for local development](./local_dev.md#how-to-use)
- [Connecting Docker to your code editor](./local_dev.md#connecting-docker-to-your-code-editor)
- [Debugging](./local_dev.md#debugging)
- [Docker 101 and how we use it with the foundation site](./local_dev.md#docker-vocabulary-and-overview). Start here if you're new to Docker

## How to use

To interact with the project, you can use [docker](https://docs.docker.com/engine/reference/commandline/cli/) and [docker-compose](https://docs.docker.com/compose/reference/overview/) CLIs or use shortcuts with invoke.

The general workflow is:
- Install the project with `invoke new-env`,
- Run the project with `docker-compose up`,
- Log into the admin site with username `admin` and password `admin`,
- Use invoke commands for frequent development tasks (database migrations, dependencies install, run tests, etc),
- After doing a `git pull`, keep your clone up to date by running `invoke catchup`.

### Invoke tasks

Invoke is a python tasks runner that creates shortcuts for commands we frequently use. For example, instead of `docker-compose run --rm backend ./dockerpythonvenv/bin/python manage.py migrate`, you can use `inv docker-migrate`. It can also be used to run management commands: `inv docker-manage load-fake-data`. If you need to add multiple args to an invoke commands, use quotes. ex: `invoke docker-npm "install moment"`

Installation instructions: https://www.pyinvoke.org/installing.html

#### Invoke tasks available:

Run `inv -l` in your terminal to get the list of available tasks.

```
  catch-up (catchup, docker-catch-up, docker-catchup)   Rebuild images, install dependencies, and apply migrations
  compilemessages (docker-compilemessages)              Compile the latest translations
  makemessages (docker-makemessages)                    Extract all template messages in .po files for localization
  makemigrations (docker-makemigrations)                Creates new migration(s) for apps
  manage (docker-manage)                                Shorthand to manage.py. inv docker-manage "[COMMAND] [ARG]"
  migrate (docker-migrate)                              Updates database schema
  new-db (docker-new-db)                                Delete your database and create a new one with fake data
  new-env (docker-new-env, setup)                       Get a new dev environment and a new database with fake data
  npm (docker-npm)                                      Shorthand to npm. inv docker-npm "[COMMAND] [ARG]"
  npm-install (docker-npm-install)                      Install Node dependencies
  pip-compile (docker-pip-compile)                      Shorthand to pip-tools. inv pip-compile "[COMMAND] [ARG]"
  pip-compile-lock (docker-pip-compile-lock)            Lock prod and dev dependencies
  pip-sync (docker-pip-sync)                            Sync your python virtualenv
  test (docker-test)                                    Run both Node and Python tests
  test-node (docker-test-node)                          Run node tests
  test-python (docker-test-python)                      Run python tests
```

### Docker and docker-compose CLIs

We strongly recommend you to check at least the [docker-compose CLI](https://docs.docker.com/compose/reference/overview/) documentation since we're using it a lot. Meanwhile, here are the commands you will use the most:

**docker-compose:**
- [docker-compose up](https://docs.docker.com/compose/reference/up/): start the services and the project. Stop them with `^C`. If you want to rebuild your images, for example after a python dependencies update, add the `--build` flag. If you want to run the services in detached mode, use `--detached`. To get logs, use `docker-compose logs --follow [SERVICE]`,
- [docker-compose down](): stop and remove the services,
- [docker-compose run (--rm) [SERVICE NAME] [COMMAND]](https://docs.docker.com/compose/reference/run/): run a command against a service. `--rm` removes your container when you're done,
- [docker-compose build [SERVICE NAME]](https://docs.docker.com/compose/reference/build/): build a new image for the service. Use `--no-cache` to build the image from scratch again,
- [docker-compose ps](https://docs.docker.com/compose/reference/ps/): list the services running.

**docker:**
- [docker image](https://docs.docker.com/engine/reference/commandline/image/): interact with images,
- [docker container](https://docs.docker.com/engine/reference/commandline/container/): interact with containers,
- [docker volume](https://docs.docker.com/engine/reference/commandline/volume_create/): interact with volumes.
- [docker system prune](https://docs.docker.com/engine/reference/commandline/system_prune/): delete all unused container, image and network. Add `--volumes` to also remove volume. :rotating_light: It will impact other docker project running on your system! For a more subtle approach, [check this blog post](https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes) on to remove elements selectively.

### How to install or update dependencies?

#### Python

**Note on [pip-tools](https://github.com/jazzband/pip-tools)**:
- Only edit the `.in` files and use `invoke pip-compile-lock` to generate `.txt` files.
- Both `(dev-)requirements.txt` and `(dev-)requirements.in` files need to be pushed to Github.
- `.txt` files act as lockfiles, where dependencies are pinned to a precise version.

Dependencies live on your filesystem: you don't need to rebuild the `backend` image when installing or updating dependencies.

**Install packages:**

- Modify the `requirements.in` or `dev-requirements.in` to add the dependency you want to install.
- Run `invoke pip-compile-lock`.
- Run `invoke pip-sync`.

**Update packages:**

- `invoke pip-compile "-upgrade (dev-)requirements.in"`: update all (the dev) dependencies.
- `invoke pip-compile "--upgrade-package [PACKAGE](==x.x.x)"`: update the specified dependency. To update multiple dependencies, you always need to add the `-P` flag.

When it's done, run `inv pip-sync`.

#### JS

Dependencies live on your filesystem: you don't need to rebuild the `watch-static-files` image when installing or updating dependencies.

**Install packages:**

Use `invoke npm "install [PACKAGE]"`.

**Update packages:**

Use `invoke npm update`.

## Connecting Docker to your code editor

### Pycharm

This feature is only available for the professional version of Pycharm. Follow the official instructions [available here](https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html#config-docker)

### Visual Studio Code

Visual Studio Code use a feature called Dev Container to run Docker projects. The configuration files are in the `.devconatainer` directory. This feature is only available starting VSCode 1.35 stable. For now, we're only creating a python container to get Intellisense, we're not running the full project inside VSCode. We may revisit this in the future if Docker support in VSCode improves.

A few things to keep in mind when using that setup:
- Do not use the terminal in VSCode when running `invoke docker-` commands: use a local terminal instead,
- when running `inv docker-catchup` or installing python dependencies, you will need to rebuild the Dev Container. To do that, press `F1` and look for `Rebuild Container`.

#### Instructions:

- Install the [Remote - containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers),
- Open the project in VSCode: it detects the Dev Container files and a popup appears: click on `Reopen in a Container`,
- Wait for the Dev Container to build,
- Work as usual and use the docker invoke commands in a terminal outside VSCode.

## Debugging and testing

### Testing the code

You can test the code using the `inv test` command. This may fail for four reasons:

1. JS(X) linting errors
2. (S)CSS linting errors
3. Python linting errors
4. `manage test` failure.

In case of (1) or (2), you can run `inv npm "run fix"`, which should fix any linting erros for JS(X) and (S)CSS. We do not currently have automated fixing in place for Python errors.


### Integration tests

Integration testing is done using [Playwright](https://playwright.dev/), with the integration tests found in ./tests/integration.spec.js

You can run these tests locally by running a one-time `npm run playwright:install` after which you should be able to run `npm run playwright` to run the visual tests.

Note that this is still a work in progress.


### Debugging the code

Ensure you have the official [python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) for Visual Studio Code installed. It provides the debugging type required for the run configuration to work.

1. Set the `VSCODE_DEBUGGER` value to `True` in your .env

2. Rebuild your Docker containers: `inv docker-catchup`, then `docker-compose up`

3. Start the debug session from VS Code for the `[django:docker] runserver` configuration

   1. Open up the debugger, or open the Command Palette and select
      `View: Show Run and Debug`.

   2. Select `[django:docker] runserver` from the dropdown near the Play button in the top left.

   3. Hit the Play button or hit `F5` to start debugging

      - Logs will redirect to your integrated terminal as well.

4. Set some breakpoints!

   - You can create a breakpoint by clicking to the left of a line number. When that code is
     executed, the debugger will pause code execution so you can inspect the call stack and
     variables. You can either resume code execution or manage code execution manually by stepping
     into the next pieces of code, or over them.

Note that sometimes, bugs only show when the `DEBUG` environment variable is set to `False`, as this turns off some quality-of-life improvements for local development that are not used on production. In order for the code to work properly with `DEBUG=False`, remember to also run through the production bootstrapping steps:

- Make sure to have run `npm run build` so that the front end gets built without debug affordances
- Make sure to run `inv migrate collectstatic` as only the official static asset dir will be used by Django when not running in debug mode

---

## Docker vocabulary and overview

Welcome to Docker! Before jumping into Docker installation, take a moment to get familiar with Docker vocabulary:

- Docker: Docker is a platform to develop, deploy and run applications with containers.
- Docker engine: The Docker engine is a service running in the background (daemon). It's managing containers.
- Docker CLI: Command Line Interface to interact with Docker. For example, `Docker image ls` lists the images available on your system.
- Docker hub: Registry containing Docker images.
- Image: An image is a file used to build containers: In our case, it's mostly instructions to install dependencies.
- Container: Containers run an image. In our case, we have a container for the database, another one for building static files and the last one for running Django. A container life is ephemeral: data written there don't persist when you shut down a container.
- Volume: A volume is a special directory on your machine that is used to make data persistent. For example, we use it to store the database: that way, you don't lose your data when you turn down your containers.
- Host: host is used in Docker docs to mean the system on top of which containers run.
- Docker-compose: It's a tool to run multi-container applications: we use it to run our three containers together.
- Docker-compose CLI: Command line interface to interact with docker-compose. It's used to launch your dev environment.
- Docker-compose service: a service is a container and the configuration associated to it.

I would recommend watching [An Intro to Docker for Djangonauts](https://www.youtube.com/watch?v=qsEfVSTZO9Q) by Lacey Williams Henschel (25 min, [repo mentioned in the talk](https://github.com/williln/docker-hogwarts)): it's a great beginner talk to learn Docker and how to use it with Django.

### Project Structure

All our containers run Linux.

For local development, we have two Dockerfiles that define our images:
- `Dockerfile.node`: use a node12 Debian Stretch slim base image from the Docker Hub and install node dependencies.
- `Dockerfile.python`: use a python3.9 Debian Stretch slim base image, install required build dependencies before installing the project dependencies.
We don't have a custom image for running postgres and use one from the Docker Hub.

The `docker-compose.yml` file describes the 4 services that the project needs to run:
- `watch-static-files`: rebuilds static files when they're modified.
- `postgres`: contains a postgres database.
- `backend`: runs Django. Starting this one automatically starts the two other ones.
- `backend-worker`: runs a RQ Worker to process donations.

### Resources about Docker

- [Docker](https://docs.docker.com/) and [Docker-compose](https://docs.docker.com/compose/overview/) documentations,
- [Intro to Docker](https://www.revsys.com/tidbits/brief-intro-docker-djangonauts/): Lacey wrote a good intro tutorial to Docker and Django, without Harry Potter metaphors this time :),
- [Jérôme Petazzoni's training slides and talks](https://container.training/): presentations and slides if you want to dive into Docker.
