import urllib.parse
import base64
import mimetypes
import requests
from time import sleep

srcs = []

for search in searches:
    q = urllib.parse.quote_plus(search)
    url = f'https://www.bing.com/images/search?q={q}&form=RESTAB&first=1'
    driver.get(url)
    amount = -1

    while amount != len(srcs):
        amount = len(srcs)
        driver.find_element('xpath', '/html/body').send_keys(Keys.CONTROL + Keys.END)
        sleep(4)

        imgs = driver.find_elements('xpath', '//img')
        for img in imgs:
            src = img.get_attribute('src')
            if src not in srcs and src is not None:
                srcs.append(src)

    print(f'найдено изображений: {len(srcs)}')

for i in range(len(srcs)):
    url = srcs[i]

    if 'base64' in url:
        mime_type = url.split(';')[0].split(':')[1]
        content = base64.b64decode(url.split(',')[1])
        ext = mimetypes.guess_extension(mime_type)

        if 'svg' not in ext:
            fname = f'{i}{ext}'
            with open(fname, 'wb') as f:
                f.write(content)

    else:
        response = requests.get(srcs[i])
        mime_type = response.headers['content-type']
        ext = mimetypes.guess_extension(mime_type)
        fname = f'{i}{ext}'

        if 'svg' not in ext:
            with open(fname, 'wb') as f:
                f.write(response.content)

    sleep(3)
    print(f'Скачали {fname}')
