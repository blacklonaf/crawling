from pathlib import Path
from datetime import datetime

from crawl_modules.fetchHTML import fetch_html
from crawl_modules.parHEADnaver import parse_headlines
from crawl_modules.savetoCSV import save_to_csv

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--section', type=str, required=True)
    return parser.parse_args()

def main(section_code = '105'):
    base_url = f"https://news.naver.com/section/{section_code}"
    html = fetch_html(base_url)
    if not html:
        return
    
    keyword = input("키워드 입력 (여러개 쉼표 구분) : ").split(',') # input, interactive 형태. 추후 CLI, 프로그램 등에선 argparse 이용.
    today = datetime.today().strftime("%Y-%m-%d")

    BASE_DIR = Path(__file__).parent

    for kw in keyword:
        records = parse_headlines(html, keyword=kw)
        csv_path = BASE_DIR / 'data' / f'{today}' / f'news_{section_code}_{kw}.csv'
        save_to_csv(records, csv_path)

# 이는 해당 파일을 직접 실행할 때만 실행하는 조건문
# 즉 다른 파일에서 import를 통해 실행되더라도 해당 조건문에는 충족되지 않아 해당 파일이 실행되는 것을 방지할 수 있다.
if __name__ == "__main__": 
    args = parse_args()
    section_code = args.section
    print(f'{section_code} 네이버 헤드라인을 검색합니다.')
    main(section_code)