from tkinter import *
from tkinter import font

g_Tk = Tk()
g_Tk.geometry('400x600+750+200')
DataList = []
url = 'openapi.seoul.go.kr:8088'
api_key = ''
query = '/' + api_key + '/xml/subwayStationMaster/'



#호선명
SGGUCD = [['1/10','1호선'], ['11/60','2호선'], ['61/94','3호선'],
          ['95/97','진접선'], ['98/123','4호선'], ['124/130','경부선']]

'''import http.client
conn = http.client.HTTPConnection(url)
conn.request('GET', query+SGGUCD[0][0])'''

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font = TempFont, text='[지하철 호선 검색]')
    MainText.pack()
    MainText.place(x=20)
    
def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=150,y=50)
    
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',
                            width=10, height=5, borderwidth= 12, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)
    
    for i in range(6):
        SearchListBox.insert(i+1, SGGUCD[i][1])
        
    SearchListBox.pack()
    SearchListBox.place(x=10,y=50)

    ListBoxScrollbar.config(command=SearchListBox.yview)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family= 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text='검색', command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=330, y=110)

def SearchButtonAction():
    global SearchListBox

    RenderText.configure(state ='normal')
    RenderText.delete(0.0,END)
    iSearchIndex = SearchListBox.curselection()[0]

    sgguCD = SGGUCD[iSearchIndex][0]
    Search(sgguCD)

    RenderText.configure(state='disabled')

def Search(sgguCD):
    import http.client
    conn = http.client.HTTPConnection(url)
    conn.request("GET", query+sgguCD)

    req = conn.getresponse()


    global DataList
    DataList.clear()

    if req.status == 200:
        strXml = req.read().decode('utf-8')
        #print(strXml)
        from xml.etree import ElementTree
        tree = ElementTree.fromstring(strXml)
        itemElements = tree.iter('row')
        #print(itemElements)
        for item in itemElements:
            Sname = item.find('STATN_NM')
            Sroute = item.find('ROUTE')
            Ypos = item.find('CRDNT_Y')
            Xpos = item.find('CRDNT_X')
            DataList.append((Sname.text, Sroute.text, Ypos.text, Xpos.text))

        for i in range(len(DataList)):
            RenderText.insert(INSERT, '[')
            RenderText.insert(INSERT, i + 1)
            RenderText.insert(INSERT, ']')
            RenderText.insert(INSERT, '지하철 명: ')
            RenderText.insert(INSERT, DataList[i][0])
            RenderText.insert(INSERT, '\n')
            RenderText.insert(INSERT, '호선 : ')
            RenderText.insert(INSERT, DataList[i][1])
            RenderText.insert(INSERT, '\n')
            RenderText.insert(INSERT, '위도: ')
            RenderText.insert(INSERT, DataList[i][2])
            RenderText.insert(INSERT, '경도: ')
            RenderText.insert(INSERT, DataList[i][3])
            RenderText.insert(INSERT, '\n\n')

def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375,y=200)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=49, height=27, borderwidth=12, relief='ridge',
                      yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')

InitTopText()
InitSearchListBox()
InitSearchButton()
InitRenderText()
g_Tk.mainloop()