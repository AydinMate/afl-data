from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import csv

driver = webdriver.Chrome()
driver.get("https://www.foxsports.com.au/afl/stats/players?sortBy=disposals")

wait = WebDriverWait(driver, 10)

wait.until(EC.presence_of_element_located((By.ID, "banner-ad-close-sticky-mobile")))
close_banner_button = driver.find_element(By.ID, "banner-ad-close-sticky-mobile")
close_banner_button.click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ab-message-button")))
message_buttons = driver.find_elements(By.CLASS_NAME, "ab-message-button")
no_button = message_buttons[1]
no_button.click()

pages = 34
data = []  # Initialize data list for each page

for page in range(1, pages + 1):
    next_button = driver.find_element(By.CLASS_NAME, "fiso-lab-pagination__button--next")
    actions = ActionChains(driver)
    actions.move_to_element(next_button).perform()
    titles = []
    whole_table = driver.find_element(By.CLASS_NAME, "fiso-lab-table")

    heading_table = whole_table.find_element(By.TAG_NAME, "thead")
    heading_elements_row = heading_table.find_element(By.TAG_NAME, "tr")
    heading_elements = heading_elements_row.find_elements(By.TAG_NAME, "th")

    for heading_element in heading_elements:
        heading = heading_element.find_element(By.CLASS_NAME, "fiso-lab-table__column-heading")
        title = heading.get_attribute("title")
        titles.append(title)

    titles.insert(1, "Team")

    player_table = whole_table.find_element(By.TAG_NAME, "tbody")

    player_elements = player_table.find_elements(By.TAG_NAME, "tr")

    for player_element in player_elements:
        player_data_list = {}
        player_name = player_element.find_element(By.CLASS_NAME, "fiso-lab-table__row-heading-primary-data").text
        player_data_list["Player"] = player_name
        player_team_element = player_element.find_element(By.CLASS_NAME, "fiso-lab-table__row-heading-secondary-data")
        player_team = player_team_element.get_attribute("title")
        player_data_list["Team"] = player_team
        all_player_data = player_element.find_elements(By.TAG_NAME, "td")

        for i, player_data in enumerate(all_player_data):
            player_data_list[titles[i + 2]] = player_data.text

        data.append(player_data_list)

    next_button.click()

with open("data.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Data saved to data.json")

with open("data.csv", "w", newline="") as csv_file:
    fieldnames = data[0].keys() if data else []  # Get the field names from the first record
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for record in data:
        writer.writerow(record)

print("Data saved to data.csv")

driver.quit()
