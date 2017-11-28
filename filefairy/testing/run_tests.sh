#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
for py_file in $(find $DIR -name *test.py)
do
  python $py_file
done
