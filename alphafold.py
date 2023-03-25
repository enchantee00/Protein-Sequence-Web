import requests
from bs4 import BeautifulSoup


response = requests.get(url)


if response.status_code == 200:
    #텍스트 형태의 html
    html = response.content
    #html을 수프 객체로 변환 -> 원하는 태크 추출 쉽게 만들어줌
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
    # msp-sequence-wrapper-non-empty
    try:
        title = soup.find('span', '')
        print(type(title))
        print(title.get_text())

        # array = soup.select_one('span.msp-sequence-wrapper msp-sequence-wrapper-non-empty')
        # seqs = array.select('span.msp-sequence-present')
        # print(seqs)
        # for seq in seqs:
        #     print(seq.get_text())
    except AttributeError: 
        print("에러")

else:
    print(response.status_code)



#main-content-area > app-entry > div:nth-child(2) > div > div.columns.small-12.medium-9.molstarView > div > div > div > div > div.msp-layout-region.msp-layout-top > div > div > div.msp-sequence-wrapper.msp-sequence-wrapper-non-empty > span:nth-child(2)