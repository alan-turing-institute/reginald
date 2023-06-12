#!/bin/bash
handbook_dir="../../REG-handbook"
data_dir="../data/handbook"
files=`find ${handbook_dir}/content/ -name "[^_]*.md"`
for file_name in "${files[@]}"; do
  rsync -vv ${file_name} ${data_dir}
done
