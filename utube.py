"""
YouTube Lite
============

A lightweight, privacy-focused YouTube desktop client.

Features:
    - YouTube-only browsing
    - YouTube search
    - Multiple tabs
    - Back / forward / reload
    - YouTube home
    - Network-level ad/tracker blocking
    - YouTube player ad detection
    - Automatic Skip Ad handling
    - Ad overlay removal
    - No watch history
    - No search history
    - No bookmarks
    - No favorites
    - No Watch Later
    - No JSON/config files
    - No persistent cookies
    - No persistent HTTP cache
    - No application browsing logs
    - Off-the-record WebEngine profile
    - Dark / light theme
    - Keyboard shortcuts
    - External non-YouTube navigation blocked

Install:
    pip install PyQt5 PyQtWebEngine

Run:
    python youtube_lite.py
"""

import sys
from urllib.parse import quote_plus, urlparse

from PyQt5.QtCore import (
    QSize,
    Qt,
    QUrl,
)

from PyQt5.QtGui import (
    QColor,
    QIcon,
    QKeySequence,
    QPainter,
    QPen,
    QPixmap,
)

from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QShortcut,
    QTabWidget,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QMenu,
)

from PyQt5.QtWebEngineCore import (
    QWebEngineUrlRequestInterceptor,
)

from PyQt5.QtWebEngineWidgets import (
    QWebEnginePage,
    QWebEngineProfile,
    QWebEngineScript,
    QWebEngineView,
)


# ============================================================
# APPLICATION
# ============================================================

APP_NAME = "YouTube Lite"
APP_VERSION = "2.1.0"


# ============================================================
# THEMES
# ============================================================

THEMES = {
    "dark": {
        "window": "#0f0f0f",
        "surface": "#181818",
        "surface2": "#212121",
        "hover": "#272727",
        "pressed": "#303030",
        "border": "#303030",
        "text": "#f1f1f1",
        "muted": "#aaaaaa",
        "accent": "#ff0033",
        "input": "#121212",
    },

    "light": {
        "window": "#ffffff",
        "surface": "#f8f8f8",
        "surface2": "#eeeeee",
        "hover": "#e5e5e5",
        "pressed": "#d9d9d9",
        "border": "#d5d5d5",
        "text": "#0f0f0f",
        "muted": "#606060",
        "accent": "#ff0033",
        "input": "#f2f2f2",
    },
}


# ============================================================
# STYLESHEET
# ============================================================

def build_stylesheet(theme):

    t = THEMES[theme]

    return f"""
    QWidget {{
        background-color: {t["window"]};
        color: {t["text"]};
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 13px;
    }}

    QMainWindow {{
        background-color: {t["window"]};
    }}

    QToolBar {{
        background-color: {t["surface"]};
        border: none;
        spacing: 4px;
        padding: 6px;
    }}

    QToolButton {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 7px;
        color: {t["text"]};
    }}

    QToolButton:hover {{
        background-color: {t["hover"]};
    }}

    QToolButton:pressed {{
        background-color: {t["pressed"]};
    }}

    QLineEdit {{
        background-color: {t["input"]};
        color: {t["text"]};
        border: 1px solid {t["border"]};
        border-radius: 18px;
        padding: 8px 14px;
        selection-background-color: {t["accent"]};
    }}

    QLineEdit:focus {{
        border-color: {t["muted"]};
    }}

    QTabWidget::pane {{
        border: none;
    }}

    QTabBar {{
        background-color: {t["surface"]};
    }}

    QTabBar::tab {{
        background-color: transparent;
        color: {t["muted"]};
        padding: 9px 14px;
        margin: 3px 2px 0 2px;
        border-radius: 8px 8px 0 0;
        min-width: 120px;
    }}

    QTabBar::tab:hover {{
        background-color: {t["hover"]};
    }}

    QTabBar::tab:selected {{
        background-color: {t["window"]};
        color: {t["text"]};
    }}

    QMenu {{
        background-color: {t["surface"]};
        color: {t["text"]};
        border: 1px solid {t["border"]};
        padding: 5px;
    }}

    QMenu::item {{
        padding: 8px 24px;
        border-radius: 5px;
    }}

    QMenu::item:selected {{
        background-color: {t["hover"]};
    }}

    QLabel#logo {{
        color: {t["accent"]};
        font-size: 16px;
        font-weight: 700;
    }}
    """


# ============================================================
# ICONS
# ============================================================

class Icons:

    @staticmethod
    def icon(name, color="#aaaaaa", size=18):

        pixmap = QPixmap(
            size * 2,
            size * 2,
        )

        pixmap.fill(
            Qt.transparent
        )

        pixmap.setDevicePixelRatio(2)

        painter = QPainter(pixmap)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        pen = QPen(
            QColor(color)
        )

        pen.setWidthF(1.8)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        painter.setPen(pen)

        w = size
        h = size

        if name == "back":

            painter.drawLine(
                int(w * .65),
                int(h * .20),
                int(w * .30),
                int(h * .50),
            )

            painter.drawLine(
                int(w * .30),
                int(h * .50),
                int(w * .65),
                int(h * .80),
            )

        elif name == "forward":

            painter.drawLine(
                int(w * .35),
                int(h * .20),
                int(w * .70),
                int(h * .50),
            )

            painter.drawLine(
                int(w * .70),
                int(h * .50),
                int(w * .35),
                int(h * .80),
            )

        elif name == "reload":

            painter.drawArc(
                int(w * .18),
                int(h * .18),
                int(w * .64),
                int(h * .64),
                45 * 16,
                290 * 16,
            )

            painter.drawLine(
                int(w * .72),
                int(h * .18),
                int(w * .72),
                int(h * .38),
            )

            painter.drawLine(
                int(w * .72),
                int(h * .18),
                int(w * .54),
                int(h * .24),
            )

        elif name == "home":

            painter.drawLine(
                int(w * .15),
                int(h * .48),
                int(w * .50),
                int(h * .18),
            )

            painter.drawLine(
                int(w * .50),
                int(h * .18),
                int(w * .85),
                int(h * .48),
            )

            painter.drawLine(
                int(w * .25),
                int(h * .42),
                int(w * .25),
                int(h * .82),
            )

            painter.drawLine(
                int(w * .25),
                int(h * .82),
                int(w * .75),
                int(h * .82),
            )

            painter.drawLine(
                int(w * .75),
                int(h * .82),
                int(w * .75),
                int(h * .42),
            )

        elif name == "search":

            painter.drawEllipse(
                int(w * .16),
                int(h * .16),
                int(w * .48),
                int(h * .48),
            )

            painter.drawLine(
                int(w * .58),
                int(h * .58),
                int(w * .84),
                int(h * .84),
            )

        elif name == "plus":

            painter.drawLine(
                int(w * .50),
                int(h * .20),
                int(w * .50),
                int(h * .80),
            )

            painter.drawLine(
                int(w * .20),
                int(h * .50),
                int(w * .80),
                int(h * .50),
            )

        elif name == "menu":

            for y in (.25, .50, .75):

                painter.drawLine(
                    int(w * .20),
                    int(h * y),
                    int(w * .80),
                    int(h * y),
                )

        painter.end()

        return QIcon(pixmap)


# ============================================================
# TOOL BUTTON
# ============================================================

class ToolButton(QToolButton):

    def __init__(
        self,
        icon_name,
        tooltip,
        parent=None,
    ):

        super().__init__(parent)

        self.setIcon(
            Icons.icon(
                icon_name
            )
        )

        self.setIconSize(
            QSize(19, 19)
        )

        self.setToolTip(
            tooltip
        )

        self.setCursor(
            Qt.PointingHandCursor
        )

        self.setFixedSize(
            34,
            34,
        )


# ============================================================
# YOUTUBE URL HELPERS
# ============================================================

YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
    "www.youtu.be",
}


def is_youtube_url(url):

    try:

        value = str(url).strip()

        if not value:
            return False

        if "://" not in value:

            value = (
                "https://"
                + value
            )

        parsed = urlparse(value)

        host = (
            parsed.hostname
            or ""
        ).lower().rstrip(".")

        return (
            host in YOUTUBE_HOSTS
            or host.endswith(
                ".youtube.com"
            )
        )

    except Exception:

        return False


def youtube_search_url(query):

    return (
        "https://www.youtube.com/results?search_query="
        + quote_plus(
            query.strip()
        )
    )


def normalize_youtube_url(value):

    value = str(value).strip()

    if not value:

        return QUrl(
            "https://www.youtube.com/"
        )

    if " " in value:

        return QUrl(
            youtube_search_url(
                value
            )
        )

    if value.startswith(
        (
            "http://",
            "https://",
        )
    ):

        if is_youtube_url(value):

            return QUrl(value)

        return QUrl(
            "https://www.youtube.com/"
        )

    if value.startswith(
        "youtu.be/"
    ):

        return QUrl(
            "https://"
            + value
        )

    if value.startswith(
        "youtube.com"
    ):

        return QUrl(
            "https://www."
            + value
        )

    if "." not in value:

        return QUrl(
            youtube_search_url(
                value
            )
        )

    return QUrl(
        "https://www.youtube.com/"
    )


# ============================================================
# NETWORK AD BLOCKER
# ============================================================

class YouTubeAdBlocker(
    QWebEngineUrlRequestInterceptor
):

    BLOCKED_DOMAINS = {
        "doubleclick.net",
        "googleadservices.com",
        "googlesyndication.com",
        "google-analytics.com",
        "googletagmanager.com",

        "adnxs.com",
        "adsrvr.org",
        "advertising.com",
        "amazon-adsystem.com",
        "scorecardresearch.com",
        "quantserve.com",
        "rubiconproject.com",
        "pubmatic.com",
        "openx.net",
        "criteo.com",
        "taboola.com",
        "outbrain.com",

        "hotjar.com",
        "mixpanel.com",
        "segment.com",
        "segment.io",
        "clarity.ms",
    }

    BLOCKED_PATHS = (
        "/pagead/",
        "/pagead2/",
        "/adservice/",
        "/adsystem/",
        "/ad_status",
        "/ptracking",
        "/pageadview",
    )

    def __init__(self):

        super().__init__()

        self.blocked_count = 0

    def interceptRequest(
        self,
        info,
    ):

        url = info.requestUrl()

        host = (
            url.host()
            .lower()
            .rstrip(".")
        )

        path = (
            url.path()
            .lower()
        )

        # Block known advertising domains.
        if any(
            host == domain
            or host.endswith(
                "." + domain
            )
            for domain
            in self.BLOCKED_DOMAINS
        ):

            info.block(True)

            self.blocked_count += 1

            return

        # Block known advertising paths.
        if any(
            blocked in path
            for blocked
            in self.BLOCKED_PATHS
        ):

            info.block(True)

            self.blocked_count += 1


# ============================================================
# YOUTUBE AD-BLOCKING JAVASCRIPT
# ============================================================

YOUTUBE_AD_SCRIPT = r"""
(() => {

    if (window.__youtubeLiteAdBlockerInstalled) {
        return;
    }

    window.__youtubeLiteAdBlockerInstalled = true;

    const removeElement = (element) => {
        try {
            if (element && element.remove) {
                element.remove();
            }
        } catch (_) {}
    };

    const clickIfPresent = (selectors) => {

        for (const selector of selectors) {

            const elements =
                document.querySelectorAll(selector);

            for (const element of elements) {

                try {

                    if (
                        element.offsetParent !== null ||
                        element.getClientRects().length
                    ) {

                        element.click();

                        return true;
                    }

                } catch (_) {}
            }
        }

        return false;
    };

    const removeAdElements = () => {

        const selectors = [

            // Player advertisements
            ".ytp-ad-module",
            ".ytp-ad-overlay-container",
            ".ytp-ad-overlay-slot",
            ".ytp-ad-player-overlay",
            ".ytp-ad-image-overlay",
            ".ytp-ad-text-overlay",

            // Homepage/search ads
            "ytd-display-ad-renderer",
            "ytd-promoted-sparkles-web-renderer",
            "ytd-ad-slot-renderer",
            "ytd-in-feed-ad-layout-renderer",

            // Shorts advertisements
            "ytd-ad-slot-renderer",

            // Other known containers
            ".ytd-display-ad-renderer",
            ".ytd-promoted-sparkles-web-renderer"
        ];

        for (const selector of selectors) {

            try {

                document
                    .querySelectorAll(selector)
                    .forEach(removeElement);

            } catch (_) {}
        }
    };


    const handleVideoAd = () => {

        const player =
            document.querySelector(".html5-video-player");

        if (!player) {
            return;
        }

        const isAd =
            player.classList.contains("ad-showing") ||
            player.classList.contains("ad-interrupting");

        if (!isAd) {
            return;
        }

        // Try YouTube's own skip button first.
        clickIfPresent([
            ".ytp-ad-skip-button",
            ".ytp-ad-skip-button-modern",
            ".ytp-skip-ad-button",
            "button.ytp-ad-skip-button-modern"
        ]);

        // Try to finish the ad video.
        const video =
            player.querySelector("video");

        if (video) {

            try {

                if (
                    Number.isFinite(video.duration) &&
                    video.duration > 0
                ) {

                    video.currentTime =
                        video.duration;
                }

            } catch (_) {}
        }

        // Remove overlay elements.
        removeAdElements();
    };


    const clean = () => {

        removeAdElements();

        handleVideoAd();
    };


    // Run immediately.
    clean();


    // YouTube is a SPA and constantly changes its DOM.
    const observer =
        new MutationObserver(() => {
            clean();
        });


    const startObserver = () => {

        if (!document.documentElement) {
            return;
        }

        observer.observe(
            document.documentElement,
            {
                childList: true,
                subtree: true
            }
        );
    };


    startObserver();


    // Periodic fallback for player state changes.
    setInterval(
        clean,
        250
    );

})();
"""


# ============================================================
# WEB PAGE
# ============================================================

class YouTubePage(QWebEnginePage):

    def __init__(
        self,
        browser,
        profile,
        parent=None,
    ):

        super().__init__(
            profile,
            parent,
        )

        self.browser = browser

    def acceptNavigationRequest(
        self,
        url,
        navigation_type,
        is_main_frame,
    ):

        target = url.toString()

        if (
            is_main_frame
            and not is_youtube_url(target)
        ):

            self.browser.show_status(
                "Navigation outside YouTube blocked"
            )

            return False

        return super().acceptNavigationRequest(
            url,
            navigation_type,
            is_main_frame,
        )


# ============================================================
# YOUTUBE TAB
# ============================================================

class YouTubeTab(QWidget):

    def __init__(
        self,
        browser,
    ):

        super().__init__()

        self.browser = browser

        self.view = QWebEngineView(
            self
        )

        self.page = YouTubePage(
            browser,
            browser.web_profile,
            self.view,
        )

        self.view.setPage(
            self.page
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.addWidget(
            self.view
        )

        self.view.titleChanged.connect(
            self.title_changed
        )

        self.view.urlChanged.connect(
            self.url_changed
        )

        self.view.loadFinished.connect(
            self.load_finished
        )

    def navigate(
        self,
        url,
    ):

        self.view.setUrl(
            normalize_youtube_url(
                url
            )
        )

    def title_changed(
        self,
        title,
    ):

        index = (
            self.browser.tabs.indexOf(
                self
            )
        )

        if index < 0:
            return

        title = title.strip()

        self.browser.tabs.setTabText(
            index,
            (
                title[:30]
                if title
                else "YouTube"
            ),
        )

    def url_changed(
        self,
        url,
    ):

        if (
            self.browser.current_tab()
            is self
        ):

            self.browser.address_bar.setText(
                url.toString()
            )

    def load_finished(
        self,
        success,
    ):

        if not success:

            self.browser.show_status(
                "Page failed to load"
            )

            return

        self.browser.show_status(
            "YouTube • Ad blocker active • No local history"
        )


# ============================================================
# MAIN WINDOW
# ============================================================

class YouTubeLite(QMainWindow):

    def __init__(self):

        super().__init__()

        # ----------------------------------------------------
        # OFF-THE-RECORD PROFILE
        # ----------------------------------------------------
        #
        # Creating QWebEngineProfile without a storage name
        # creates an off-the-record profile.
        #
        # Nothing is intentionally persisted by the app.
        # ----------------------------------------------------

        self.web_profile = QWebEngineProfile(
            self
        )

        self.web_profile.setPersistentCookiesPolicy(
            QWebEngineProfile.NoPersistentCookies
        )

        self.web_profile.setHttpCacheType(
            QWebEngineProfile.NoCache
        )

        # ----------------------------------------------------
        # NETWORK BLOCKER
        # ----------------------------------------------------

        self.ad_blocker = YouTubeAdBlocker()

        self.web_profile.setUrlRequestInterceptor(
            self.ad_blocker
        )

        # ----------------------------------------------------
        # GLOBAL YOUTUBE SCRIPT
        # ----------------------------------------------------

        script = QWebEngineScript()

        script.setName(
            "YouTubeLiteAdBlocker"
        )

        script.setSourceCode(
            YOUTUBE_AD_SCRIPT
        )

        script.setInjectionPoint(
            QWebEngineScript.DocumentReady
        )

        script.setWorldId(
            QWebEngineScript.MainWorld
        )

        script.setRunsOnSubFrames(
            True
        )

        self.web_profile.scripts().insert(
            script
        )

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.current_theme = "dark"

        self.setWindowTitle(
            APP_NAME
        )

        self.resize(
            1400,
            850,
        )

        self.build_ui()
        self.setup_shortcuts()

        self.new_tab()

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        toolbar = QToolBar()

        toolbar.setMovable(False)
        toolbar.setFloatable(False)

        self.addToolBar(
            toolbar
        )

        logo = QLabel(
            "▶  YouTube Lite"
        )

        logo.setObjectName(
            "logo"
        )

        logo.setMinimumWidth(
            145
        )

        toolbar.addWidget(
            logo
        )

        # ----------------------------------------------------
        # Navigation
        # ----------------------------------------------------

        self.back_button = ToolButton(
            "back",
            "Back",
        )

        self.forward_button = ToolButton(
            "forward",
            "Forward",
        )

        self.reload_button = ToolButton(
            "reload",
            "Reload",
        )

        self.home_button = ToolButton(
            "home",
            "YouTube Home",
        )

        self.back_button.clicked.connect(
            self.go_back
        )

        self.forward_button.clicked.connect(
            self.go_forward
        )

        self.reload_button.clicked.connect(
            self.reload
        )

        self.home_button.clicked.connect(
            self.go_home
        )

        toolbar.addWidget(
            self.back_button
        )

        toolbar.addWidget(
            self.forward_button
        )

        toolbar.addWidget(
            self.reload_button
        )

        toolbar.addWidget(
            self.home_button
        )

        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------

        self.address_bar = QLineEdit()

        self.address_bar.setPlaceholderText(
            "Search YouTube..."
        )

        self.address_bar.setMinimumHeight(
            36
        )

        self.address_bar.returnPressed.connect(
            self.search_or_navigate
        )

        toolbar.addWidget(
            self.address_bar
        )

        search_button = ToolButton(
            "search",
            "Search YouTube",
        )

        search_button.clicked.connect(
            self.search_or_navigate
        )

        toolbar.addWidget(
            search_button
        )

        # ----------------------------------------------------
        # New tab
        # ----------------------------------------------------

        new_tab = ToolButton(
            "plus",
            "New tab",
        )

        new_tab.clicked.connect(
            self.new_tab
        )

        toolbar.addWidget(
            new_tab
        )

        # ----------------------------------------------------
        # Menu
        # ----------------------------------------------------

        menu_button = ToolButton(
            "menu",
            "Menu",
        )

        menu_button.setPopupMode(
            QToolButton.InstantPopup
        )

        popup = QMenu(
            self
        )

        popup.addAction(
            "YouTube Home",
            self.go_home,
        )

        popup.addAction(
            "New Tab",
            self.new_tab,
        )

        popup.addSeparator()

        ad_action = popup.addAction(
            "Ad Blocker"
        )

        ad_action.setCheckable(
            True
        )

        ad_action.setChecked(
            True
        )

        ad_action.triggered.connect(
            self.toggle_ad_blocker
        )

        popup.addSeparator()

        popup.addAction(
            "Toggle Theme",
            self.toggle_theme,
        )

        popup.addSeparator()

        popup.addAction(
            "About",
            self.show_about,
        )

        menu_button.setMenu(
            popup
        )

        toolbar.addWidget(
            menu_button
        )

        # ----------------------------------------------------
        # Tabs
        # ----------------------------------------------------

        self.tabs = QTabWidget()

        self.tabs.setTabsClosable(
            True
        )

        self.tabs.setMovable(
            True
        )

        self.tabs.setDocumentMode(
            True
        )

        self.tabs.tabCloseRequested.connect(
            self.close_tab
        )

        self.tabs.currentChanged.connect(
            self.tab_changed
        )

        self.setCentralWidget(
            self.tabs
        )

        self.statusBar().showMessage(
            "Private session • Ad blocker active"
        )

    # ========================================================
    # SHORTCUTS
    # ========================================================

    def setup_shortcuts(self):

        QShortcut(
            QKeySequence("Ctrl+T"),
            self,
            activated=self.new_tab,
        )

        QShortcut(
            QKeySequence("Ctrl+W"),
            self,
            activated=self.close_current_tab,
        )

        QShortcut(
            QKeySequence("Ctrl+L"),
            self,
            activated=self.focus_search,
        )

        QShortcut(
            QKeySequence("Ctrl+R"),
            self,
            activated=self.reload,
        )

        QShortcut(
            QKeySequence("F5"),
            self,
            activated=self.reload,
        )

        QShortcut(
            QKeySequence("Alt+Left"),
            self,
            activated=self.go_back,
        )

        QShortcut(
            QKeySequence("Alt+Right"),
            self,
            activated=self.go_forward,
        )

    # ========================================================
    # TABS
    # ========================================================

    def current_tab(self):

        widget = (
            self.tabs.currentWidget()
        )

        if isinstance(
            widget,
            YouTubeTab,
        ):

            return widget

        return None

    def new_tab(self):

        tab = YouTubeTab(
            self
        )

        index = self.tabs.addTab(
            tab,
            "YouTube",
        )

        self.tabs.setCurrentIndex(
            index
        )

        tab.navigate(
            "https://www.youtube.com/"
        )

    def close_tab(
        self,
        index,
    ):

        if self.tabs.count() <= 1:

            self.new_tab()

        widget = (
            self.tabs.widget(
                index
            )
        )

        if widget is None:
            return

        self.tabs.removeTab(
            index
        )

        widget.deleteLater()

    def close_current_tab(self):

        index = (
            self.tabs.currentIndex()
        )

        if index >= 0:

            self.close_tab(
                index
            )

    def tab_changed(
        self,
        index,
    ):

        tab = self.current_tab()

        if tab is None:
            return

        self.address_bar.setText(
            tab.view.url().toString()
        )

    # ========================================================
    # NAVIGATION
    # ========================================================

    def go_back(self):

        tab = self.current_tab()

        if tab:
            tab.view.back()

    def go_forward(self):

        tab = self.current_tab()

        if tab:
            tab.view.forward()

    def reload(self):

        tab = self.current_tab()

        if tab:
            tab.view.reload()

    def go_home(self):

        tab = self.current_tab()

        if tab:

            tab.navigate(
                "https://www.youtube.com/"
            )

    def focus_search(self):

        self.address_bar.setFocus()

        self.address_bar.selectAll()

    def search_or_navigate(self):

        value = (
            self.address_bar.text()
            .strip()
        )

        if not value:
            return

        tab = self.current_tab()

        if tab is None:
            return

        if is_youtube_url(value):

            tab.navigate(
                value
            )

        else:

            tab.navigate(
                youtube_search_url(
                    value
                )
            )

    # ========================================================
    # AD BLOCKER TOGGLE
    # ========================================================

    def toggle_ad_blocker(
        self,
        enabled,
    ):

        if enabled:

            self.web_profile.setUrlRequestInterceptor(
                self.ad_blocker
            )

            self.show_status(
                "Ad blocker enabled"
            )

        else:

            self.web_profile.setUrlRequestInterceptor(
                None
            )

            self.show_status(
                "Ad blocker disabled"
            )

    # ========================================================
    # THEME
    # ========================================================

    def toggle_theme(self):

        if self.current_theme == "dark":

            self.current_theme = "light"

        else:

            self.current_theme = "dark"

        QApplication.instance().setStyleSheet(
            build_stylesheet(
                self.current_theme
            )
        )

        self.show_status(
            f"{self.current_theme.capitalize()} theme enabled"
        )

    # ========================================================
    # STATUS
    # ========================================================

    def show_status(
        self,
        message,
    ):

        self.statusBar().showMessage(
            message,
            4000,
        )

    # ========================================================
    # ABOUT
    # ========================================================

    def show_about(self):

        QMessageBox.about(
            self,
            "About YouTube Lite",
            (
                f"<b>{APP_NAME}</b><br>"
                f"Version {APP_VERSION}<br><br>"
                "A lightweight YouTube-focused "
                "desktop client built with Python "
                "and PyQt5.<br><br>"
                "<b>Privacy:</b><br>"
                "No application history.<br>"
                "No search history.<br>"
                "No persistent cookies.<br>"
                "No persistent cache.<br>"
                "No local browsing database.<br>"
                "No application activity logs.<br><br>"
                "<b>Blocking:</b><br>"
                "Network ad/tracker filtering "
                "plus YouTube player ad detection."
            ),
        )


# ============================================================
# MAIN
# ============================================================

def main():

    QApplication.setApplicationName(
        APP_NAME
    )

    QApplication.setApplicationVersion(
        APP_VERSION
    )

    app = QApplication(
        sys.argv
    )

    app.setStyleSheet(
        build_stylesheet(
            "dark"
        )
    )

    window = YouTubeLite()

    window.show()

    return app.exec_()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    sys.exit(
        main()
    )