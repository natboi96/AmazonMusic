from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import requests

class AmazonMusic:
    #driver = webdriver.Chrome()
    #driver.get('https://music.amazon.com')
    #wait = WebDriverWait(driver, timeout = 10, poll_frequency = 0.25)
    #action = ActionChains(driver)

    search_url = 'https://music.amazon.com/search'
    playlist_url = 'https://music.amazon.com/my/playlists'
    def __init__(self):
        print("wtf")
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout = 10, poll_frequency = 0.25)
        self.action = ActionChains(self.driver)

    # Clicks an element based on ID
    def click_element(self, type, id):
        self.wait.until(ec.visibility_of_element_located((type, id)))
        self.driver.find_element(type, id).click()

    # Fills an input element
    def fill_field(self, type, id, input):
        self.wait.until(ec.visibility_of_element_located((type, id)))
        self.driver.find_element(type, id).send_keys(input)

    # Waits for element to load
    def wait_for_element(self, type, id):
        self.wait.until(ec.visibility_of_element_located((type, id)))

    # Logs in to Amazon music
    def music_login(self):
        self.click_element(By.ID, "signInButton")
        self.fill_field(By.ID, "ap_email", "7038322676")
        # Sleeps are used to avoid bot detection
        time.sleep(1)
        self.fill_field(By.ID, "ap_password", "Z4nP4k1@0")
        time.sleep(1)
        self.click_element(By.ID, "signInSubmit")

    # Searches song in search bar
    def search_song(self, song_title, song_author):
        time.sleep(3)
        if self.search_url not in self.driver.current_url:
            self.driver.get(self.search_url)
        # Song is added to filter out albums
        query_contents = song_title + " " + song_author + " song"
        self.fill_field(By.ID ,'navbarSearchInput', query_contents)
        time.sleep(1)
        self.click_element(By.ID, 'navbarSearchInputButton')

    # Adds songs to playlist
    def add_to_playlist(self, song_title, song_author, playlist_name):
        self.search_song(song_title, song_author)
        time.sleep(3)
        # Checks where the desired song appears on the search
        potential_songs = self.driver.find_elements_by_tag_name("music-horizontal-item")
        song_flag = -1
        for song in potential_songs:
            song_info = song.get_attribute('data-key')
            if song_title in song_info and song_author in song_info:
                self.action.move_to_element(song).perform()
                time.sleep(1)
                song.find_element_by_xpath(".//music-button[@icon-name='more']").click()
                song_flag = 1
                break
        
        if song_flag == -1:
            print("Song not found")
            return

        # Clicks add to playlist button
        print("Adding to playlist")
        time.sleep(0.5)
        list_items = self.driver.find_elements_by_tag_name("music-list-item")
        for item in list_items:
            if item.get_attribute("id") == "contextMenuOption1":
                item.click()
                break

        # Searches through playlists for target
        print("Pressing Add button")
        time.sleep(1)
        playlists = self.driver.find_elements_by_tag_name("music-image-row")
        for playlist in playlists:
            if playlist.get_attribute("primary-text") == playlist_name:
                playlist.find_element_by_xpath(".//music-button[@icon-name='add']").click()
        
        time.sleep(1)
        self.driver.get(self.search_url)

    # Checks if playlist exists in library
    def check_playlist(self, playlist_name):
        time.sleep(1)
        if self.playlist_url not in self.driver.current_url:
            self.driver.get(self.playlist_url)
        # Find your playlist section
        self.wait_for_element(By.TAG_NAME, "music-vertical-item")
        playlists = self.driver.find_elements_by_tag_name("music-vertical-item")
        for playlist in playlists:
            if playlist_name == playlist.get_attribute("primary-text"):
                return True
        return False

    # Creates playlist
    def create_playlist(self, playlist_name):
        time.sleep(1)
        if self.playlist_url not in self.driver.current_url:
            self.driver.get(self.playlist_url)
        # Clicks create new playlist button
        self.wait_for_element(By.TAG_NAME, "music-button")
        buttons = self.driver.find_elements_by_tag_name("music-button")
        for button in buttons:
            if button.get_attribute("icon-name") == "add":
                button.click()
                break
        # Inputs playlist name and creates
        self.fill_field(By.TAG_NAME, "input", playlist_name)
        self.click_element(By.ID, "dialogButton1")