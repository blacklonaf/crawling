import csv
from bs4 import BeautifulSoup
import requests
import os # 운영체제 경로 처리

url = "https://news.naver.com/section/105"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
base = soup.select('ul.sa_list li.sa_item._SECTION_HEADLINE')

with open('it_science.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['제목', '링크', '요약'])   # 헤더
    for a in base:
        title = a.select_one('strong.sa_text_strong').get_text(strip=True)
        link = a.select_one('a.sa_text_title._NLOG_IMPRESSION').get('href')
        summary = a.select_one('div.sa_text_lede').get_text(strip=True)
        writer.writerow([title, link, summary])

print("it_science.csv 파일로 저장 완료!")