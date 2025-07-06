from bs4 import BeautifulSoup

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