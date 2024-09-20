import os
import re
import time
import random
import string
import datetime
import json
import requests
from bs4 import BeautifulSoup

#import pandas as pd
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

# --- Utility Functions ---
# def convert_to_int(value):
#     """Converts string values like '1.2M' to integers."""
#     if pd.isna(value) or value == '':
#         return 0
#     if isinstance(value, str):
#         num = re.findall(r'\d+', value)
#         if not num:
#             return 0
#         num = int(float(''.join(num)))
#         multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
#         for suffix, multiplier in multipliers.items():
#             if suffix in value:
#                 return num * multiplier
#         return num
#     return int(value)

def get_youtube_url(video_id):
    """Constructs a YouTube URL from a video ID."""
    return f"https://www.youtube.com/watch?v={video_id}"

def get_youtube_video_id(youtube_url):
    """Extracts the video ID from a YouTube URL."""
    patterns = [
        r"watch\?v=([^&]+)",  # Standard format
        r"youtu\.be/([^&]+)"   # Shortened format
    ]
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None


# --- WebDriver Management ---

def init_webdriver():
    """Initializes a headless Chrome WebDriver."""
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage') 

        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=chrome_options) 

        print("WebDriver initialized successfully")
        return driver
    except Exception as e:
        print(f"Failed to initialize WebDriver: {e}")
        raise

def close_webdriver(driver):
    """Closes the WebDriver instance."""
    driver.quit()
    print("WebDriver closed successfully")

# --- YouTube Data Extraction ---

def get_comments_html(video_url, driver):
    """
    Fetches the HTML content of the comments section from a YouTube video.

    This function initializes a WebDriver instance to open the provided YouTube video URL,
    scrolls down to load the comments section, and retrieves the HTML content of the loaded
    comments section.

    Args:
        video_url (str): The URL of the YouTube video from which to fetch comments.
        driver: An initialized WebDriver instance (from Selenium).

    Returns:
        str: The HTML content of the comments section.

    Raises:
        TimeoutException: If the comments section does not load within the specified time.
    """

    # Wait until the comments section is loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-comments')))

    # Scroll to the comments section to load initial comments
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    # Set initial values for dynamic loading
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    scroll_pause_time = 2  # Time to wait between scrolls
    max_scrolls = 100  # Increase the max number of scrolls to ensure all comments are loaded
    scroll_count = 0

    while scroll_count < max_scrolls:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait for new comments to load dynamically
        time.sleep(scroll_pause_time)  # Simple wait to allow comments to load

        # Check the new scroll height and compare it with the last height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            # If the height hasn't changed, try one more scroll to ensure all comments are loaded
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                # If the height still hasn't changed, we've reached the end
                print("All comments have been loaded.")
                break

        last_height = new_height
        scroll_count += 1

    # Get the HTML of the comments section
    comments_html = driver.page_source

    # Close the driver
    close_webdriver(driver)

    return comments_html

def get_comment_thread_renderers(comments_html):
    """
    Parses the provided HTML content to extract YouTube comment threads and their counts.

    This function uses BeautifulSoup to parse the HTML content of a YouTube video's comments section.
    It finds and prints the number of comments and the number of comment thread renderers (`ytd-comment-thread-renderer`).
    It then returns a list of all the `ytd-comment-thread-renderer` elements found in the HTML.

    Args:
        comments_html (str): The HTML content of the comments section of a YouTube video.

    Returns:
        list: A list of `ytd-comment-thread-renderer` elements found in the HTML.
    """
    soup = BeautifulSoup(comments_html, 'html.parser')
    # comment_count_span = soup.find('span', class_='style-scope yt-formatted-string')
    # comment_count = comment_count_span.text.strip() if comment_count_span else "N/A"
    # print("Comment Count:", comment_count)
    return soup.find_all('ytd-comment-thread-renderer', class_='style-scope ytd-item-section-renderer')

def get_comments(comment_thread_renderers):
    """Parses comments and their data from the renderers."""
    comments_data = []
    for renderer in comment_thread_renderers:
        comment_text = renderer.find('yt-attributed-string', id='content-text')
        comment_text = comment_text.get_text(strip=True) if comment_text else None

        like_count = renderer.find('span', class_='style-scope ytd-comment-engagement-bar')
        like_count = like_count.get_text(strip=True) if like_count else None

        reply_count = renderer.find('ytd-button-renderer', id='more-replies')
        reply_count = reply_count.get_text(strip=True) if reply_count else None

        comments_data.append({
            "comment_text": comment_text,
            "like_count": like_count,
            "reply_count": reply_count
        })

    return comments_data

def get_video_comments(video_url, driver):
    """
    Retrieves comments from the provided YouTube video URL.

    Args:
        video_url (str): The URL of the YouTube video.

    Returns:
        list: A list of comments and their data.
    """
    comments_html = get_comments_html(video_url, driver)
    comment_thread_renderers = get_comment_thread_renderers(comments_html)
    return get_comments(comment_thread_renderers)

def get_video_data(video_id):
    """Fetches video data from YouTube given a video ID.

    Args:
        video_id (str): The ID of the YouTube video to fetch data for.

    Returns:
        dict: A dictionary containing the video data with the following keys:
            - 'channel_name': The name of the channel that uploaded the video.
            - 'video_title': The title of the video.
            - 'video_description': The description of the video.

    Raises:
        Exception: If there is an error accessing or processing the video data.
    """
    driver = init_webdriver()
    video_url = get_youtube_url(video_id)
    video_data = {}

    try:
        driver.get(video_url)

        # Handle consent dialog and other modals (if they appear)
        for xpath in ['//button[contains(., "I agree")]', '//button[@aria-label="Close"]']:
            try:
                button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                button.click()
            except TimeoutException:
                print("No consent dialog found or already handled.")
                pass 
        
        # Handle any other potential modal dialogs that might pop up
        try:
            dialog_close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Close"]'))
            )
            dialog_close_button.click()
        except TimeoutException:
            print("No additional modal dialogs found.")

        try:
            # Wait for key elements and extract data
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'bottom-row')))

            try:
                expand_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//tp-yt-paper-button[@id="expand"]'))
                )
                driver.execute_script("arguments[0].scrollIntoView();", expand_button)
                driver.execute_script("arguments[0].click();", expand_button)
            except TimeoutException:
                pass

            expanded_description = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'description-inline-expander'))
            )
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@class="style-scope ytd-watch-metadata"]//yt-formatted-string'))
            )
            channel_name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//ytd-channel-name[@id="channel-name"]//yt-formatted-string//a'))
            )

            video_data = {
                'channel_name': channel_name_element.text,
                'video_title': title_element.text,
                'video_description': expanded_description.text,
                'comments': get_video_comments(video_url, driver)
            }
            # # Clean the description
            # temp_list = [video_data]
            # cleaned_description = clean_description(temp_list)
            # video_data['video_description'] = cleaned_description


        except TimeoutException:
            print(f"Error processing {video_url}: Elements not found within timeout.")

    except Exception as e:
        print(f"Error processing {video_url}: {e}")

    finally:
        close_webdriver(driver)

    return video_data
