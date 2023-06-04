from tkinter import *
from tkinter import font
import threading
import sys
from tkinter import messagebox
import folium
from cefpython3 import cefpython as cef
import requests
import xml.etree.ElementTree as ET
import tkinter.ttk

g_Tk = Tk()
g_Tk.geometry('800x600+750+200')
DataList = []
url = 'openapi.seoul.go.kr:8088'
api_key = '42704c444f62626938306557617842'
query = '/' + api_key + '/xml/subwayStationMaster/'



#호선명
SGGUCD = [['1/10','1호선'], ['11/60','2호선'], ['61/94','3호선'],
          ['95/97','진접선'], ['98/123','4호선'], ['124/130','경부선']]

'''import http.client
conn = http.client.HTTPConnection(url)
conn.request('GET', query+SGGUCD[0][0])'''

def showMap(frame):
    global browser
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id(), [0,0,400,400])
    cef.Initialize()
    browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
    cef.MessageLoop()

def setup():
    # 지도 저장
    # 위도 경도 지정
    m = folium.Map(location=[37.351735, 126.742989], zoom_start=13)
    # 마커 지정
    folium.Marker([37.351735, 126.742989], popup='정왕').add_to(m)
    # html 파일로 저장
    m.save('map.html')

    # 브라우저를 위한 쓰레드 생성
    thread = threading.Thread(target=showMap, args=(frame2,))
    thread.daemon = True
    thread.start()

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font = TempFont, text='[지하철 호선 검색]')
    MainText.pack()
    MainText.place(x=20,y=10)
    
def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=120,y=50)
    
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',
                            width=8, height=5, borderwidth= 12, relief='ridge',
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
    SearchButton.place(x=140, y=50)

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

        maps = tree.findall('row')
        Station01 = []
        # Station01Line = []
        for i in maps:
            mapping = {
                'Name': i.findtext('STATN_NM'),
                'route': i.findtext('ROUTE'),
                'Ypos': i.findtext('CRDNT_Y'),
                'Xpos': i.findtext('CRDNT_X')
            }
            Station01.append(mapping)

        print(DataList)

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
            RenderText.insert(INSERT, '\n')
            RenderText.insert(INSERT, '경도: ')
            RenderText.insert(INSERT, DataList[i][3])
            RenderText.insert(INSERT, '\n\n')

        ypos, xpos = float(DataList[0][2]), float(DataList[0][3])
        m = folium.Map(location=[ypos, xpos], zoom_start=13)

        for mapping in Station01:
            if mapping['Xpos'] and mapping['Ypos']:
                lat, lng = float(mapping['Ypos']), float(mapping['Xpos'])
                folium.Marker([lat, lng], popup=mapping['Name']).add_to(m)

        m.save('map.html')
        browser.Reload()

def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375,y=200)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=24, height=27, borderwidth=12, relief='ridge',
                      yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT)

    RenderText.configure(state='disabled')

InitTopText()
InitSearchListBox()
InitSearchButton()
InitRenderText()
frame2 = Frame(g_Tk, width=400, height=400)
frame2.pack(side=RIGHT)
setup()
g_Tk.mainloop()