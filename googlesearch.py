import os
import platform
import subprocess
from selenium import webdriver
from PyQt5.QtWidgets import QMessageBox, QFileDialog

# Upgrade Meta
upgrade_name = "Headless Google Search"
upgrade_description = "Allows GPT-4 to perform a Google Search and return the results."
upgrade_config_options = []
upgrade_help_options = [
    {
        "name": "How to use this upgrade",
        "description": "When you input a command starting with '!google', the upgrade will perform a Google Search and return the results."
    },
    {
        "name": "How to install required components",
        "description": "This upgrade requires Google Chrome and ChromeDriver. If you don't have these installed, you will be prompted to do so when you use the upgrade."
    }
]

def __init__(self, main_window):
    self.main_window = main_window
    self.main_window.add_to_system_prompt("'!google' followed by a search query will search the requested object, and return the top 10 links, you may select one and the text on the page will be returned. ")

def check_chrome_installed(self):
    try:
        if platform.system() == "Windows":
            subprocess.Popen(['where', 'chrome'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:  # for MacOS and Linux
            subprocess.Popen(['which', 'google-chrome'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        QMessageBox.warning(self, 'Browser Missing', 'Google Chrome is required for this plugin. Please install it and try again.')
        return False
    return True

def check_chromedriver_installed(self):
    try:
        if platform.system() == "Windows":
            subprocess.Popen(['where', 'chromedriver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:  # for MacOS and Linux
            subprocess.Popen(['which', 'chromedriver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        file_dialog = QFileDialog()
        chromedriver_path, _ = file_dialog.getOpenFileName(self, 'Locate ChromeDriver', os.path.expanduser('~'))
        if not chromedriver_path:
            QMessageBox.warning(self, 'ChromeDriver Missing', 'ChromeDriver is required for this plugin. You can download it from: https://chromedriver.storage.googleapis.com/')
            return False
    return True

def search_google(self, query):
    if not check_chrome_installed() or not check_chromedriver_installed():
        return []

    # Start the Selenium browser
    driver = webdriver.Chrome()

    # Navigate to Google
    driver.get("https://www.google.com")

    # Enter the search query and submit it
    search_box = driver.find_element_by_name('q')
    search_box.send_keys(query)
    search_box.submit()

    # Scrape the results
    results = driver.find_elements_by_css_selector('div.g')

    # Return the top 10 results
    return [result.text for result in results[:10]]
