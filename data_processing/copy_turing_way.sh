#!/bin/bash
source_dir="../../the-turing-way/book/website"
data_dir="../data/the_turing_way_md"
files=`find ${source_dir} -name "[^_]*.md"`
mkdir -p ${data_dir}
for file_name in "${files[@]}"; do
  rsync -vv ${file_name} ${data_dir}
done
