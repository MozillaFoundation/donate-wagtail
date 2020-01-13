# donate-wagtail

[![Build Status](https://travis-ci.org/mozilla/donate-wagtail.svg?branch=master)](https://travis-ci.org/mozilla/donate-wagtail)

## Table of contents

- [How to setup your dev environment with Docker](#setup-your-dev-environment-with-docker),
- [How to use Invoke tasks](#invoke-tasks),
- [Basket donations queue](#basket)

## Documentation

- [Pages](docs/pages.md)
- [Pontoon Integration](docs/pontoon_integration.md)

## Setup your Dev Environment with Docker

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (macOS and Windows). For Linux users: install [Docker CE](https://docs.docker.com/install/#supported-platforms) and [Docker Compose](https://docs.docker.com/compose/install/). If you don't want to create a Docker account, direct links to download can be found [in this issue](https://github.com/docker/docker.github.io/issues/6910),
- [Check your install](https://docs.docker.com/get-started/#test-docker-version) by running `docker run hello-world`,
- [Install Invoke](https://www.pyinvoke.org/installing.html),
- If relevant: delete your node_modules directory (`rm -rf node_modules`). It's not necessary, but it speeds up the install.
- Run `inv docker-new-env`: it's building docker images, installing dependencies, setting up a populated DB, and configuring your environment variables.

When it's done, run `docker-compose up`, wait for the static files to be built, and go to `0.0.0.0:8000`. When you want to stop, do `^C` to shut down your containers. If they don't stop properly, run `docker-compose down`. If you want a new dev environment, stop your containers and run `inv docker-new_env`.

It's possible to connect your IDE to the python virtual env available inside the backend container (tested with pycharm and vscode). If you run into issues, ping patjouk on slack.

To run commands with Docker, run `docker-compose run [SERVICE] [COMMAND]`. For example, running the python tests is done by `docker-compose run backend pipenv run python manage.py test --settings=donate.settings_test`. Since it's pretty long, most case are covered by Invoke commands.

## Configuration

[Django Configurations](https://django-configurations.readthedocs.io/en/stable/) is used for application configuration. The following Configuration Classes are provided:

| Value                 | Purpose                                                                                                            |
|-----------------------|--------------------------------------------------------------------------------------------------------------------|
| Development           |  Base configuration, suitable for local development.                                                               |
| Staging               | Staging configuration.                                                                                             |
| Production            | Production configuration.                                                                                          |
| ReviewApp             | Review App configuration. Use this configuration for Heroku Review apps.                                           |
| ThunderbirdDevelopment | Base configuration that enables all the Thunderbird template and string overrides. Suitable for local development. |
| ThunderbirdStaging    | Staging configuration for Thunderbird donation configurations.                                                     |
| ThunderbirdProduction | Production configuration for Thunderbird donation configurations.                                                  |
| ThunderbirdReviewApp  | Review App configuration for Thunderbird donation configurations.                                                  |


## Invoke tasks

Invoke is a python tasks runner that creates shortcuts for commands we frequently use. For example, instead of `docker-compose run --rm backend pipenv manage.py migrate`, you can use `inv docker-migrate`. It can also be used to run management commands: `inv docker-manage load-fake-data`. If you need to add multiple args to an invoke commands, use quotes. ex: `invoke docker-npm "install moment"`

Installation instructions: https://www.pyinvoke.org/installing.html

### Invoke tasks available:

Run `inv -l` in your terminal to get the list of available tasks.

- `inv docker-catch-up (docker-catchup)`: Rebuild images and apply migrations
- `inv docker-makemigrations`: Creates new migration(s)
- `inv docker-manage`: Shorthand to manage.py. ex: `inv docker-manage "[COMMAND] [ARG]"`
- `inv docker-makemessages`: Extract all template messages in .po files for localization
- `inv docker-compilemessages`: Compile the latest translations
- `inv docker-migrate`: Updates database schema
- `inv docker-new-env`: Get a new dev environment and a new database with fake data
- `inv docker-new-db`: Delete your database and create a new one with fake data
- `inv docker-npm`: Shorthand to npm. ex: `inv docker-npm "[COMMAND] [ARG]"`
- `inv docker-pipenv`: Shorthand to pipenv. ex: `inv docker-pipenv "[COMMAND] [ARG]"`
- `inv docker-test-python`: Run python tests

## Braintree configuration

The following environment variables are required to configure payment processing via Braintree:

- `BRAINTREE_MERCHANT_ID`: the merchant ID for the Braintree account used to process donations.
- `BRAINTREE_MERCHANT_ACCOUNTS`: a series of key-value pairs that map each supported currency to the corresponding Braintree merchant account that is configured in that currency. For example: `usd=usd-ac,gbp=gbp-ac,eur=eur-ac` where `usd-ac`, `gbp-ac` and `eur-ac` are merchant account IDs.
- `BRAINTREE_PLANS`: a series of key-value pairs that map each supported currency to the corresponding Braintree subscription plan that is configured in that currency. For example: `usd=usd-plan,gbp=gbp-plan,eur=eur-plan` where `usd-plan`, `gbp-plan` and `eur-plan` are plan IDs.
- `BRAINTREE_PUBLIC_KEY`: Public API key provided by Braintree.
- `BRAINTREE_PRIVATE_KEY`: Private API key provided by Braintree.
- `BRAINTREE_TOKENIZATION_KEY`: Tokenization key provided by Braintree.
- `BRAINTREE_USE_SANDBOX`: Boolean to configure whether or not to use the Braintree sandbox.

### Webhook Configuration

There's a webhook endpoint for processing Braintree events. The events it supports are:

* `subscription_charged_successfully`
* `subscription_charged_unsuccessfully`
* `dispute_lost`

The endpoint accepts requests on `/braintree/webhook/` and will verify the payload signature to ensure it's a legitimate event. [Documentation for Braintree webhooks can be found here](https://developers.braintreepayments.com/guides/webhooks/overview).

## Basket

[Basket](https://github.com/mozmeao/basket) is a tool run by MoCo to manage newsletter subscriptions and donations. It's listening for messages (JSON) sent to a SQS queue.

### Basket donations queue:

Basket has [4 event types we can use](https://github.com/mozmeao/basket/blob/master/basket/news/management/commands/process_donations_queue.py#L21-L26):

- `donation`: process a donation and send its data to SFDC,
- `crm_petition_data`: add petition signature to SFDC,
- `newsletter_signup_data`: newsletter signup for the foundation site,
- `DEFAULT`: process a followup Stripe event on a donation.

For this project, we're only using the `donation` event type.

### Donation event type

Example of a donation message sent to Basket, via SQS:

```
{
    'data': {
        'event_type': 'donation',
        'last_name': 'alex',
        'email': 'alex@alex.org',
        'donation_amount': 50,
        'currency': 'usd',
        'created': 1563801762,
        'recurring': false,
        'service': 'paypal',
        'transaction_id': 'ch_1Ez1TSG8Mmx3htnxyShib70n',
        'project': 'mozillafoundation',
        'last_4': '4242',
        'donation_url': 'http://localhost:3000/en-US/',
        'locale': 'en-US',
        'conversion_amount': 50,
        'net_amount': 48.6,
        'transaction_fee': 1.4
    }
}
```

- `event_type`: Basket event type. Should be donation,
- `first_name`: first name of the donor (optional),
- `last_name`: last name of the donor,
- `email`: email of the donor,
- `donation_amount`: amount of the donation,
- `currency`: letter code for the currency,
- `created`: unix timestamp,
- `recurring`: `false` for a one-time donation or `true` for a recurring one,
- `service`: name of the payment processor (ex: `stripe` or `paypal`)
- `transaction_id`: ID generated by the payment processor,
- `project`: name of the project that will receive the donation (ex: `thunderbird`, `mozillafoundation`)
- `last_4`: last 4 digits of the credit card,
- `donation_url`: url from which the donation was made,
- `locale`: language code for the donor,
- `conversion_amount`: donation amount in USD, before transaction fees,
- `net_amount`: donation amount in USD, after transaction fees,
- `transaction_fee`: payment processor's transaction fees in USD


### Newsletter signup

We're using Basket newsletter HTTP API to signup people to our newsletter. Specs are available in [Basket's documentation](https://basket.readthedocs.io/newsletter_api.html#news-subscribe). (Note that this is different than the SQS approach used for donation events)

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

## Review App

Opening a PR will automatically create a Review App in the `donate-wagtail` pipeline. A slack bot posts credentials and links to Review Apps in to the `mofo-ra-donate-wagtail` channel.

This only work for Mo-Fo staff: you will need to manually open a Review App on Heroku for PRs opened by external contributors.

## SSO and admin logins for local development

The default for admin login for local development is the standard Django login. To use Mozilla SSO via OpenID Connect, set the `USE_CONVENTIONAL_AUTH` environment variable to `False`.

To make sure you can log in using your Mozilla SSO credentials, your will need to create a Django superuser with your mozilla email address, using:

```shell
docker-compose exec app python manage.py createsuperuser
```

## Adding users to the system

The security model currently requires that an existing admin creates an account for a new user first, tied to that user's Mozilla email account, before that user can can log in using SSO.

Further more, in order for SSO authentication to succeed, their account must be a member of the donate user group. To request that an account be added to this group, please file [an SSO request bug](https://bugzilla.mozilla.org/enter_bug.cgi?product=Infrastructure%20%26%20Operations&component=SSO:%20Requests), making sure to also `cc` a donate admin in the bug.
