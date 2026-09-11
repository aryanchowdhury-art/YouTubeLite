# YouTubeLite

A lightweight, privacy-focused YouTube desktop client built with **Python and PyQt5**.

YouTubeLite is designed for watching YouTube without the unnecessary features of a full web browser. It provides a simple YouTube-focused interface with an in-memory browsing session and a lightweight ad-blocking layer.

## Features

* 🎬 YouTube-focused browsing
* 🔎 YouTube search
* 📑 Multiple tabs
* ⬅️ Back / forward navigation
* 🔄 Reload
* 🏠 YouTube home
* 🚫 Lightweight YouTube ad blocking
* 🕵️ In-memory browser session
* 🧹 No application-level browsing history
* 🧹 No search-history database
* 🧹 No bookmarks or watch-later database
* 🗑️ No persistent application configuration
* 🌙 Dark / light interface
* ⌨️ Keyboard shortcuts
* 🔒 Non-YouTube navigation blocked
* ⚡ Lightweight desktop interface

## Privacy

YouTubeLite uses an **off-the-record QtWebEngine profile** rather than maintaining a normal persistent browser profile.

The application does not intentionally create or maintain:

* Browser history
* Search history
* Bookmarks
* Watch-later lists
* Persistent cookies
* Persistent HTTP cache
* Local browsing databases
* Application activity logs
* JSON configuration files

This means the application itself does not maintain a normal persistent browsing history.

> **Note:** This does not make you anonymous on the internet. YouTube, Google, your network provider, or other network services can still observe network activity.

## Ad Blocking

YouTubeLite uses two layers:

### Network filtering

The application intercepts web requests through QtWebEngine and blocks known advertising and tracking endpoints.

### YouTube player filtering

A YouTube-specific JavaScript layer detects common player advertisement states and attempts to:

* Skip available advertisements
* Close advertisement overlays
* Remove common ad containers
* Prevent some advertisement elements from remaining visible

The blocker is intentionally lightweight and focused specifically on YouTube.

> YouTube frequently changes its player and advertising infrastructure, so no custom YouTube blocker can guarantee permanent compatibility.

## Technology

* **Python**
* **PyQt5**
* **QtWebEngine / Chromium**
* **JavaScript**
* **Qt WebEngine URL interception**

## Requirements

* Python 3.9+
* PyQt5
* PyQtWebEngine

Install the dependencies:

```bash
pip install PyQt5 PyQtWebEngine
```

## Run

```bash
python youtube_lite.py
```

## Keyboard Shortcuts

| Shortcut      | Action                   |
| ------------- | ------------------------ |
| `Ctrl + L`    | Focus address/search bar |
| `Ctrl + T`    | New tab                  |
| `Ctrl + W`    | Close current tab        |
| `Ctrl + R`    | Reload page              |
| `Alt + Left`  | Go back                  |
| `Alt + Right` | Go forward               |
| `Ctrl + Q`    | Quit                     |

## Project Structure

```text
YouTubeLite/
│
├── youtube_lite.py
└── README.md
```

## Why This Exists

YouTubeLite was built as a personal lightweight alternative to opening a full browser just to watch YouTube.

The goal is simple:

**Open → Search → Watch → Close**

No general-purpose browser features. No unnecessary application data. Just a small desktop YouTube client.

## Disclaimer

YouTubeLite is an independent project and is **not affiliated with or endorsed by YouTube or Google**.

YouTube's website, player, APIs, and advertising mechanisms can change at any time. Features such as ad filtering may therefore require future updates.

## License

Choose a license that matches how you want others to use the project.

For a simple personal/open-source project, **MIT License** is a reasonable choice.
