"""
~This is a simple Python program that will retrieve a list of character names from a Toyhouse user's profile.

~Using "requests" to get the webpages, and "BeautifulSoup" to scrape data, and "re" to clean the text more.

~Disclaimer: No authentication/sessions are used so it will only scrape whatever is publicly available.

~Credit for baseline BeautifulSoup code structure: https://realpython.com/beautiful-soup-web-scraper-python/#what-is-web-scraping

"""

import requests
from bs4 import BeautifulSoup
import re

#Removes symbols, spaces, emojis, etc. so the text is cleaner.
def clean_text(text):
    cleaned_text = re.sub(r"[^\w\s]", "", text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    return cleaned_text

"""
~Once a username is entered, requests will get the url and then a loop will occur that increases the page number at the end until no more pages are found/no more character elements are found.
"""

def get_characters(username):
    page_number = 1
    while True:
        URL = f"https://toyhou.se/{username}/characters/folder:all?page={page_number}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        #If the username entered isn't accessible, then one of these messages will appear instead.
        results = soup.find(id="main")
        if "This user is not visible to guests." in page.text:
            print("This user is not visible to guests.")
            break
        if "We can't find that page!" in page.text:
            print("Page does not exist or access is denied.")
            break
        results = soup.find(id="main")
        if results is None:
            print("An unexpected error has occurred.")
            break

        #"Thumb-caption" is the name of the class that displays the character names.
        character_elements = results.find_all("div", class_="thumb-caption")

        if not character_elements:
            print("...")
            print("No more pages!")
            break

        for character_element in character_elements:
            title_element = character_element.find(
                "span", class_="thumb-character-name"
            )
            if title_element:
                cleaned_name = clean_text(title_element.text.strip())
                print(cleaned_name)
                print()

        page_number += 1


#User types in account name to scrape
username = input("Enter username: ")
get_characters(username)
