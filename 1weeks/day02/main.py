# find_all vs find
# find      => 첫 번째로 매칭된 요소 하나만 반환
# find_all  => 매칭된 모든 요소를 리스트로 반환

from bs4 import BeautifulSoup

html = """
<ul class="items">
  <li><a href="/p1">상품1</a></li>
  <li><a href="/p2">상품2</a></li>
  <li><a href="/p3">상품3</a></li>
</ul>
"""

soup = BeautifulSoup(html, 'html.parser')

# find_all 사용
items = soup.find_all('li')
for li in items:
    print(li.text) # 상품1, 상품2, 상품3

# find 사용
first = soup.find('li')
print(first.text) # 상품1

# class=items인 ul 태그 내부 li태그 내부의 a 모든 태그 선택
links = soup.select('ul.items li a')
for a in links:
    print(a['href'], a.text) # a의 href(링크)값과 a의 text 값을 가져옴
    # /p1 상품1
    # /p2 상품2
    # /p3 상품3

# get으로 attribute 추출 방법
for a in links:
    href = a.get('href')    # 안전하게 href 가져오기 가능
    title = a.text.strip()
    print(title, "->", href)

