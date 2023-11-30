import sys
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


        icon_size = QSize(40,40)  # Adjust the width and height as needed
        navbar.setIconSize(icon_size)

        # Set the stylesheet for the taskbar to make text white
        navbar.setStyleSheet("color: white;")

        button_width = 30  

        back_btn = QToolButton(self)
        back_btn.setText('Back')
        back_btn.setIcon(QIcon('back_icon.png'))  # Replace with your actual icon
        back_btn.clicked.connect(self.browser.back)
        back_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(back_btn)

        forward_btn = QToolButton(self)
        forward_btn.setText('Forward')
        forward_btn.setIcon(QIcon('forward_icon.png'))  # Replace with your actual icon
        forward_btn.clicked.connect(self.browser.forward)
        forward_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(forward_btn)


        reload_btn = QToolButton(self)
        reload_btn.setText('Reload')
        reload_btn.setIcon(QIcon('reload_icon.png'))  # Replace with your actual icon
        reload_btn.clicked.connect(self.browser.reload)
        reload_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(reload_btn)

        self.home_btn = QToolButton(self)
        self.home_btn.setText('Home')
        self.home_btn.setIcon(QIcon('home_icon.png'))  # Replace with your actual icon
        self.home_btn.clicked.connect(self.navigate_home)
        self.home_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(self.home_btn)


        light_btn = QToolButton(self)
        light_btn.setText('Home')
        light_btn.setIcon(QIcon('home_icon.png'))  # Replace with your actual icon
        light_btn.clicked.connect(lambda: self.light_mode(navbar))
        light_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(light_btn)

        bookmark_btn = QToolButton(self)
        bookmark_btn.setText('bookmark')
        bookmark_btn.setIcon(QIcon('back_icon.png'))  # Replace with your actual icon
        bookmark_btn.clicked.connect(self.set_visible)
        bookmark_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(bookmark_btn)



        self.bookmark_box_widget = QFrame(self)
        self.bookmark_box_widget.setGeometry(184, 22, 400, 600)
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

        settings_btn = QToolButton(self)
        settings_btn.setText('settings')
        settings_btn.setIcon(QIcon('back_icon.png'))  # Replace with your actual icon
        settings_btn.clicked.connect(self.set_settings_visible)
        settings_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(settings_btn)



        self.settings_widget = QFrame(self)
        self.settings_widget.setGeometry(184, 22, 400, 600)
        self.settings_widget.setFrameShape(QFrame.Box)
        self.settings_widget.setFrameShadow(QFrame.Raised)
        self.settings_widget.setLineWidth(2)
        self.settings_widget.setVisible(self.settings_box_visible)
        self.settings_widget.setStyleSheet("background-color: #404040; color: white;")
        self.settings_layout = QVBoxLayout(self.settings_widget)
        self.settings_widget.setLayout(self.settings_layout)

        self.show_home_btn_checkbox = QCheckBox('Enable Feature')
        self.settings_layout.addWidget(self.show_home_btn_checkbox)
        self.show_home_btn_checkbox.stateChanged.connect(self.some_method)

        self.home_btn.setVisible(not self.show_home_btn_checkbox.isChecked())



    def some_method(self):
        self.home_btn.setVisible(not self.show_home_btn_checkbox.isChecked())




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

    #def search_engine_select(self):
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
            self.mode="Light"
        elif self.mode == "Light":
            navbar.setStyleSheet("color: white;")
            self.setStyleSheet("background-color: black;")
            self.mode="Dark"
        

    def navigate_home(self):
        self.browser.setUrl(QUrl('https://zen-mauve.vercel.app/'))

    def navigate_to_url(self):
        url = self.url_bar.text()

        if "." in url:
            if "https://" in url or "http://" in url:
                self.browser.setUrl(QUrl(url))
            else:
                self.browser.setUrl(QUrl("https://" + url))
        else:
            temp = url.split(" ")
            url = "https://search."+self.search_engine+".com/search?q="
            for i in temp:
                url = url + "+" + i
            url = url + "&source=web"
            self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        url = q.toString()
        self.url_bar.setText(url)

app = QApplication(sys.argv)
QApplication.setApplicationName('My Cool Browser')
window = MainWindow()
# Set the background color of the taskbar to black
window.setStyleSheet("background-color: black;")
app.exec_()

