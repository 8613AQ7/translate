from urllib.request import urlopen
from urllib.parse import urlencode
from json import loads

def getResult(content):
    url = 'http://fy.iciba.com/ajax.php?a=fy'#翻译网站
    data={}                             #给网站递交的post内容
    data['f'] = 'auto'
    data['t'] = 'auto'
    data['w'] = content
    data = urlencode(data).encode('utf-8')
    try:
        response = urlopen(url,data,timeout=4)
    except:
        result=''
    else:
        html = response.read().decode('utf-8')
        html = loads(html)
        temp = html['content']
        if 'word_mean' in temp:
            result = temp['word_mean'][0][:-1]
        else:
            result = temp['out']
                
    result = result.replace('#','\n')    #解决换行问题2
    return result

if __name__ == '__main__':
    while True:
        content = input('输入需要翻译的内容：')
        print(getResult(content))
