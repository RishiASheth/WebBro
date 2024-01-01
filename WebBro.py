# Dear programmer:
# when i wrote this code,
# only god and i knew how it worked.
# Now, only god knows it!
#
# Therefore, if you are trying to optimize this routine
# and it fails ( most surely ),
# please increase this counter as a
# warning for the next person:
#
# total_hours_wasted_here = 69

import time
import sys
import requests
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://zen-mauve.vercel.app/'))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.box_visible = False
        self.settings_box_visible = False
        self.mode = "Dark"
        navbar = QToolBar()
        self.addToolBar(navbar)
        self.l1 = []
        self.search_engine = "brave"
        self.history = []
        self.history_box_visible = False
        self.password_box_visible = False
        self.passwords={}
        self.home_btn_url="https://zen-mauve.vercel.app/"
        self.timer = QTimer()

        icon_size = QSize(18, 18)  # Adjust the width and height as needed
        navbar.setIconSize(icon_size)

        # Set the stylesheet for the taskbar to make text white
        navbar.setStyleSheet("color: white;")

        button_width = 35


        self.back_btn = QToolButton(self)
        self.back_btn.setText('Back')
        self.back_btn.setIcon(QIcon('back_btn_white.png'))  # Replace with your actual icon
        self.back_btn.clicked.connect(self.browser.back)
        self.back_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(self.back_btn)

        self.forward_btn = QToolButton(self)
        self.forward_btn.setText('Forward')
        self.forward_btn.setIcon(QIcon('forward_btn_white.png'))  # Replace with your actual icon
        self.forward_btn.clicked.connect(self.browser.forward)
        self.forward_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(self.forward_btn)

        self.reload_btn = QToolButton(self)
        self.reload_btn.setText('Reload')
        self.reload_btn.setIcon(QIcon('reload_btn_white.png'))  # Replace with your actual icon
        self.reload_btn.clicked.connect(self.browser.reload)
        self.reload_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(self.reload_btn)

        self.home_btn = QToolButton(self)
        self.home_btn.setText('Home')
        self.home_btn.setIcon(QIcon('home_btn_white.png'))  # Replace with your actual icon
        self.home_btn.clicked.connect(self.navigate_home)
        self.home_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(self.home_btn)

        self.light_btn = QToolButton(self)
        self.light_btn.setText('Home')
        self.light_btn.setIcon(QIcon('light_btn_white.png'))  # Replace with your actual icon
        self.light_btn.clicked.connect(lambda: self.light_mode(navbar))
        self.light_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(self.light_btn)

        self.bookmark_btn = QToolButton(self)
        self.bookmark_btn.setText('bookmark')
        self.bookmark_btn.setIcon(QIcon('bookmark_btn_white.png'))  # Replace with your actual icon
        self.bookmark_btn.clicked.connect(self.set_visible)
        self.bookmark_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(self.bookmark_btn)

        self.bookmark_box_widget = QFrame(self)
        self.bookmark_box_widget.setGeometry(199, 32, 330, 500)
        self.bookmark_box_widget.setFrameShape(QFrame.Box)
        self.bookmark_box_widget.setFrameShadow(QFrame.Raised)
        self.bookmark_box_widget.setLineWidth(2)
        self.bookmark_box_widget.setVisible(self.box_visible)
        self.bookmark_box_widget.setStyleSheet("background-color: #404040; color: white;")
        self.bookmark_box_layout = QVBoxLayout(self.bookmark_box_widget)
        self.bookmark_box_widget.setLayout(self.bookmark_box_layout)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        self.history_btn = QToolButton(self)
        self.history_btn.setText('History')
        self.history_btn.setIcon(QIcon('history_btn_white.png'))  #Replace with whatever history icon you want
        self.history_btn.clicked.connect(self.show_history)
        self.history_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(self.history_btn)

        self.history_box_widget = QFrame(self)
        self.history_box_widget.setGeometry(800, 32, 330, 500)
        self.history_box_widget.setFrameShape(QFrame.Box)
        self.history_box_widget.setFrameShadow(QFrame.Raised)
        self.history_box_widget.setLineWidth(2)
        self.history_box_widget.setVisible(self.history_box_visible)
        self.history_box_widget.setStyleSheet("background-color: #404040; color: white;")
        self.history_box_layout = QVBoxLayout(self.history_box_widget)
        self.history_box_widget.setLayout(self.history_box_layout)

        #    self.search_engine_bar = QLineEdit()
        #    self.search_engine_bar.setPlaceholderText("Enter the search engine you want to use ex - google ")
        #    self.search_engine_bar.returnPressed.connect(self.search_engine_select)
        #    navbar.addWidget(self.search_engine_bar)

        combo_box = QComboBox()
        combo_box.addItem('brave')
        combo_box.addItem('bing')
        combo_box.addItem('google')
        combo_box.addItem('yahoo')
        combo_box.activated.connect(self.on_combobox_activated)
        navbar.addWidget(combo_box)

        new_window_btn = QToolButton(self)
        new_window_btn.setText('New Window')
        new_window_btn.clicked.connect(self.open_new_window)
        navbar.addWidget(new_window_btn)

        self.password_btn = QToolButton(self)
        self.password_btn.setText('Password Manager')
        self.password_btn.setIcon(QIcon('password_btn_white.png'))  # Replace with your actual icon
        self.password_btn.clicked.connect(self.password_set_visible)
        self.password_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(self.password_btn)

        self.password_box_widget = QFrame(self)
        self.password_box_widget.setGeometry(1014, 32, 300, 400)
        self.password_box_widget.setFrameShape(QFrame.Box)
        self.password_box_widget.setFrameShadow(QFrame.Raised)
        self.password_box_widget.setLineWidth(2)
        self.password_box_widget.setVisible(self.password_box_visible)
        self.password_box_widget.setStyleSheet("background-color: #404040; color: white;")
        self.password_box_layout = QVBoxLayout(self.password_box_widget)
        self.password_box_widget.setLayout(self.password_box_layout)

        self.username_bar = QLineEdit()
        self.password_bar = QLineEdit()
        self.username_bar.setText("Username:   ")
        self.password_bar.setText("Password:   ")
        


        self.settings_btn = QToolButton(self)
        self.settings_btn.setText('settings')
        self.settings_btn.setIcon(QIcon('settings_btn_white.png'))  # Replace with your actual icon
        self.settings_btn.clicked.connect(self.set_settings_visible)
        self.settings_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(self.settings_btn)

        self.settings_widget = QFrame(self)
        self.settings_widget.setGeometry(1150, 32, 200, 400)
        self.settings_widget.setFrameShape(QFrame.Box)
        self.settings_widget.setFrameShadow(QFrame.Raised)
        self.settings_widget.setLineWidth(2)
        self.settings_widget.setVisible(self.settings_box_visible)
        self.settings_widget.setStyleSheet("background-color: #404040; color: white;")
        self.settings_layout = QVBoxLayout(self.settings_widget)
        self.settings_widget.setLayout(self.settings_layout)

        self.setting_new_window = QToolButton(self)
        self.setting_new_window.setText('open new window')
        self.setting_new_window.clicked.connect(self.open_new_window)
        self.setting_new_window.setFixedSize(100,32)
        self.settings_layout.addWidget(self.setting_new_window)

        self.home_bar = QLineEdit()
        self.home_bar.setPlaceholderText("Enter Home address:")
        self.home_bar.returnPressed.connect(self.assign_home_url)
        self.settings_layout.insertWidget(0,self.home_bar)

        self.setting_show_bookmark = QToolButton(self)
        self.setting_show_bookmark.setText('show Bookmarks')
        self.setting_show_bookmark.clicked.connect(self.set_visible)
        self.setting_show_bookmark.setFixedSize(100,32)
        self.settings_layout.addWidget(self.setting_show_bookmark)

        self.setting_show_history = QToolButton(self)
        self.setting_show_history.setText('show History')
        self.setting_show_history.clicked.connect(self.show_history)
        self.setting_show_history.setFixedSize(100,32)
        self.settings_layout.addWidget(self.setting_show_history)

        self.setting_show_password = QToolButton(self)
        self.setting_show_password.setText('Manage passwords')
        self.setting_show_password.clicked.connect(self.password_set_visible)
        self.setting_show_password.setFixedSize(100,32)
        self.settings_layout.addWidget(self.setting_show_password)


        self.self_destruct_btn = QToolButton(self)
        self.self_destruct_btn.setText('Self Destruct')
        self.self_destruct_btn.clicked.connect(self.self_destruct_start)
        self.self_destruct_btn.setFixedSize(100,32)
        self.settings_layout.addWidget(self.self_destruct_btn)

        

        


        self.show_home_btn_checkbox = QCheckBox('Show home Button')
        self.settings_layout.insertWidget(1,self.show_home_btn_checkbox)
        # self.show_home_btn_checkbox.stateChanged.connect(lambda state: self.disappear(self.home_btn,state))
        self.show_home_btn_checkbox.stateChanged.connect(lambda state: self.disappear_home(state))


    def self_destruct_start(self):
        self.timer.timeout.connect(self.self_destruct_end)
        self.browser.setUrl(QUrl("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDBpYjgyaXQ1a2p1dncxc2xiaTBldjVzdGhmMWlraDFsbWpkYnR6ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TNwX48Ear64uWmN7t3/giphy.gif"))
        self.timer.start(4000)

    def self_destruct_end(self):
        self.timer.stop()
        self.app.quit()


        

    def url_ok(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
        try:
            response = requests.get(url,headers=headers)
            response.raise_for_status()
            return True
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return False
        except requests.RequestException as e:
            print(f"Error: {e}")
            return False


    def assign_home_url(self):
        self.home_btn_url=self.valid_url(self.home_bar.text())
        

    def password_set_visible(self):
        self.password_box_visible = not self.password_box_visible
        self.passwords.update({self.username_bar.text(): self.password_bar.text()})
        while self.password_box_layout.count():
            item = self.password_box_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        self.password_box_layout.insertWidget(0, self.username_bar)
        self.password_box_layout.insertWidget(1, self.password_bar)
        for key, value in self.passwords.items():
            label_text = f"{key}: {value} "
            label = QLabel(label_text, self)
            self.password_box_layout.addWidget(label)

        self.password_box_widget.setVisible(self.password_box_visible)


    def disappear_home(self,state):
        if state==2:
            if self.mode=="Dark":
                self.home_btn.setIcon(QIcon('home_btn_black.png'))
            else:
                self.home_btn.setIcon(QIcon('home_btn_white.png'))
        else:
            if self.mode=="Dark":
                self.home_btn.setIcon(QIcon('home_btn_white.png'))
            else:
                self.home_btn.setIcon(QIcon('home_btn_black.png'))
        
        #     if self.mode == "Dark":
        #         button_text = name.text()  # Assuming name is a QPushButton or similar widget
        #         filename = button_text + '_black.png'
        #         name.setIcon(QIcon(filename))
        #     elif self.mode == "Light":
        #         button_text = name.text()
        #         filename = button_text + '_white.png'
        #         name.setIcon(QIcon(filename))
        # else:
        #     if self.mode == "Dark":
        #         button_text = name.text()  # Assuming name is a QPushButton or similar widget
        #         filename = button_text + '_white.png'
        #         name.setIcon(QIcon(filename))
        #     elif self.mode == "Light":
        #         button_text = name.text()
        #         filename = button_text + '_black.png'
        #         name.setIcon(QIcon(filename))

        

    def set_settings_visible(self):
        self.settings_box_visible = not self.settings_box_visible


        self.settings_widget.setVisible(self.settings_box_visible)

    def open_new_window(self):
        new_window = MainWindow()
        new_window.show()

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.exec_()

    def on_combobox_activated(self):
        self.search_engine = self.sender().currentText()

    # def search_engine_select(self):
    #   self.search_engine =  self.search_engine_bar.text()

    def set_visible(self):
        self.box_visible = not self.box_visible
        if self.box_visible:
            current_url = self.url_bar.text()
            if current_url not in self.l1:
                self.l1.append(current_url)
                label = QLabel(current_url)
                self.bookmark_box_layout.addWidget(label)
        self.bookmark_box_widget.setVisible(self.box_visible)

    def light_mode(self, navbar):
        if self.mode == "Dark":
            navbar.setStyleSheet("color: black;")
            self.setStyleSheet("background-color: white;")
            self.back_btn.setIcon(QIcon('back_btn_black.png'))
            self.home_btn.setIcon(QIcon('home_btn_black.png'))
            self.forward_btn.setIcon(QIcon('forward_btn_black.png'))
            self.reload_btn.setIcon(QIcon('reload_btn_black.png'))  
            self.bookmark_btn.setIcon(QIcon('bookmark_btn_black.png'))  
            self.history_btn.setIcon(QIcon('history_btn_black.png'))  
            self.password_btn.setIcon(QIcon('password_btn_black.png'))  
            self.light_btn.setIcon(QIcon('light_btn_black.png'))  
            self.settings_btn.setIcon(QIcon('settings_btn_black.png'))  
            self.mode = "Light"
        elif self.mode == "Light":
            navbar.setStyleSheet("color: white;")
            self.setStyleSheet("background-color: black;")
            self.back_btn.setIcon(QIcon('back_btn_white.png'))
            self.home_btn.setIcon(QIcon('home_btn_white.png'))
            self.forward_btn.setIcon(QIcon('forward_btn_white.png'))
            self.reload_btn.setIcon(QIcon('reload_btn_white.png'))  
            self.bookmark_btn.setIcon(QIcon('bookmark_btn_white.png'))  
            self.history_btn.setIcon(QIcon('history_btn_white.png'))  
            self.password_btn.setIcon(QIcon('password_btn_white.png'))  
            self.light_btn.setIcon(QIcon('light_btn_white.png'))  
            self.settings_btn.setIcon(QIcon('settings_btn_white.png'))
            self.mode = "Dark"

    def navigate_home(self):
        self.browser.setUrl(QUrl(self.home_btn_url))

    def navigate_to_url(self):
        self.url = self.url_bar.text()
        self.url=self.valid_url(self.url)
        self.browser.setUrl(QUrl(self.url))

    def error_alert(self):
        # Creating a QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Invaid Website")
        msg.setWindowTitle("Moye-Moye")
        msg.setStandardButtons(QMessageBox.Ok)
        result = msg.exec_()

    
    def valid_url(self,url):
        if "." in url:
            if "https://" in url or "http://" in url:
                if self.url_ok(url):
                    return url
                else:
                    self.error_alert()
            else:
                url="https://"+url
                if self.url_ok(url):
                    return url
                else:
                    self.error_alert()
        else:
            temp = url.split(" ")
            url = "https://search." + self.search_engine + ".com/search?q="
            for i in temp:
                url = url + "+" + i
            url = url + "&source=web"
        return url
        

    def update_url(self, q):
        self.url = q.toString()
        self.url_bar.setText(self.url)
        self.history.append(self.url)


        

    # def show_history(self):
    #     self.settings_box_visible = not self.settings_box_visible
    #     history_text = "\n".join(self.history)
    #     msg_box = QMessageBox()
    #     msg_box.setText(history_text)
    #     msg_box.setStyleSheet("QMessageBox { background-color: lightblue; } QLabel { color: darkblue; }")
    #     msg_box.setWindowTitle("Browsing History")
    #     msg_box.exec_()
    #     self.history_box_widget.setVisible(self.history_box_visible)

    def show_history(self):
        self.history_box_visible = not self.history_box_visible
        history_text = "\n".join(self.history)

        while self.history_box_layout.count():
            item = self.history_box_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        # for item in range(0,len(self.history),2):
        #     label = QLabel(self.history[item], self)
        #     self.history_box_layout.addWidget(label)
        for item in self.history:
             label = QLabel(item, self)
             self.history_box_layout.addWidget(label)
        self.history_box_widget.setVisible(self.history_box_visible)




app = QApplication(sys.argv)
QApplication.setApplicationName('WebBro')
window = MainWindow()
# Set the background color of the taskbar to black
window.setStyleSheet("background-color: black;")
app.exec_()
