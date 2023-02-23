import json
import time
from seleniumwire import webdriver
from seleniumwire.utils import decode as sw_decode
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Opening the website on Chrome
try:
    driver = webdriver.Chrome()
except:
    driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://food.grab.com/sg/en/restaurants")

driver.maximize_window()

# writing the initial data into json file
def write_json(new_data, filename="restaurants.json"):
    try:
        with open(filename, "r+") as file:
            file_data = json.load(file)
            file_data["restaurants"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    except:
        print("File is not present")

# fetching values and dumping it into required format
def fetch_values_from_json(post_data):
    d = {}
    for p in post_data:  # get the restaurants latlng from the post response and save it in a dictionary
        print(p, '--------------------')
        l = p['searchResult']['searchMerchants']  # list of restaurants
        for rst in l:  # for each restaurant
            try:
                # chainID is the key for the dictionary
                d[rst['chainID']] = {
                    'chainName': rst['chainName'], 'latlng': rst['latlng']}
            except Exception as err:  # if the chainID is not present in the dictionary
                d[rst['address']['name']] = {
                    'chainName': rst['address']['name'], 'latlng': rst['latlng']}

    write_json(d)

# calculating the total count of restaurants


def getting_total_count():
    f = open('restaurants.json')
    data = json.load(f)
    total_count = 0
    for i in data['restaurants']:
        print(len(i.keys()))
        total_count = total_count + int(len(i.keys()))
    print("Total Restaurants:", total_count)
    final_dict = {}
    final_dict['total_restaurants'] = total_count
    final_dict.update(data)
    return final_dict

#writing data to csv
def write_to_csv(final_dict):
        final_dataframe = []
        for i in final_dict['restaurants']:
            for k,v in i.items():
                innner_dict = {}
                innner_dict['Restaurant'] = v['chainName']
                innner_dict['Latitude'] = v['latlng']['latitude']
                innner_dict['Longitude'] = v['latlng']['longitude']
                final_dataframe.append(innner_dict)
        df = pd.DataFrame(final_dataframe)
        df.to_csv('Final_data.csv')

# method to fetch all details while scrolling the screen
def scroll_down():
    post_data = []

    """A method for scrolling the page"""

    # get the latest height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        element = driver.find_element(By.CLASS_NAME, "footerNew___2PBRV")
        driver.execute_script("arguments[0].scrollIntoView();", element)

        # Wait to load the page.
        time.sleep(10)

        # Calculate new height and compare with available last scroll height.
        updated_height = driver.execute_script(
            "return document.body.scrollHeight")

        if updated_height == last_height:
            break

        last_height = updated_height
        # Returns an iterator over captured requests. Useful when dealing with a large number of requests.
        for r in driver.iter_requests():
            if r.method == 'POST' and r.url == "https://portal.grab.com/foodweb/v2/search":  # capture the post response

                response_data = sw_decode(r.response.body, r.response.headers.get(
                    'Content-Encoding', 'identity'))  # decode the response
                response_data = response_data.decode(
                    "utf8")  # decode the response
                # print(data_1,'data')

                # convert the response to json
                jsonified_data = json.loads(response_data)
                post_data.append(jsonified_data)

    fetch_values_from_json(post_data)
    final_dict = getting_total_count()
    with open("final_required_data.json", "w") as outfile:
        json.dump(final_dict, outfile)
    write_to_csv(final_dict)

   


for i in range(1):
    scroll_down()

driver.quit()
