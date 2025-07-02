import requests
import re
import os
from bs4 import BeautifulSoup

if not os.path.exists('music_download'):
    os.mkdir('music_download')
while True:
    ms_name = input('请输入歌名/歌手：')
    url = f'https://www.gequbao.com/s/{ms_name}'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        ,
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        ,
        'cache-control': 'max-age=0'
        ,
        'dnt': '1'
        ,
        'priority': 'u=0, i'
        ,
        'referer': 'https://www.gequbao.com/?from=www.xiaozhongjishu.com'
        ,
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"'
        ,
        'sec-ch-ua-mobile': '?0'
        ,
        'sec-ch-ua-platform': '"Windows"'
        ,
        'sec-fetch-dest': 'document'
        ,
        'sec-fetch-mode': 'navigate'
        ,
        'sec-fetch-site': 'same-origin'
        ,
        'sec-fetch-user': '?1'
        ,
        'upgrade-insecure-requests': '1'
        ,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
        ,
    }

    response = requests.get(url=url, headers=headers)
    html = response.text
    # print(html)
    # 'https://www.gequbao.com' +
    mu_url_id = re.findall('<a href="(.*?)" target="_blank"><u>播放&下载</u></a>', html)
    music_name = re.findall('<span>(.*?)</span>', html)

    singer = re.findall(r'<small class="text-jade\s*font-weight-bolder\s*align-middle">\s*([^<]+?)\s*</small>', html)

    # 创建歌曲列表并显示序号
    songs = []
    print("\n搜索结果：")
    for i, (name, sing, url_id) in enumerate(zip(music_name, singer, mu_url_id), 1):
        songs.append((name, sing, url_id))
        print(f"{i}. {name} - {sing}")

    # 用户选择要下载的歌曲
    if not songs:
        print("没有找到相关歌曲！")
        exit()

    selection = input("\n请输入要下载的歌曲序号（多个用空格分隔）：")
    selected_indices = [int(idx) - 1 for idx in selection.split() if idx.isdigit()]
    selected_indices = [idx for idx in selected_indices if 0 <= idx < len(songs)]

    if not selected_indices:
        print("没有有效的选择，程序退出。")
        exit()

    # 下载选中的歌曲
    for idx in selected_indices:
        name, sing, url_id = songs[idx]
        url_1 = 'https://www.gequbao.com' + url_id
        print(f"\n开始下载: {name} - {sing} ({idx + 1}/{len(songs)})")

        # 原有逻辑保持不变
        response1 = requests.get(url=url_1, headers=headers)
        html1 = response1.text
        play_id = re.findall('"play_id":"(.*?)","mp3_title":', html1)[0]
        soup = BeautifulSoup(html1, 'html.parser')
        lyrics = str(soup.find('div', id='content-lrc'))
        # print(lyrics)
        lyrics_content = lyrics.strip('<div class="content-lrc mt-1" id="content-lrc">').strip('</div>').replace(
            '<br/>',
            '')

        # 保存歌词
        with open('music_download\\' + f'{name}--{sing}' + '.lrc', mode='w', encoding='utf-8') as textual:
            textual.write(lyrics_content)
        # print(soup)
        print(lyrics_content)
        url2 = 'https://www.gequbao.com/api/play-url'
        params = {
            "id": play_id
        }
        response2 = requests.post(url=url2, json=params)
        music_url = response2.json()['data']['url']
        # print(music_url)
        res = requests.get(url=music_url).content

        # 保存音乐文件
        with open('music_download\\' + f'{name}--{sing}.mp3', mode='wb') as f:
            f.write(res)
        print(f"下载完成: {name} - {sing}")

    print("\n所有选中的歌曲下载完成！")
