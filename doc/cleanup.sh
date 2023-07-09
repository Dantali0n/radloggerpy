#!/bin/bash

FILE_DIR=$(dirname -- "$(readlink -f -- "${0}")")

echo "Cleaning.. ${FILE_DIR}/source/source_documentation/*"

for f in "${FILE_DIR}"/source/source_documentation/*
do

  case $f in
    */index.rst) true;;
    *) echo "Removing.. ${f}"; rm "${f}";;
  esac
done