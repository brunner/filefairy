#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
for py_file in $(find $DIR -name *$1.py)
do
  python $py_file
done
