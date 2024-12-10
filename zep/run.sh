#!/bin/bash

# npx zep-script archive 명령어 실행
echo "Running 'npx zep-script archive'..."
npx zep-script archive

# 위 명령어의 성공 여부를 확인
if [ $? -ne 0 ]; then
    echo "'npx zep-script archive' failed. Aborting."
    exit 1
fi

echo "'npx zep-script archive' succeeded."

# npx zep-script publish 명령어 실행
echo "Running 'npx zep-script publish'..."
npx zep-script publish

# 위 명령어의 성공 여부를 확인
if [ $? -ne 0 ]; then
    echo "'npx zep-script publish' failed."
    exit 1
fi

echo "'npx zep-script publish' succeeded."
