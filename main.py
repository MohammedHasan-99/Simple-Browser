from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys
import validators

BROWSER_NAME = "My hacker Browser"
DEFAULT_URL = "http://google.com"
HOME_PAGE = "http://google.com"
BAR_SIZE = 40
URL_FONT = QFont("Times", 10, QFont.Bold)
BTN_FONT = QFont("Times", 10)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Web Engine
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(DEFAULT_URL))
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Navigation
        navbar = QToolBar("Navigation")
        navbar.setMovable(False)
        navbar.setFixedHeight(BAR_SIZE)
        self.addToolBar(navbar)

        # Back
        back_btn = QPushButton("Back", self)
        back_btn.setFixedHeight(BAR_SIZE - 5)
        back_btn.clicked.connect(self.back)
        back_btn.setFont(BTN_FONT)
        navbar.addWidget(back_btn)

        # Forward
        next_btn = QPushButton("Forward", self)
        next_btn.setFixedHeight(BAR_SIZE - 5)
        next_btn.clicked.connect(self.forward)
        next_btn.setFont(BTN_FONT)
        navbar.addWidget(next_btn)

        # Home
        home_btn = QPushButton("Home", self)
        home_btn.setFixedHeight(BAR_SIZE - 5)
        home_btn.clicked.connect(self.navigate_home)
        home_btn.setFont(BTN_FONT)
        navbar.addWidget(home_btn)

        # Reload
        reload_btn = QPushButton("Reload", self)
        reload_btn.setFixedHeight(BAR_SIZE - 5)
        reload_btn.clicked.connect(self.browser.reload)
        reload_btn.setFont(BTN_FONT)
        navbar.addWidget(reload_btn)

        # url bar
        navbar.addSeparator()
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setFixedHeight(BAR_SIZE - 5)
        self.url_bar.setFont(URL_FONT)
        navbar.addWidget(self.url_bar)
        navbar.addSeparator()

        # Stop
        stop_btn = QPushButton("Stop", self)
        stop_btn.setFixedHeight(BAR_SIZE - 5)
        stop_btn.clicked.connect(self.browser.stop)
        stop_btn.setFont(BTN_FONT)
        navbar.addWidget(stop_btn)

        # Bookmark
        navbar.addSeparator()
        bookmark_btn = QPushButton("Bookmark", self)
        bookmark_btn.setFixedHeight(BAR_SIZE - 5)
        bookmark_btn.clicked.connect(self.add_bookmark)
        bookmark_btn.setFont(BTN_FONT)
        navbar.addWidget(bookmark_btn)

        # Drop list for bookmarks
        self.cb = QComboBox()
        self.cb.setFixedHeight(BAR_SIZE - 5)
        self.cb.setFixedWidth(200)
        self.cb.addItem("")
        self.cb.setFont(BTN_FONT)
        self.cb.currentIndexChanged.connect(self.selection_change)
        navbar.addWidget(self.cb)

        # Bookmarks
        self.bookmarks = {"": ""}

        self.showMaximized()

    def update_title(self):
        self.statusBar.showMessage("Done loading...")
        page_title = self.browser.page().title()
        self.setWindowTitle(f"{BROWSER_NAME} - {page_title}")

    def navigate_home(self):
        self.statusBar.showMessage("Loading...")
        self.cb.setCurrentIndex(0)
        self.browser.setUrl(QUrl(HOME_PAGE))

    def navigate_to_url(self):
        self.statusBar.showMessage("Loading...")
        self.cb.setCurrentIndex(0)
        url = self.url_bar.text()
        q_url = QUrl(self.url_bar.text())
        if q_url.scheme() == "":
            q_url.setScheme("http")
            url = f"http://{url}"

        if validators.url(url):
            self.browser.setUrl(q_url)
        else:
            self.browser.setUrl(QUrl(f"http://www.google.com/search?q={self.url_bar.text()}"))

    def update_url_bar(self, url):
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)

    def selection_change(self):
        url = self.bookmarks[self.cb.currentText()]
        if url != "":
            self.statusBar.showMessage("Loading...")
            self.browser.setUrl(QUrl(url))

    def add_bookmark(self):
        page_title = self.browser.page().title()
        if page_title != "":
            if page_title not in self.bookmarks:
                self.bookmarks[page_title] = self.url_bar.text()
                self.cb.insertItem(self.cb.count(), page_title)
                self.cb.setCurrentIndex(self.cb.count() - 1)

    def back(self):
        self.cb.setCurrentIndex(0)
        self.browser.back()

    def forward(self):
        self.cb.setCurrentIndex(0)
        self.browser.forward()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(BROWSER_NAME)
    window = MainWindow()
    app.exec_()


if __name__ == '__main__':
    main()
