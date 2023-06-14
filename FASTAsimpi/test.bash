#!/usr/bin/env bash
declare id
declare name
declare url
declare version

while read line; do
  if [[ ! ${line} =~ ^[\+\| ]]; then
    if [[ ${line} =~ \|[[:space:]]*([[:digit:]]+)[[:space:]]*\|[[:space:]]+([[:alnum:]\.]+)[[:space:]]+\|[[:space:]]+(https?:\/\/(www\.)?[[:alnum:]]+\.[[:alpha:]]+\/?)[[:space:]]*\|[[:space:]]*([[:digit:]](\.[[:digit:]])?)[[:space:]]*\|  ]]; then
      id="${BASH_REMATCH[1]}"
      name="${BASH_REMATCH[2]}"
      url="${BASH_REMATCH[3]}"
      version="${BASH_REMATCH[5]}"
      echo "${id}:${name}:${url}:${version}"
    fi
  fi
done
