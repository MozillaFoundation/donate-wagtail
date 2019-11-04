#!/usr/bin/env bash
# Create the necessary config files to be able to push to GitHub from Heroku.
# Used for syncing translation files between Pontoon and wagtail-donate-prod

set -e

if [ $USE_PONTOON ]; then
  echo "Generating SSH config"
  SSH_DIR=/app/.ssh

  mkdir $SSH_DIR
  chmod 700 $SSH_DIR

  echo $SSH_KEY > $SSH_DIR/id_rsa
  chmod 400 $SSH_DIR/id_rsa

  echo $SSH_CONFIG > $SSH_DIR/config
  chmod 600 $SSH_DIR/config
  echo "Done!"
fi
