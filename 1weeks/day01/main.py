# 네이버의 html 코드를 500자까지만 가져옴
import requests

url = "https://news.naver.com/section/101"

response = requests.get(url)

print(response.text[:500])


# 특정 태그의 정보 추출하기

from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, 'html.parser') 
# 단순 텍스트 html을 개발자 도구에서 보는 트리구조로 바꿈으로써 파싱이 가능하도록 변환

### 특정 데이터 추출 방법

## find(tag) -> 해당 가장 먼저 찾은 해당 태그 정보 1개
title_tag = soup.find('title') # 태그까지 저장
title_tag_text = soup.find('title').text # 태그 내부의 text만 저장

print("페이지 제목 : ", title_tag) # 페이지 제목 :  <title>경제 : 네이버 뉴스</title>
print("페이지 제목 : ", title_tag_text) # 페이지 제목 :  경제 : 네이버 뉴스

## select(css 선택자 = class) -> 해당하는 클래스의 요소를 리스트로 여러개 추출
select_text = soup.select('a.sa_text_title._NLOG_IMPRESSION strong') # 다중 클래스로 묶여있을 경우, 점으로 표현
print("select : ", select_text) 
# [<strong class="sa_text_strong">역대급 폭염 예고...냉방속도 빠르고 전기료 덜 나오는 에어컨은?</strong>, <strong class="sa_text_strong">"연봉 5억에 모십니다"…삼성전자 '파격 채용' 나섰다</strong>] 이 외로도 더 많이 나온다.

# select로 여러 개를 가져와 list로 저장한 경우, 따로 전처리를 진행해주어야 함. -> 이를 통해 태그를 제거한 말끔한 기사들 추출출
for tag in select_text:
    print(tag.text.strip()) # strip()로 줄바꿈 태그, 좌우 불필요한 공백을 제거함.

text_list = [tag.text.strip() for tag in select_text]
print(text_list) # 해당 뉴스 기사들을 리스트로 출력함