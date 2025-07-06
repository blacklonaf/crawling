# [IT 뉴스 최신 헤드라인 10개 추출 후 저장]
# extra_mission :   크롤링 대상 키워드를 input으로 받아 처리하도록 할 것.
#                   os.path.join을 통해 저장 경로 자동 생성

import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import csv


def fetch_html(url, timeout=10): # timeout 변수 기본 값을 10으로 초기화 / 변수 기본 값으로, 이는 함수 실행해서 누락하면 기본 값 적용
    try:
        resp = requests.get(url, timeout=timeout) # timeout 판단 기준을 10초로 지정
        resp.raise_for_status # 상태 코드가 4xx(클라이언트 오류), 5xx(서버 오류)일 때, HTTPError 예외를 발생시킨다.
        # 단순 상태 코드를 반환하고 싶은 경우, resp.status_code를 이용

    except requests.exceptions.Timeout: # 타임아웃 예외가 발생했을 경우
        print(f"[ERROR] 요청 시간 초과 : {url}")
        return None
    except requests.exceptions.HTTPError as e: # HTTPError가 발생했을 경우
        print(f"[ERROR] HTTP 에러({e.response.status_code}) : {url}")
        return None
    except requests.exceptions.RequestException as e: # 이외의 모든 에러가 발생했을 경우,
        print(f"[ERROR] 요청 중 예외 발생 : {e}") # 해당 에러 내용을 그대로 출력함.
        return None
    else:
        return resp.text
    finally:
        print("finally는 예외처리 상관없이 항상 실행") 
        # 이는 db 연결 해제, 파일 세션 닫기 등 결과에 상관없이 수행되어야하는 동작에 적용한다.
    
def parse_headlines(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('ul.sa_list li.sa_item._SECTION_HEADLINE')
    data = []
    for a in items:
        title = a.select_one('strong.sa_text_strong').get_text(strip=True)
        link  = a.select_one('a.sa_text_title._NLOG_IMPRESSION')['href']
        summary_tag = a.select_one('div.sa_text_lede')
        summary = summary_tag.get_text(strip=True) if summary_tag else "" # summary_tag가 존재하지 않을 경우, ""으로 초기화
        if (keyword.lower() in title.lower()) or (keyword.lower() in summary.lower()): # lower() 함수로 키워드가 대소문자 구분하지 않도록 설정.
            data.append({
                'title' : title,
                'link' : link,
                'summary' : summary
            }) # dictionary로 저장
    if not data:
        print(f"'{keyword}' 키워드에 해당하는 내용이 없습니다.")
    return data

def save_to_csv(data, path):
    os.makedirs(path.parent, exist_ok=True) # result 파일이 존재하지 않아 경로를 못찾는 경우를 방지하는 result 파일 제작
    try:
        with open(path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'link', 'summary'])
            writer.writeheader()
            writer.writerows(data)
    except OSError as e:
        print(f"[ERROR] 파일 저장 실패: {e}")
    else:
        print(f"[INFO] CSV 저장 완료: {path}")

def main(section_code = '105'):
    base_url = f"https://news.naver.com/section/{section_code}"
    html = fetch_html(base_url)
    if not html:
        return
    
    keyword = input("추출하고자하는 키워드를 입력해주세요 : ")

    records = parse_headlines(html, keyword=keyword)

    # __file__ : 해당 파일의 위치 (C:\Users\hwaro_0\Desktop\crolling\1weeks\day04\subject1.py)
    BASE_DIR = Path(__file__).parent # 현재 파일의 부모 파일의 path 개체 (C:\Users\hwaro_0\Desktop\crolling\1weeks\day04)
    csv_path = BASE_DIR / 'results' / f'news_{section_code}.csv' # 저장할 csv 파일의 전체 경로 지정 / 이는 open 함수에서 사용 가능
    save_to_csv(records, csv_path)

# 이는 해당 파일을 직접 실행할 때만 실행하는 조건문
# 즉 다른 파일에서 import를 통해 실행되더라도 해당 조건문에는 충족되지 않아 해당 파일이 실행되는 것을 방지할 수 있다.
if __name__ == "__main__": 
    section_num = 101
    for i in range(5):
        print(section_num)
        main(section_num)
        section_num = section_num + 1