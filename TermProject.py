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

import graph
import LineMap
import RealTimeDv

g_Tk = Tk()
g_Tk.geometry('900x650')
notebook = tkinter.ttk.Notebook(g_Tk, width=600, height=600)
notebook.pack(side=RIGHT)
DataList = []
url = 'openapi.seoul.go.kr:8088'
api_key = ''
query = '/' + api_key + '/xml/subwayStationMaster/'



#호선명
SGGUCD = [['1/10','1호선'], ['11/60','2호선'], ['61/94','3호선'],
          ['95/97','진접선'], ['98/123','4호선'], ['124/130','경부선']
          , ['131/145','경원선'], ['146/153','분당선'], ['388/443','5호선']]

'''import http.client
conn = http.client.HTTPConnection(url)
conn.request('GET', query+SGGUCD[0][0])'''

def showMap(frame):
    global browser
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id(), [0,0,600,600])
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
    
    for i in range(9):
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

def LSearch():
    surl = 'http://openapi.seoul.go.kr:8088/' + api_key + '/xml/subwayStationMaster/1/500'
    response = requests.get(surl)
    root = ET.fromstring(response.content)
    maps = root.findall('row')

    Station = []
    for i in maps:
        mapping = {
            'Name': i.findtext('STATN_NM'),
            'route': i.findtext('ROUTE'),
            'Ypos': i.findtext('CRDNT_Y'),
            'Xpos': i.findtext('CRDNT_X')
        }
        Station.append(mapping)

    print(Station[0]['Name'])

    path = inputBox.get()
    print(path)

    for name in Station:
        if name["Name"] == path:
            Sname = name['Name']
            start_Y = name['Ypos']
            Start_X = name['Xpos']

    m = folium.Map(location=[start_Y, Start_X], zoom_start=13)
    folium.Marker([start_Y, Start_X], popup=Sname).add_to(m)

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
    RenderText.place(x=10, y=250)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=210, y=250)

    RenderText.configure(state='disabled')


InitTopText()
InitSearchListBox()
InitSearchButton()
InitRenderText()
frame2 = Frame(g_Tk, width=600, height=600)
notebook.add(frame2, text='지도')
frame3 = Frame(g_Tk, width=600, height=600)
notebook.add(frame3, text='노선도')
frame4 = Frame(g_Tk, width=600, height=600)
notebook.add(frame4, text='그래프')
frame5 = Frame(g_Tk, width=600, height=600)
notebook.add(frame5, text='실시간')
#frame2.pack()
#frame2.place(x=300,y=180)

NameLabel = Label(g_Tk, text='역 이름')
NameLabel.pack()
NameLabel.place(x=10, y=210)

inputBox = Entry(g_Tk)
inputBox.pack()
inputBox.place(x = 55, y= 210, width= 100, height= 22)

Sbutton = Button(g_Tk, text='찾기', command=LSearch)
Sbutton.pack()
Sbutton.place(x=165, y=210)

graph.initGraph(frame4)
LineMap.InitMap(frame3)
RealTimeDv.InitRealTime(frame5)

setup()
g_Tk.mainloop()