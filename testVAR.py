import sys
import io
import threading
import os

from datetime import datetime
from playsound import playsound

from PyQt6.QtCore import QTimer, QTime, QDate, QDateTime
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
      <width>351</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>18</pointsize>
     </font>
    </property>
    <property name="text">
     <string>название (описание) события:</string>
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
      <x>50</x>
      <y>540</y>
      <width>331</width>
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
   <widget class="QLabel" name="label1">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>450</y>
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
      <x>50</x>
      <y>500</y>
      <width>331</width>
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
   <widget class="QPushButton" name="update_info_btn">
    <property name="geometry">
     <rect>
      <x>220</x>
      <y>400</y>
      <width>161</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>10</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Обновить инфорамцию</string>
    </property>
   </widget>
   <widget class="QPlainTextEdit" name="name_for_update">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>380</y>
      <width>191</width>
      <height>71</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>340</y>
      <width>421</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>выберите событие (введите только название)</string>
    </property>
   </widget>
   <widget class="QProgressBar" name="time_progress">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>580</y>
      <width>331</width>
      <height>23</height>
     </rect>
    </property>
    <property name="value">
     <number>0</number>
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
        self.alarm_list = []

        self.is_playing = False  # Флаг для отслеживания воспроизведения звука
        self.create_btn.clicked.connect(self.otvet)
        self.update_info_btn.clicked.connect(self.update_time_left)
        self.update_info_btn.clicked.connect(self.update_date_left)
        self.update_info_btn.clicked.connect(self.update_progress)

        self.timeEdit.setTime(QTime.currentTime())
        self.dateEdit.setDate(QDate.currentDate())


        # Настроим таймер для периодической проверки времени(частота - раз в секунду)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_time)
        self.timer.start(1000)  
    

    def otvet(self): 
        self.name = self.eventInfo.toPlainText()  # описание события
        f = 1
        for alarm in self.alarm_list:
            if self.name == alarm[0]:
                f = 0
                break
        if f and self.name:
            self.date = self.dateEdit.dateTime().toString('dd-MM-yyyy')  # дата события
            self.time = self.timeEdit.dateTime().toString('hh-mm')  # время события

            # Извлекаем компоненты даты и времени
            self.alarm_year = int(self.date[6:])
            self.alarm_month = int(self.date[3:5])
            self.alarm_day = int(self.date[0:2])
            self.alarm_hour = int(self.time[0:2])
            self.alarm_min = int(self.time[3:5])
            

            target_time = QTime.fromString(self.time, 'hh-mm')
            target_date = QDate.fromString(self.date, 'dd-MM-yyyy')
            current_datetime = QDateTime.currentDateTime()
            event_datetime = QDateTime(target_date, target_time)
            
            if current_datetime < event_datetime:
                self.diff = current_datetime.secsTo(event_datetime)
                self.alarm_list.append([self.name, self.date, self.time, False, self.diff])
                self.eventList.addItem(f"{self.name} {self.date} {self.time}")
            else:
                self.diff = -1
            

        
        
        
    def calculate_time_left(self, alarm_name):
        for alarm in self.alarm_list: # Перебирается список с будильниками 
            name = alarm[0]
            if name == alarm_name:
                target_date = alarm[1]
                target_time = alarm[2]
                

        target_time = QTime.fromString(target_time, 'hh-mm')
        target_date = QDate.fromString(target_date, 'dd-MM-yyyy')
        current_datetime = QDateTime.currentDateTime()
        event_datetime = QDateTime(target_date, target_time)
        
        if current_datetime < event_datetime:
            diff = current_datetime.secsTo(event_datetime) # Подсчет оставшегося вренмени
            
            diff %= 365 * 24 * 3600
            diff %= 30 * 24 * 3600
            diff %= 24 * 3600

            hours = diff // 3600
            diff %= 3600
            minutes = diff / 60
            if minutes > 1:
                minutes = int(minutes)
            elif minutes != 0 and minutes < 1 and minutes > 0:
                minutes = 1
            
            if 11 <= hours % 100 <= 14:  # Числа от 11 до 14
                word_hour = "часов"
            elif hours % 10 == 1:  # Число оканчивается на 1 (кроме 11)
                word_hour = "час"
            elif 2 <= hours % 10 <= 4:  # Число оканчивается на 2, 3 или 4 (кроме 12-14)
                word_hour = "часа"
            else:  # Все остальные случаи
                word_hour = "часов"

            if 11 <= minutes % 100 <= 14:  #аналогчино для минут
                word_minute = "минут"
            elif minutes % 10 == 1:  
                word_minute = "минута"
            elif 2 <= minutes % 10 <= 4:  
                word_minute = "минуты"
            else:  
                word_minute = "минут"

            return f"Осталось: {hours} {word_hour}, {minutes} {word_minute}"
        return f"Будильник прозвенел"
    

    def calculate_date_left(self, alarm_name): 
        for alarm in self.alarm_list:
            name = alarm[0]
            if name == alarm_name:
                target_date = alarm[1]
                target_time = alarm[2]
                

        target_time = QTime.fromString(target_time, 'hh-mm')
        target_date = QDate.fromString(target_date, 'dd-MM-yyyy')
        current_datetime = QDateTime.currentDateTime()
        event_datetime = QDateTime(target_date, target_time)
        
        if current_datetime < event_datetime:
            diff = current_datetime.secsTo(event_datetime)
            years = diff // (365 * 24 * 3600)
            diff %= 365 * 24 * 3600
            months = diff // (30 * 24 * 3600)
            diff %= 30 * 24 * 3600
            days = diff // (24 * 3600)

            if 11 <= years % 100 <= 14:  
                word_year = "лет"
            elif years % 10 == 1:  
                word_year = "год"
            elif 2 <= years % 10 <= 4:  
                word_year = "года"
            else:  
                word_year = "лет"
            
            if 11 <= months % 100 <= 14:  
                word_month = "месяцев"
            elif months % 10 == 1:  
                word_month = "месяц"
            elif 2 <= months % 10 <= 4:  
                word_month = "месяца"
            else:  
                word_month = "месяцев"
            
            if 11 <= days % 100 <= 14:  
                word_day = "дней"
            elif days % 10 == 1:  
                word_day = "день"
            elif 2 <= days % 10 <= 4:  
                word_day = "дня"
            else:  
                word_day = "дней"

            return f"Осталось: {years} {word_year}, {months} {word_month}, {days} {word_day}"
        return f"Будильник прозвенел"
        

    def update_time_left(self):
        f = 0
        alarm_name = self.name_for_update.toPlainText()
        for alarm in self.alarm_list:
            if alarm_name in alarm:
                f = 1
        if alarm_name and f:
            self.label_timeleft.setText(self.calculate_time_left(alarm_name))
    

    def update_date_left(self):
        f = 0
        alarm_name = self.name_for_update.toPlainText()
        for alarm in self.alarm_list:
            if alarm_name in alarm:
                f = 1
        if alarm_name and f:
            self.label_dateleft.setText(self.calculate_date_left(alarm_name))
    
    def calculate_time_left_seconds(self, alarm_name):
        for alarm in self.alarm_list:
            name = alarm[0]
            if name == alarm_name:
                target_date = alarm[1]
                target_time = alarm[2]
                
        if name:
            target_time = QTime.fromString(target_time, 'hh-mm')
            target_date = QDate.fromString(target_date, 'dd-MM-yyyy')
            current_datetime = QDateTime.currentDateTime()
            event_datetime = QDateTime(target_date, target_time)
            diff = current_datetime.secsTo(event_datetime)
            return diff

    def update_progress(self):
        f = 0
        alarm_name = self.name_for_update.toPlainText()
        for alarm in self.alarm_list:
            if alarm_name in alarm:
                f = 1

        alarm_name = self.name_for_update.toPlainText()
        for alarm in self.alarm_list: # Перебирается список с будильниками 
            name = alarm[0]
            if name == alarm_name:
                total_seconds = alarm[4]
        if alarm_name and f:        
            remaining_seconds = self.calculate_time_left_seconds(alarm_name)

            if total_seconds > 0:
                progress = ((total_seconds - remaining_seconds) / total_seconds) * 100
                self.time_progress.setValue(int(progress))
        else:
            self.label_dateleft.setText("Событие не найдено")
            self.label_timeleft.setText("Событие не найдено")
            self.time_progress.setValue(0)


    
    def check_time(self):
        for alarm in self.alarm_list:
            self.is_playing = alarm[3]
            target_date = alarm[1]
            target_time = alarm[2]

            self.alarm_year = int(target_date[6:])
            self.alarm_month = int(target_date[3:5])
            self.alarm_day = int(target_date[0:2])
            self.alarm_hour = int(target_time[0:2])
            self.alarm_min = int(target_time[3:5])

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
                not alarm[3] and alarm[4] != -1):
                    alarm[3] = True  # Устанавливаем флаг воспроизведения

                    if getattr(sys, 'frozen', False):  # Для PyInstaller
                        base_path = sys._MEIPASS
                    else:
                        base_path = os.path.dirname(os.path.abspath(__file__))

                    # Формируем корректный абсолютный путь к файлу
                    file_path = os.path.join(base_path, 'assets', 'GalarmMusic.mp3')
                    file_path = os.path.abspath(file_path)
                    threading.Thread(target=playsound, args=(file_path,)).start() 
                
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Project()
    ex.show()
    sys.exit(app.exec())
