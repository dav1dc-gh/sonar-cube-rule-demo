#!/bin/sh

# This is a script that will allow us to burn (remove) a file from a local git repository. This is useful when we want to remove a file that contains sensitive information, such as a password or an API key, from the repository's history.
# Usage: ./bash.sh <file-to-remove>
if [ -z "$1" ]; then
  echo "Usage: $0 <file-to-remove>"
  exit 1
fi
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch $1" --prune-empty --tag-name-filter cat -- --all
echo "File '$1' has been removed from the repository's history. Please run 'git push --force' to update the remote repository." 

