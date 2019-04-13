import urllib.request
import urllib.parse
import json

def getResult(content):
    url='http://fy.iciba.com/ajax.php?a=fy'#翻译网站
    data={}                             #给网站递交的post内容
    data['f']='auto'
    data['t']='auto'
    data['w']=content
    data=urllib.parse.urlencode(data).encode('utf-8')
    answer=1
    while answer==1:
        try:
            response=urllib.request.urlopen(url,data,timeout=4)
        except:
            answer=messagebox.askretrycancel('错误！','连接超时！请检查网络设置')
            result=''
        else:
            answer=0
            html=response.read().decode('utf-8')
            html=json.loads(html)
            temp=html['content']
            if 'word_mean' in temp:
                result=temp['word_mean'][0][:-1]
            else:
                result=temp['out']
    result=result.replace('#','\n')    #解决换行问题2
    return result

if __name__ == '__main__':
    content = input('输入需要翻译的内容：')
    print(getResult(content))
