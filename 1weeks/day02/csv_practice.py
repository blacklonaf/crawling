import csv
from bs4 import BeautifulSoup
import requests

url = "https://news.naver.com/section/101"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')

headlines = soup.select('ul.sa_list a.sa_text_title._NLOG_IMPRESSION')

with open('headlines.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['제목', '링크'])   # 헤더
    for a in headlines:
        title = a.get_text(strip=True)
        link = a.get('href')
        writer.writerow([title, link])

print("headlines.csv 파일로 저장 완료!")