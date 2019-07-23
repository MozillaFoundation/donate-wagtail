# donate-wagtail

[![Build Status](https://travis-ci.org/mozilla/donate-wagtail.svg?branch=master)](https://travis-ci.org/mozilla/donate-wagtail)

## Table of contents

- [How to setup your dev environment with Docker](#how-to-setup-your-dev-environment-with-docker),
- [How to use Invoke tasks](#invoke-tasks),
- [Basket donations queue](#basket)

## Notes on Docker

It should be possible to connect the python virtual env inside the container to your IDE (tested with pycharm and vscode), if you run into issues, ping patjouk on slack.

## How to Setup your Dev Environment with Docker

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (macOS and Windows). For Linux users: install [Docker CE](https://docs.docker.com/install/#supported-platforms) and [Docker Compose](https://docs.docker.com/compose/install/). If you don't want to create a Docker account, direct links to download can be found [in this issue](https://github.com/docker/docker.github.io/issues/6910),
- [Check your install](https://docs.docker.com/get-started/#test-docker-version) by running `docker run hello-world`,
- [Install Invoke](https://www.pyinvoke.org/installing.html),
- If relevant: delete your node_modules directory (`rm -rf node_modules`). It's not necessary, but it speeds up the install.
- Run `inv docker-setup`. 

When it's done, run `docker-compose up`, wait until the static files to be built, and go to `0.0.0.0:8000`. When you want to stop, do `^C` to shut down your containers.

## Invoke tasks

Invoke is a python tasks runner that creates shortcuts for commands we frequently use. For example, instead of `docker-compose run --rm backend pipenv manage.py migrate`, you can use `inv docker-migrate`. It can also be used to run management commands: `inv docker-manage load-fake-data`. If you need to add multiple args to an invoke commands, use quotes. ex: `invoke docker-npm "install moment"`

Installation instructions: https://www.pyinvoke.org/installing.html

### With Docker

### Invoke tasks available:

- `inv -l`: list available tasks,
- `inv docker-catch-up (docker-catchup)`: Rebuild images and apply migrations
- `inv docker-makemigrations`: Creates new migration(s)
- `inv docker-manage`: Shorthand to manage.py. ex: `inv docker-manage "[COMMAND] [ARG]"`
- `inv docker-migrate`: Updates database schema
- `inv docker-npm`: Shorthand to npm. ex: `inv docker-npm "[COMMAND] [ARG]"`
- `inv docker-nuke-db`: Delete your database and create a new one with fake data
- `inv docker-pipenv`: Shorthand to pipenv. ex: `inv docker-pipenv "[COMMAND] [ARG]"`
- `inv docker-setup`: Prepare your dev environment after a fresh git clone
- `inv docker-test-python`: Run python tests

Use `docker-compose up/down` to start or shutdown the dev server.

**note**: use `inv docker-setup` when you've just cloned the repo. If you did a `git pull` on master and want to install the latest dependencies and apply migrations, use `inv docker-catchup` instead.

### Without Docker

### Invoke tasks available:

- `inv -l`: list available tasks,
- `inv catch-up (catchup)`: Install dependencies and apply migrations
- `inv makemigrations`: Creates new migration(s)
- `inv manage`: Shorthand to manage.py. ex: `inv manage "[COMMAND] [ARG]"`
- `inv migrate`: Updates database schema
- `inv setup`: Prepare your dev environment after a fresh git clone
- `inv test`: Run python tests
- `inv runserver`: Start a web server

**note**: use `inv setup` when you've just cloned the repo. If you did a `git pull` on master and want to install the latest dependencies and apply migrations, use `inv catchup` instead.

### Without Invoke

### Running commands inside the Docker container

When the Django server is running, you can start the Django shell with:

    docker-compose exec backend pipenv run python manage.py shell

### Running tests

Run the back-end test suite with:

    docker-compose exec backend pipenv run python manage.py test --settings=donate.settings_test


## Basket

[Basket](https://github.com/mozmeao/basket) is a tool run by MoCo to manage newsletter subscriptions and donations. It's listening for messages (JSON) sent to a SQS queue.

### Basket donations queue:

Basket has 4 [donation event types](https://github.com/mozmeao/basket/blob/master/basket/news/management/commands/process_donations_queue.py#L21-L26): 

- `donation`: process a donation and send its data to SFDC,
- `crm_petition_data`: add petition signature to SFDC,
- `newsletter_signup_data`: newsletter signup for the foundation site,
- `DEFAULT`: process a followup Stripe event on a donation.

For this project, we're only using the `donation` event type.

### Donation event type

Example of a donation message sent to Basket:

```
{ event_type: 'donation',
  last_name: 'alex',
  email: 'alex@alex.org',
  donation_amount: 50,
  currency: 'usd',
  created: 1563801762,
  recurring: false,
  service: 'stripe',
  transaction_id: 'ch_1Ez1TSG8Mmx3htnxyShib70n',
  project: 'mozillafoundation',
  last_4: '4242',
  donation_url: 'http://localhost:3000/en-US/',
  locale: 'en-US',
  conversion_amount: 50,
  net_amount: 48.6,
  transaction_fee: 1.4 }
```

`event_type`: Basket event type. Should be donation,
`first_name`: first name of the donor (optional),
`last_name`: last name of the donor,
`email`: email of the donor,
`donation_amount`: amount of the donation,
`currency`: letter code for the currency,
`created`: unix timestamp,
`recurring`: `false` for a one-time donation or `true` for a recurring one,
`service`: name of the payment processor (ex: `stripe` or `paypal`)
`transaction_id`: ID generated by the payment processor,
`project`: name of the project that will receive the donation (ex: `thunderbird`, `mozillafoundation`)
`last_4`: last 4 digits of the credit card,
`donation_url`: url from which the donation was made,
`locale`: language code for the donor,
`conversion_amount`: donation amount in USD, before transaction fees,
`net_amount`: donation amount in USD, after transaction fees,
`transaction_fee`: payment processor's transaction fees in USD


### Newsletter signup

We're using Basket newsletter API to signup people to our newsletter. Specs are available in [Basket's documentation](https://basket.readthedocs.io/newsletter_api.html#news-subscribe)

Example from donate.mozilla.org:
```
 { format: 'html',
   lang: 'en-US',
   newsletters: 'mozilla-foundation',
   trigger_welcome: 'N',
   source_url: 'https://donate.mozilla.org/',
   email: 'alex@alex.org',
   country: undefined }
```

_Notes_: We want to keep the `trigger_welcome` at `N` and the `format` to `html`. We don't have the country info for now, but from what I understood, it's something we want to change.
