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

        navbar = QToolBar()
        self.addToolBar(navbar)

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

        home_btn = QToolButton(self)
        home_btn.setText('Home')
        home_btn.setIcon(QIcon('home_icon.png'))  # Replace with your actual icon
        home_btn.clicked.connect(self.navigate_home)
        home_btn.setFixedSize(button_width, button_width)
        navbar.addWidget(home_btn)

        # Create the bookmark button
        self.bookmark_btn = QAction('Bookmark', self)
        self.bookmark_btn.triggered.connect(self.toggle_bookmark_box)
        navbar.addAction(self.bookmark_btn)

        # Create the history button
        self.history_btn = QAction('History', self)
        self.history_btn.triggered.connect(self.toggle_history_box)
        navbar.addAction(self.history_btn)

        # Create the bookmark box widget
        self.bookmark_box_widget = QFrame(self)
        self.bookmark_box_widget.setGeometry(184, 22, 400, 600)
        self.bookmark_box_widget.setFrameShape(QFrame.Box)
        self.bookmark_box_widget.setFrameShadow(QFrame.Raised)
        self.bookmark_box_widget.setLineWidth(2)
        self.bookmark_box_widget.setVisible(self.box_visible)
        self.bookmark_box_widget.setStyleSheet("background-color: #404040; color: #872341;")

        # Create the bookmark list widget inside the bookmark box widget
        self.bookmark_list_widget = QListWidget(self.bookmark_box_widget)
        self.bookmark_list_widget.itemDoubleClicked.connect(self.load_item)

        # Set the stylesheet for the bookmark list items
        self.bookmark_list_widget.setStyleSheet("color: #F2F2F2;")

        # Create a layout for the bookmark box widget
        bookmark_layout = QVBoxLayout(self.bookmark_box_widget)
        bookmark_layout.addWidget(self.bookmark_list_widget)

        # Create the history box widget
        self.history_box_widget = QFrame(self)
        self.history_box_widget.setGeometry(184, 22, 400, 600)
        self.history_box_widget.setFrameShape(QFrame.Box)
        self.history_box_widget.setFrameShadow(QFrame.Raised)
        self.history_box_widget.setLineWidth(2)
        self.history_box_widget.setVisible(self.box_visible)
        self.history_box_widget.setStyleSheet("background-color: #353535; color: white;")

        # Create the history list widget inside the history box widget
        self.history_list_widget = QListWidget(self.history_box_widget)
        self.history_list_widget.itemDoubleClicked.connect(self.load_item)

        # Set the stylesheet for the history list items
        self.history_list_widget.setStyleSheet("color: white;")

        # Create a layout for the history box widget
        history_layout = QVBoxLayout(self.history_box_widget)
        history_layout.addWidget(self.history_list_widget)

        # Initialize the current box widget to None
        self.current_box_widget = None

        # Create the URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Connect the URL changed signal to the update_url method
        self.browser.urlChanged.connect(self.update_url)

        # Initialize the history list
        self.history = []

    def toggle_bookmark_box(self):
        self.toggle_box(self.bookmark_box_widget, self.bookmark_list_widget)

    def toggle_history_box(self):
        self.toggle_box(self.history_box_widget, self.history_list_widget)

    def toggle_box(self, box_widget, list_widget):
        self.box_visible = not self.box_visible

        if self.current_box_widget and self.current_box_widget != box_widget:
            self.current_box_widget.setVisible(False)

        box_widget.setVisible(self.box_visible)

        if self.box_visible:
            current_url = self.url_bar.text()
            self.add_item_to_list(list_widget, current_url)

        self.current_box_widget = box_widget

    def navigate_home(self):
        self.browser.setUrl(QUrl('https://zen-mauve.vercel.app/'))

    def add_item_to_list(self, list_widget, item):
        list_item = QListWidgetItem(item)
        list_widget.addItem(list_item)

    def load_item(self, item):
        url = item.text()
        self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))

    def navigate_to_url(self):
        url = self.url_bar.text()

        if "." in url:
            if "https://" in url or "http://" in url:
                self.browser.setUrl(QUrl(url))
            else:
                self.browser.setUrl(QUrl("https://" + url))
        else:
            temp = url.split(" ")
            url = "https://search.brave.com/search?q="
            for i in temp:
                url = url + "+" + i
            url = url + "&source=web"
            self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        url = q.toString()
        self.url_bar.setText(url)
        self.history.append(url)
        self.add_item_to_list(self.history_list_widget, url)

app = QApplication(sys.argv)
QApplication.setApplicationName('My Cool Browser')
window = MainWindow()
# Set the background color of the taskbar to black
window.setStyleSheet("background-color: black;")
app.exec_()
