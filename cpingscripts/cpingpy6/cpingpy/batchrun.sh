#!/bin/bash
c=1
while [ $c -le 5 ]
do
	echo "Running $c time"
	(( c++ ))
    python3 cping.py
    sleep 300
done
