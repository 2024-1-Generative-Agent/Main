#!/bin/bash

source_file="spatial_memory.json"
target_root="../../../../storage/ours/personas" #change spatial memory


if [ ! -d "$target_root" ]; then
  echo "Error: Target root folder '$target_root' does not exist."
  exit 1
fi

if [ ! -f "$source_file" ]; then
  echo "Error: Source JSON file '$source_file' does not exist."
  exit 1
fi

# 모든 하위 폴더를 탐색하여 memory 폴더에 복사
for dir in "$target_root"/*/; do
  memory_dir="${dir}bootstrap_memory/"
  if [ -d "$memory_dir" ]; then
    cp "$source_file" "$memory_dir"
    echo "Copied '$source_file' to '$memory_dir'"
  else
    echo "Warning: '$memory_dir' does not exist, skipping..."
  fi
done

echo "Finished copying JSON file to all 'memory' folders."
