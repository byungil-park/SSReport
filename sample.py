import requests
import xml.etree.ElementTree as ET

class StationMap:
    def __init__(self):
        self.decoding = 'BKWL/Ns986D6yTDU7dJUJFTfLLquRZlIfEkQ+MXXANgvuZ8w1C3R8lxTvpdl4VW/xcfUEvwchK3+qt666UG1UA=='
        self.url = 'http://apis.data.go.kr/1613000/SubwayInfoService/getKwrdFndSubwaySttnList'
        self.params = {
            'serviceKey': self.decoding,
            'pageNo': '1',
            'numOfRows': '1000',
            '_type': 'xml'
        }

    def get_subway_stations(self):
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            subway_stations = {}

            items = root.findall('.//item')
            for item in items:
                station_name = item.find('subwayStationName').text
                station_id = item.find('subwayStationId').text

                if station_name not in subway_stations:
                    subway_stations[station_name] = [station_id]
                else:
                    subway_stations[station_name].append(station_id)

            return subway_stations

        else:
            print("API 호출 실패")
            return None