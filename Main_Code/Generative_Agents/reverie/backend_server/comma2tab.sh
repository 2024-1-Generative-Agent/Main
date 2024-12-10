#!/bin/bash

# 입력으로 받은 텍스트 파일 경로
FILE_PATH="$1"

# 파일이 존재하는지 확인
if [ ! -f "$FILE_PATH" ]; then
  echo "파일이 존재하지 않습니다: $FILE_PATH"
  exit 1
fi

# 쉼표를 탭으로 변환하여 임시 파일에 저장
TEMP_FILE=$(mktemp)
sed 's/,/\t/g' "$FILE_PATH" > "$TEMP_FILE"

# 원본 파일을 백업하고 변환된 내용을 덮어쓰기
cp "$FILE_PATH" "${FILE_PATH}.bak"
mv "$TEMP_FILE" "$FILE_PATH"

echo "쉼표를 탭으로 변환 완료: $FILE_PATH (백업 파일: ${FILE_PATH}.bak)"