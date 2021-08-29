#!/bin/bash

var actual_dir = $PWD;
var target_working_dir = actual_dir + "/src"


python ./src/app.py target_working_dir

while [ true ]
do
	noop
done

done
