import sys
import io
import threading

from datetime import datetime
from playsound import playsound

from PyQt6.QtCore import QTimer, QTime, QDate
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>885</width>
    <height>655</height>
   </rect>
  </property>
  <property name="font">
   <font>
    <pointsize>14</pointsize>
   </font>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QCalendarWidget" name="calendarWidget">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>10</y>
      <width>451</width>
      <height>271</height>
     </rect>
    </property>
   </widget>
   <widget class="QPlainTextEdit" name="eventInfo">
    <property name="geometry">
     <rect>
      <x>500</x>
      <y>50</y>
      <width>301</width>
      <height>161</height>
     </rect>
    </property>
   </widget>
   <widget class="QDateEdit" name="dateEdit">
    <property name="geometry">
     <rect>
      <x>500</x>
      <y>230</y>
      <width>121</width>
      <height>21</height>
     </rect>
    </property>
    <property name="date">
     <date>
      <year>2024</year>
      <month>12</month>
      <day>10</day>
     </date>
    </property>
   </widget>
   <widget class="QTimeEdit" name="timeEdit">
    <property name="geometry">
     <rect>
      <x>640</x>
      <y>230</y>
      <width>118</width>
      <height>22</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>510</x>
      <y>20</y>
      <width>211</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>18</pointsize>
     </font>
    </property>
    <property name="text">
     <string>опишите событие:</string>
    </property>
   </widget>
   <widget class="QPushButton" name="create_btn">
    <property name="geometry">
     <rect>
      <x>560</x>
      <y>260</y>
      <width>121</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>16</pointsize>
     </font>
    </property>
    <property name="text">
     <string>создать</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_dateleft">
    <property name="geometry">
     <rect>
      <x>60</x>
      <y>410</y>
      <width>291</width>
      <height>21</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>14</pointsize>
     </font>
    </property>
    <property name="text">
     <string>dateleft</string>
    </property>
   </widget>
   <widget class="QProgressBar" name="progressBar">
    <property name="geometry">
     <rect>
      <x>60</x>
      <y>520</y>
      <width>381</width>
      <height>23</height>
     </rect>
    </property>
    <property name="value">
     <number>24</number>
    </property>
   </widget>
   <widget class="QLabel" name="label1">
    <property name="geometry">
     <rect>
      <x>60</x>
      <y>320</y>
      <width>201</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>18</pointsize>
     </font>
    </property>
    <property name="text">
     <string>осталось:</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_timeleft">
    <property name="geometry">
     <rect>
      <x>60</x>
      <y>370</y>
      <width>291</width>
      <height>20</height>
     </rect>
    </property>
    <property name="text">
     <string>timeleft</string>
    </property>
   </widget>
   <widget class="QListWidget" name="eventList">
    <property name="geometry">
     <rect>
      <x>495</x>
      <y>371</y>
      <width>351</width>
      <height>211</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label_4">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>330</y>
      <width>191</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>16</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Список событий:</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>885</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class Project(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)

        self.alarm_year = 0
        self.alarm_month = 0
        self.alarm_day = 0
        self.alarm_hour = 0
        self.alarm_min = 0
        self.time = 'hh-mm'
        self.date = 'dd-MM-yyyy'

        self.is_playing = False  # Флаг для отслеживания воспроизведения звука
        self.create_btn.clicked.connect(self.otvet)

        self.timeEdit.setTime(QTime.currentTime())
        self.dateEdit.setDate(QDate.currentDate())


        # Настроим таймер для периодической проверки времени(частота - раз в секунду)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_time)
        self.timer.start(1000)  
    

    def otvet(self): 
        self.name = self.eventInfo.toPlainText()  # описание события
        self.date = self.dateEdit.dateTime().toString('dd-MM-yyyy')  # дата события
        self.time = self.timeEdit.dateTime().toString('hh-mm')  # время события

        # Извлекаем компоненты даты и времени
        self.alarm_year = int(self.date[6:])
        self.alarm_month = int(self.date[3:5])
        self.alarm_day = int(self.date[0:2])
        self.alarm_hour = int(self.time[0:2])
        self.alarm_min = int(self.time[3:5])

        self.eventList.addItem(f"{self.name} {self.date} {self.time}")
        self.label_timeleft.setText(self.calculate_time_left(self.time))
        self.label_dateleft.setText(self.calculate_date_left(self.date))
        
        
    def calculate_time_left(self, target_time):
        if QTime.currentTime() != QTime.fromString(target_time, 'hh-mm'):
            now = QTime.currentTime()
            diff = now.secsTo(QTime.fromString(target_time, 'hh-mm'))
            hours = (diff % 86400) // 3600
            minutes = (diff % 3600) // 60 + 1
            if hours < 0:
                hours += 24
            if minutes < 0:
                minutes += 60
            return f"Осталось: {hours} часов, {minutes} минут"
        return f"Осталось: 0 часов, 0 минут"
    

    def calculate_date_left(self, target_date):
        target_date = QDate.fromString(target_date, 'dd-MM-yyyy')
        now = QDate.currentDate()

        years = target_date.year() - now.year()
        months = target_date.month() - now.month()
        days = target_date.day() - now.day()

        if days < 0:
            months -= 1
            days += now.daysInMonth()

        if months < 0:
            years -= 1
            months += 12

        return f"Осталось: {years} лет, {months} месяцев, {days} дней"
        

    def update_time_left(self):
        self.label_timeleft.setText(self.calculate_time_left(self.time))
    

    def update_date_left(self):
        self.label_dateleft.setText(self.calculate_date_left(self.date))

    
    def check_time(self):
        # Получение текущего времени
        now = datetime.now()
        self.current_year = now.year  
        self.current_month = now.month  
        self.current_day = now.day  
        self.current_hour = now.hour  
        self.current_min = now.minute  

        if (self.alarm_year == self.current_year and 
            self.alarm_month == self.current_month and 
            self.alarm_day == self.current_day and 
            self.alarm_hour == self.current_hour and 
            self.alarm_min == self.current_min and 
            not self.is_playing):
                self.is_playing = True  # Устанавливаем флаг воспроизведения
                file_path = 'D:\grisha\GfinalProjectLMS\GalarmMusic.mp3' # Мой файл с музыкой
                threading.Thread(target=playsound, args=(file_path,)).start()  # Воспроизведение звука
                
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Project()
    ex.show()
    sys.exit(app.exec())