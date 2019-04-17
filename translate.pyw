from tkinter import Tk,LabelFrame,Scrollbar,RIGHT,Y,Text,LEFT,Button,Menu,mainloop,END,messagebox
from tkinter import filedialog
from tkinter import messagebox
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
    result = ''
    post = True
    while post:
        try:
            response = urlopen(url,data,timeout=4)
        except:
            post = messagebox.askretrycancel('错误！','连接超时！请检查网络设置')
        else:
            post = False
            html = response.read().decode('utf-8')
            html = loads(html)
            part = html['content']
            if not part:        #某些词语+符号的组合 网站不显示翻译结果
                messagebox.showerror('错误！','翻译失败=-=')
            else:
                if 'word_mean' in part: #单词
                    result = part['word_mean'][0][:-1]
                else:                   #句子
                    result = part['out']

    result = result.replace('#','\n')    #解决换行问题2

    return result

def clear():
    text1.delete(0.0,END)
    text2.delete(0.0,END)
    
def showcontent():
    fileName = filedialog.askopenfilename()
    if fileName!='':
        try:
            with open(fileName,'r') as f:
                content = f.read()
            text1.insert(0.0 , content)
        except:
            messagebox.showwarning('警告！','请打开文本文件')
         
def showresult():
    content = text1.get(0.0 , END)
    content = content.replace('\n','#')  #解决换行问题1
    if content.count('#') == 1:     #带符号单词会无法获得翻译结果
        content = content[:-1]

    result = getResult(content)
            
    text2.delete(0.0 , END)
    text2.insert(0.0 , result)

def saveresult():
    fileName = filedialog.asksaveasfilename() + '.txt'
    with open(fileName,'w') as f:
        f.write(text2.get(0.0 , END))



root=Tk()
root.title("翻译/Traslation")

frame1 = LabelFrame(root,text = "请在此输入需要翻译的内容")
frame1.grid(column = 0,row = 0,padx = 10,pady = 10)

scr1 = Scrollbar(frame1)
scr1.pack(side = RIGHT,fill = Y)

text1 = Text(frame1 , height = 15 , width = 40 , font = 10)
text1.pack(side = LEFT , fill = Y)

scr1.config(command = text1.yview)
text1.config(yscrollcommand = scr1.set)

frame2 = LabelFrame(root,text = "翻译结果")
frame2.grid(column = 3 , row = 0 , padx = 10 , pady = 10)

scr2 = Scrollbar(frame2)
scr2.pack(side = RIGHT,fill = Y)

text2 = Text(frame2,height = 15 , width = 40 , font = 10)
text2.pack(side = LEFT , fill = Y)

scr2.config(command = text2.yview)
text2.config(yscrollcommand = scr2.set)

trasbutton = Button(root,text = "翻译" , height = 2 , width = 10 ,font = 10 ,\
                    bg = "yellow" , fg = "blue" , command = showresult)
trasbutton.grid(column = 2 , row = 0)

menuroot = Menu(root)
root.config(menu = menuroot)
filemenu = Menu(menuroot , tearoff = False)
filemenu.add_command(label = '打开文件',command = showcontent)
filemenu.add_command(label = '保存文件',command = saveresult)
filemenu.add_command(label = '清空内容',command = clear)
filemenu.add_command(label = '退出',command = root.quit)
menuroot.add_cascade(label = '菜单',menu = filemenu)

mainloop()

