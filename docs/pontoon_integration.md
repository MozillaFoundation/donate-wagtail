# Pontoon integration

[Pontoon](https://github.com/mozilla/pontoon) is Mozilla's Localization Platform. We use it to translate our donation platform (prod only).

## Configuration

### Settings

**SSH Configuration:**

Django based strings are translated on Pontoon, pushed directly to the `donate-wagtail` repo, and deployed with the rest of the code. For Wagtail based strings, we need an intermediate repo, [mozilla-donate-content](https://github.com/mozilla-l10n/mozilla-donate-content), that gets the latest translations from Pontoon and the newest strings to translate from `donate-wagtail`. To push to that repo, we need to add a deploy key with write access on GitHub. On Heroku, we need to run a script (`.profile`) that reads the `SSH_KEY` and `SSH_CONFIG` from the environment variables and write them as files. This script runs every time a dyno is created.

**Pontoon sync:**

A scheduled task runs every 20 minutes to sync the donate platform with the `mozilla-donate-content` repo. Users can trigger a sync in the Pontoon settings of the CMS admin.

**Environment Variables:**

- `USE_PONTOON`: set at `True` to use Pontoon. If set to `False`, the SSH configuration script won't run.
- `SSH_KEY`: SSH key to be able to push to `mozilla-donate-content`.
- `SSH_CONFIG`: must be set to `StrictHostKeyChecking=no`.

**Heroku requirements:**

- A worker dyno running `python manage.py rqworker wagtail_localize_pontoon.sync`,
- `Heroku Redis` add-on,
- `Heroku scheduler` running `python manage.py enqueue_pontoon_sync` every 20 min.

### First run

The initial sync needs to be run manually:

- **If the content repo is empty:** `touch README.md` and push this file to the master branch of the content repo.
- run `heroku login`.
- run `heroku run bash -a donate-wagtail-production`.
- run `python manage.py sync_languages`: creates `Language` objects for all languages defined in the `LANGUAGES` section of `settings.py`.
- run `python manage.py submit_whole_site_to_pontoon`: generates submissions for all live translatable pages.
- run `python manage.py sync_pontoon`: pushes the source strings to `mozilla-donate-content`.

## Thunderbird donate website

Thunderbird donate stack is also using Pontoon. The configuration is the same as Mozilla donate, the only difference being the content repo: [thunderbird-donate-content](https://github.com/mozilla-l10n/thunderbird-donate-content).
