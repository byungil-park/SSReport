# -*- coding: utf-8 -*-
#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime, timedelta
import traceback
from xml.etree import ElementTree as ET
import noti


TOKEN = ''
key = ''

class IsSearching:
    def __init__(self, user):
        self.id = user
        self.isSearching = False

def getSubwayData(station_name):
    url = f'http://swopenapi.seoul.go.kr/api/subway/{key}/xml/realtimeStationArrival/0/30/{station_name}'

    # API 호출
    response = requests.get(url)

    if response.status_code == 200:
        # XML 데이터 파싱
        root = ET.fromstring(response.content)
        items = root.findall('row')

        subway_data = []

        for item in items:
            name = item.findtext('statnNm')
            line = item.findtext('updnLine')
            direction = item.findtext('trainLineNm')
            arriving_time = item.findtext('arvlMsg2')

            subway_data.append((name, line, direction, arriving_time))

        return subway_data
    else:
        return None

def replySubwayData(station_name, user):
    print(user, station_name)
    subway_data = getSubwayData(station_name)
    if subway_data:
        msg = ''
        for data in subway_data:
            msg += f'지하철역: {data[0]}, 라인 번호: {data[1]}, 방향: {data[2]}, 도착 예정 시간: {data[3]}\n'
        noti.sendMessage(user, msg)
    else:
        noti.sendMessage(user, '해당 지하철역 정보를 가져올 수 없습니다.')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('지하철') and len(args) > 1:
        print('try to 지하철', args[1])
        replySubwayData(args[1], chat_id)
    elif text.startswith('저장') and len(args) > 1:
        print('try to 저장', args[1])
        getSubwayData(chat_id, args[1])
    elif text.startswith('확인'):
        print('try to 확인')
        getSubwayData(chat_id)
    else:
        noti.sendMessage(chat_id, '모르는 명령어입니다.\n지하철 [지하철역명], 저장 [지하철역명], 확인 중 하나의 명령을 입력하세요.')



today = date.today()
current_month = today.strftime('%Y%m')

print('[', today, ']received token :', noti.TOKEN)

bot = telepot.Bot(noti.TOKEN)
pprint(bot.getMe())

bot.message_loop(handle)

print('Listening...')

while 1:
    time.sleep(10)
