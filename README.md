# donate-wagtail

[![Build Status](https://travis-ci.org/mozilla/donate-wagtail?branch=master)](https://travis-ci.org/mozilla/donate-wagtail)

## Notes on Docker

Docker expects values in the ".env" files to be without quotes, while pipenv wants quotes. Because of that, we need a ".env" and a ".env-docker".

It should be possible to connect the python virtual env inside the container to your IDE (tested with pycharm and vscode), if you run into issues, ping patjouk on slack.

## How to Setup your Dev Environment with Docker

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (macOS and Windows). For Linux users: install [Docker CE](https://docs.docker.com/install/#supported-platforms) and [Docker Compose](https://docs.docker.com/compose/install/). If you don't want to create a Docker account, direct links to download can be found [in this issue](https://github.com/docker/docker.github.io/issues/6910),
- [Check your install](https://docs.docker.com/get-started/#test-docker-version) by running `docker run hello-world`,
- If relevant: delete your node_modules directory (`rm -rf node_modules`). It's not necessary, but it speeds up the install.
- Copy `env.default` to `.docker.env` in the project root.
- Run `docker-compose build`.

When it's done, run `docker-compose up`, wait until the static files to be built, and go to `0.0.0.0:8000`. When you want to stop, do `^C` to shut down your containers.

### Running commands inside the Docker container

When the Django server is running, you can start the Django shell with:

    docker-compose exec backend pipenv run python manage.py shell

(TODO: wrap this with invoke to make it less cumbersome).
