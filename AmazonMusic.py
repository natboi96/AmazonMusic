from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import requests

driver = webdriver.Chrome()
driver.get('https://music.amazon.com')
wait = WebDriverWait(driver, timeout = 10, poll_frequency = 0.25)
action = ActionChains(driver)

search_url = 'https://music.amazon.com/search'
playlist_url = 'https://music.amazon.com/my/playlists'

# Clicks an element based on ID
def click_element(type, id):
    wait.until(ec.visibility_of_element_located((type, id)))
    driver.find_element(type, id).click()

# Fills an input element
def fill_field(type, id, input):
    wait.until(ec.visibility_of_element_located((type, id)))
    driver.find_element(type, id).send_keys(input)

# Waits for element to load
def wait_for_element(type, id):
    wait.until(ec.visibility_of_element_located((type, id)))

# Logs in to Amazon music
def music_login():
    click_element(By.ID, "signInButton")
    fill_field(By.ID, "ap_email", "7038322676")
    # Sleeps are used to avoid bot detection
    time.sleep(1)
    fill_field(By.ID, "ap_password", "Z4nP4k1@0")
    time.sleep(1)
    click_element(By.ID, "signInSubmit")

# Searches song in search bar
def search_song(song_title, song_author):
    time.sleep(3)
    if search_url not in driver.current_url:
        driver.get(search_url)
    query_contents = song_title + " " + song_author
    fill_field(By.ID ,'navbarSearchInput', query_contents)
    time.sleep(1)
    click_element(By.ID, 'navbarSearchInputButton')

# Adds songs to playlist
def add_to_playlist(song_title, song_author, playlist_name):
    search_song(song_title, song_author)
    time.sleep(3)
    # Checks where the desired song appears on the search
    potential_songs = driver.find_elements_by_tag_name("music-horizontal-item")
    song_flag = -1
    for song in potential_songs:
        song_info = song.get_attribute('data-key')
        if song_title in song_info and song_author in song_info:
            action.move_to_element(song).perform()
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
    list_items = driver.find_elements_by_tag_name("music-list-item")
    for item in list_items:
        if item.get_attribute("id") == "contextMenuOption1":
            item.click()
            break

    # Searches through playlists for target
    print("Pressing Add button")
    time.sleep(1)
    playlists = driver.find_elements_by_tag_name("music-image-row")
    for playlist in playlists:
        if playlist.get_attribute("primary-text") == playlist_name:
            playlist.find_element_by_xpath(".//music-button[@icon-name='add']").click()
    
    time.sleep(1)
    driver.get(search_url)

# Checks if playlist exists in library
def check_playlist(playlist_name):
    time.sleep(1)
    if playlist_url not in driver.current_url:
        driver.get(playlist_url)
    # Find your playlist section
    wait_for_element(By.TAG_NAME, "music-vertical-item")
    playlists = driver.find_elements_by_tag_name("music-vertical-item")
    for playlist in playlists:
        if playlist_name == playlist.get_attribute("primary-text"):
            return True
    return False

# Creates playlist
def create_playlist(playlist_name):
    time.sleep(1)
    if playlist_url not in driver.current_url:
        driver.get(playlist_url)
    # Clicks create new playlist button
    wait_for_element(By.TAG_NAME, "music-button")
    buttons = driver.find_elements_by_tag_name("music-button")
    for button in buttons:
        if button.get_attribute("icon-name") == "add":
            button.click()
            break
    # Inputs playlist name and creates
    fill_field(By.TAG_NAME, "input", playlist_name)
    click_element(By.ID, "dialogButton1")

music_login()
playlist_name = input("Enter a playlist name: ")
song_list = []
for i in range(1):
    song_info = input("Enter song {i} title and author: ").format(i).split(" - ")
    song_list.append([song_info[0], song_info[1]])

if not check_playlist(playlist_name):
    create_playlist(playlist_name)

for song in song_list:
    add_to_playlist(song[0], song[1], playlist_name)