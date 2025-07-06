import os
import csv
from pathlib import Path

def save_to_csv(data, path):
    os.makedirs(path.parent.parent, exist_ok=True)
    os.makedirs(path.parent, exist_ok=True)
    try:
        with open(path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'link', 'summary'])
            writer.writeheader()
            writer.writerows(data)
    except OSError as e:
        print(f"[ERROR] 파일 저장 실패: {e}")
    else:
        print(f"[INFO] CSV 저장 완료: {path}")