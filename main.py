from tkinter import *
from tkinter import font
from sample import StationMap

class StationMapGUI:
    def SetEntry(self):
        self.EStart = Entry(self.window)
        self.EStart.place(x=130, y=30)
        self.LGoal = Entry(self.window)
        self.LGoal.place(x=130, y=80)

    def SetButton(self):
        self.BBookmark = Button(self.window, text='즐겨찾기', width=15, height=2, font=self.fontstyle2)
        self.BBookmark.place(x=50, y=280)
        self.Search = Button(self.window, text='가까운 역 찾기', width=15, height=2, font=self.fontstyle2)
        self.Search.place(x=50, y=380)

        self.LPrediction = Button(self.window, text='길 찾기', width=12, height=1, font=self.fontstyle2, command=self.find_route)
        self.LPrediction.place(x=130, y=130)

    def SetLabel(self):
        self.LStart = Label(self.window, text='출발역', width=6, height=1, font=self.fontstyle2)
        self.LStart.place(x=50, y=30)
        self.LGoal = Label(self.window, text='도착역', width=6, height=1, font=self.fontstyle2)
        self.LGoal.place(x=50, y=80)

    def find_route(self):
        start_station = self.EStart.get()  # 출발역 입력값 가져오기
        goal_station = self.LGoal.get()  # 도착역 입력값 가져오기

        station_map = StationMap()
        subway_stations = station_map.get_subway_stations()

        if subway_stations is not None and start_station in subway_stations and goal_station in subway_stations:
            # 출발역과 도착역이 모두 유효한 경우에만 로직 실행

            # 출발역과 도착역 사이의 경로 탐색 (너비 우선 탐색 알고리즘 활용)
            visited = set()  # 방문한 역 목록
            queue = [[start_station]]  # 탐색 큐
            found = False

            while queue:
                path = queue.pop(0)
                current_station = path[-1]

                if current_station == goal_station:
                    # 도착역에 도달한 경우 경로 출력
                    print(" -> ".join(path))
                    found = True
                    break

                if current_station not in visited:
                    visited.add(current_station)

                    # 현재 역과 인접한 역들을 탐색하여 큐에 추가
                    if current_station in subway_stations:
                        adjacent_stations = subway_stations[current_station]
                        for station in adjacent_stations:
                            new_path = list(path)
                            new_path.append(station)
                            queue.append(new_path)

            if not found:
                print("경로를 찾을 수 없습니다.")
        else:
            print("유효한 역 이름을 입력하세요.")

    def __init__(self):
        self.window = Tk()
        self.window.title('지하철 맵')
        self.window.geometry('1200x600')
        self.window.configure(bg='white')
        self.fontstyle = font.Font(self.window, size=24, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=16, weight='bold', family='Consolas')
        self.SetLabel()
        self.SetButton()
        self.SetEntry()

        self.window.mainloop()

if __name__ == '__main__':
    station_map_gui = StationMapGUI()