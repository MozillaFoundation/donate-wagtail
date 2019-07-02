# donate-wagtail

[![Build Status](https://travis-ci.org/mozilla/donate-wagtail?branch=master)](https://travis-ci.org/mozilla/donate-wagtail)

## Notes on Docker

Docker expects values in the ".env" files to be without quotes, while pipenv wants quotes. Because of that, we need a ".env" and a ".env-docker".

It should be possible to connect the python virtual env inside the container to your IDE (tested with pycharm and vscode), if you run into issues, ping patjouk on slack.
