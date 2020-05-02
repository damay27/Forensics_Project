#!/bin/bash

git --no-pager --git-dir ./merged/.git log | grep "commit " | awk '{ print $2 }'