# donate-wagtail

[![Build Status](https://travis-ci.org/mozilla/donate-wagtail.svg?branch=master)](https://travis-ci.org/mozilla/donate-wagtail)

## Table of contents

- [How to setup your dev environment with Docker](#setup-your-dev-environment-with-docker)
- [Basket donations queue](#basket)

## Documentation

- [Pages](docs/pages.md)
- [Pontoon Integration](docs/pontoon_integration.md)
- [Local dev](./docs/local_dev.md)

## Setup your Dev Environment with Docker

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (macOS and Windows). For Linux users: install [Docker CE](https://docs.docker.com/install/#supported-platforms) and [Docker Compose](https://docs.docker.com/compose/install/).
- [Check your install](https://docs.docker.com/get-started/#test-docker-version) by running `docker run hello-world`.
- [Install Invoke](https://www.pyinvoke.org/installing.html). We recommend you use [pipx](https://pypi.org/project/pipx/)
- Run `inv new-env`: it's building docker images, installing dependencies, setting up a populated DB, and configuring your environment variables.

When it's done, run `docker-compose up`, wait for the static files to be built, and go to `0.0.0.0:8000`. When you want to stop, do `^C` to shut down your containers. If they don't stop properly, run `docker-compose down`. If you want a new dev environment, stop your containers and run `inv new_env`.

It's possible to connect your IDE to the python virtual env available inside the backend container (tested with pycharm and vscode). If you run into issues, ping patjouk on slack.

To run commands with Docker, run `docker-compose run [SERVICE] [COMMAND]`. For example, running the python tests is done by `docker-compose run backend ./dockerpythonvenv/bin/python manage.py test --settings=donate.settings_test`. Since it's pretty long, most cases are covered by Invoke commands.

More information on how to use Docker for local dev is available in the [Local dev](./docs/local_dev.md) documentation.

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

### Environment variables

Non-secret envs can be added to the `app.json` file. Secrets must be set on Heroku in the `Review Apps` section of the pipelines' `settings` tab.

### Review App for PRs

Opening a PR will automatically create a Review App in the `donate-wagtail` and `thunderbird-donate` pipelines. A slack bot posts credentials and links to Review Apps in to the `mofo-ra-donate-wagtail` and `mofo-ra-thunderbird-donate-wagtail` channels.

*Note:* This only work for Mo-Fo staff: you will need to manually open a Review App on Heroku for PRs opened by external contributors.

### Review App for branches

You can manually create a review app for any branch pushed to this repo. It's useful if you want to test your code on Heroku without opening a PR yet.
To create one:
- log into Heroku.
- Go in the `donate-wagtail` or `thunderbird-donate` pipeline.
- Click on `+ New app` and select the branch you want to use.

The review app slack bot will post a message in either the `mofo-ra-donate-wagtail` or `mofo-ra-thunderbird-donate-wagtail` with links and credentials as soon as the review app is ready.

## SSO and admin logins for local development

The default for admin login for local development is the standard Django login. To use Mozilla SSO via OpenID Connect, set the `USE_CONVENTIONAL_AUTH` environment variable to `False`.

To make sure you can log in using your Mozilla SSO credentials, your will need to create a Django superuser with your mozilla email address, using:

```shell
docker-compose exec app python manage.py createsuperuser
```

## Adding users to the system

The security model currently requires that an existing admin creates an account for a new user first, tied to that user's Mozilla email account, before that user can can log in using SSO.

Further more, in order for SSO authentication to succeed, their account must be a member of the donate user group. To request that an account be added to this group, please file [an SSO request bug](https://bugzilla.mozilla.org/enter_bug.cgi?product=Infrastructure%20%26%20Operations&component=SSO:%20Requests), making sure to also `cc` a donate admin in the bug.

## Translations

Translation is happening on [Pontoon](https://pontoon.mozilla.org), in multiple projects where you can participate:

| Project on Pontoon                          | Source repository                  |
|---------------------------------------------|------------------------------------|
[Mozilla & Thunderbird UI strings (Django)](https://pontoon.mozilla.org/projects/mozilla-donate-website/) | [Repository on GitHub](https://github.com/mozilla-l10n/donate-l10n)
[Mozilla (CMS content)](https://pontoon.mozilla.org/projects/donate-mozilla-content/) | [Repository on GitHub](https://github.com/mozilla-l10n/mozilla-donate-content)
[Thunderbird (CMS content)](https://pontoon.mozilla.org/projects/donate-thunderbird-content/) | [Repository on GitHub](https://github.com/mozilla-l10n/thunderbird-donate-content)

The latest UI source strings are regularly exposed to Pontoon by a Localization PM using the process below. The CMS strings are automatically synchronized with the repositories.

### Initial setup:
- Clone the `donate-l10n` repository locally.
- Set the `LOCAL_PATH_TO_L10N_REPO` variable in your `.env` file. Use the absolute path to your copy of the `donate-l10n` repository and include the trailing slash. E.g. `LOCAL_PATH_TO_L10N_REPO=/Users/username/Documents/GitHub/donate-l10n/`

### Exposing latest source strings:
- Make sure your local repositories of `donate-l10n` and `donate-wagtail` are matching the latest revision from master.
- Run `inv docker-makemessages` from your `donate-wagtail` repository.
- Files should have been updated in your `donate-l10n` repository. You can now create a pull-request.

### Getting the latest translations for local dev

Latest translations are uploaded to S3. To get them, run:
- `curl -o translations.tar https://donate-wagtail-translations.s3.amazonaws.com/translations.tar`
- `tar -C network-api -xvf translations.tar`

You don't need to run `compilemessages`.

The `translations_github_commit_[...]` file from the archive is only used for debug purposes on Heroku. It can be safely deleted if needed.
