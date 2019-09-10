from selenium import webdriver
import pandas as pd


class DataCollection:

    def __init__(self):
        data = pd.DataFrame()
        driver = self.connect_to_site("https://bip2.beeinformed.org/loss-map/")

        year_select = driver.find_element_by_css_selector("div.small-5.columns")
        for year_option in year_select.find_elements_by_tag_name("option"):
            year_option.click()
            data = data.append(self.scrape_table_data(driver, year_option.text), ignore_index=True)
        data.to_csv("data/total_winter_colony_losses.csv")
        driver.quit()

    def connect_to_site(self, site):
        driver = webdriver.Firefox()
        driver.get(site)
        return driver

    def scrape_table_data(self, driver, year):
        data = pd.DataFrame(columns=['year', 'state', 'total_loss(%)', 'beekeepers', 'beekeepers_exclusive_to_state(%)', 'colonies', 'colonies_exclusive_to_state(%)'])
        table = driver.find_elements_by_xpath("//table/tbody/tr")
        for t in table:
            split1 = t.text.split("\n")
            if len(split1) <= 2:
                continue
            split2 = split1[2].lstrip().split(" ")
            try:
                data = data.append({"year":year, "state":split1[0], 'total_loss(%)':float(split1[1][:-1]), 'beekeepers':int(split2[0]), 'beekeepers_exclusive_to_state(%)':float(split2[1][:-1]), 'colonies':int(split2[2]), 'colonies_exclusive_to_state(%)':float(split2[3][:-1])}, ignore_index=True)
            except IndexError:
                pass
        # print(data)
        return data