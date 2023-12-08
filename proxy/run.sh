#!/bin/sh

# Runs all commands as batch and fails all if any command fails
set -e

# Env substitute passes all the ENV variables
# defined in /etc/nginx/default.conf.tpl and produces
# a new config /etc/nginx/conf.d/default.conf at runtime
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# Start nginx and daemon off makes it run in the foreground
# as the primary application
nginx -g 'daemon off;'