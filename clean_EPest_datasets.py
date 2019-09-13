import pandas as pd
import os
import re

# EPest datasets collected from: https://water.usgs.gov/nawqa/pnsp/usage/maps/county-level/

# moderate to highly toxic to bee pesticides collected from: https://en.wikipedia.org/wiki/Pesticide_toxicity_to_bees
dangerous_pesticides = ["Sulfoxaflor", "Tetrachlorvinphos ", "Resmethrin", "Pyrazophos ", "Propoxur", "Phosphamidon",
                        "Phosmet", "Phorate", "Permethrin", "Oxydemeton-methyl", "Omethoate", "Naled", "Monocrotophos",
                        "Mexacarbate", "Mevinphos", "Methyl parathion ", "Methoxychlor", "Methomyl", "Methiocarb",
                        "Methidathion", "Methamidophos", "Malathion", "Imidacloprid", "Fonofos", "Fenvalerate",
                        "Fenthion", "Fensulfothion", "Fenitrothion", "Dimethoate", "Dicrotophos", "Dichlorvos",
                        "Diazinon", "Demeton", "Cypermethrin", "Chlorpyrifos", "Carbofuran", "Carbaryl", "Bifenthrin",
                        "Azinphos-methyl", "Thiamethoxam", "Clothianidin", "Endosulfan", "Demeton-S-methyl", "Acephate"]
dangerous_pesticides = [x.upper() for x in dangerous_pesticides] # convert to capital case


def convert_fips_filter_dangerous_pesticides():
    # converting these fips values to State and county names is how arcgis online used the data
    # dataset from: https://www2.census.gov/programs-surveys/popest/geographies/2017/all-geocodes-v2017.xlsx
    # open the geocodes file to convert FIPS codes
    fips_codes = pd.read_csv("data/all-geocodes-v2017.csv", header=4)
    states = fips_codes[fips_codes['Summary Level'] == 40]
    states = states.drop(columns=['Summary Level', 'County Code (FIPS)',
                          'County Subdivision Code (FIPS)', 'Place Code (FIPS)',
                          'Consolidtated City Code (FIPS)'])
    states = states.rename(columns={"Area Name (including legal/statistical area description)": "state_name"})
    counties = fips_codes[fips_codes['Summary Level'] == 50]

    # clean each yearly file
    files = os.listdir("data/")
    epest_re = re.compile("EPest\.county\.estimates.+(20\d\d)\.txt")
    for file in files:
        if epest_re.match(file):
            curr_data = pd.read_csv("data/" + file, header=0, delimiter='\t')
            small_data = curr_data[curr_data['COMPOUND'].isin(dangerous_pesticides)]
            small_data = small_data.rename(columns={"STATE_FIPS_CODE": "State Code (FIPS)", "COUNTY_FIPS_CODE": "County Code (FIPS)"})
            # merge them together to get the county data for each
            small_data = pd.merge(small_data, counties, on=['State Code (FIPS)', "County Code (FIPS)"])
            # merge again to get the state data
            small_data = pd.merge(small_data, states, on='State Code (FIPS)')
            small_data = small_data.drop(columns=['State Code (FIPS)', 'County Code (FIPS)', 'Summary Level',
                                                  'County Subdivision Code (FIPS)', 'Place Code (FIPS)',
                                                  'Consolidtated City Code (FIPS)'])
            small_data = small_data.rename(columns={'Area Name (including legal/statistical area description)':"county_name"})
            small_data.to_csv("data/small_" + file.replace(".txt", ".csv"))

# combine the datasets together into one file
def combine_years():
    data = None
    small_re = re.compile("small_EPest\.county\.estimates.+(20\d\d)\.csv")
    for file in os.listdir("data/"):
        if small_re.match(file):
            if data is None:
                data = pd.read_csv("data/"+file)
            else:
                data = data.append(pd.read_csv("data/"+file))
    data.to_csv("data/combined_small_EPest_county.csv")
    print("h")


def main():
    convert_fips_filter_dangerous_pesticides()
    combine_years()
    print("yo")


if __name__ == "__main__":
    main()

