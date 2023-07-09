#!/usr/bin/env bash

set -r

function confirm() {
    printf "$* [y/N]: "
    read -r confirm_response
    if [ "$confirm_response" != "y" ]; then
        echo "exiting..."
        exit
    fi
}

DIR=$(pwd | xargs basename)
if [ "$DIR" != "workflow" ]; then
    echo "Not running from 'workflow', enter the path to the workflow repo"
    read -r WORKFLOW
else
    WORKFLOW=$(pwd)
fi
echo "Using repo path: $WORKFLOW"

HOST=$(hostname)

NEW_HOST=$WORKFLOW/hosts/$HOST

if test -d "$NEW_HOST"; then
    echo "$NEW_HOST already exists, keeping old copy"
else
    echo "Choose one of the following hosts (with similar setup) to start with:"
    ls "$WORKFLOW"/hosts
    read -r COPY_HOST
    cp -r $WORKFLOW/hosts/$COPY_HOST $NEW_HOST
fi
mkdir "$WORKFLOW/local_scripts"

FILES=$(find $NEW_HOST -type f | xargs)
echo "Hit enter to run:"
echo "vim -p $FILES"
read
vim -p $FILES
echo "If ready to pull run:"
echo "$NEW_HOST/pull_to_$HOST"
