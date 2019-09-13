import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def average_loss_by_year():
    data = pd.read_csv("data/total_winter_colony_losses.csv")
    yearly_average = data.groupby(data['year']).mean()
    plt.plot(yearly_average.index, yearly_average['total_loss(%)'], 'y*-')
    plt.title("Yearly average total colony winter loss")
    plt.ylabel("Percentage of loss")
    plt.xlabel("Years")
    plt.xticks(rotation=45)
    plt.show()
    print("y")


def pesticde_usage_by_state():
    pesticides = pd.read_csv("data/combined_small_EPest_county.csv")
    pesticides_2016 = pesticides[pesticides['YEAR'] == 2016]
    state_pesticides = pesticides_2016.groupby("state_name").sum()
    fig, ax = plt.subplots()
    ax.bar(state_pesticides.index, state_pesticides['EPEST_LOW_KG'])
    plt.xticks(rotation=90)
    plt.title("2016 total amount of harmful pesticides used by state")
    plt.ylabel("EPest_LOW_KG (pesticide usage)")
    fig.tight_layout()
    plt.show()


def pesticide_use_by_year():
    pesticides = pd.read_csv("data/combined_small_EPest_county.csv")
    year_pests = pesticides.groupby('YEAR').sum()
    plt.plot(year_pests.index, year_pests['EPEST_LOW_KG'], 'go--')
    plt.xlabel("year")
    plt.ylabel("EPEST_LOW_KG total")
    plt.title("Total amount of dangerous pesticide \nusage across USA by Year")
    plt.show()


def average_loss_by_state():
    colony_loss = pd.read_csv("data/total_winter_colony_losses.csv")
    loss_by_state = colony_loss.groupby("state").mean()
    loss_by_state = loss_by_state[loss_by_state.index != "MultiStateOperation"]
    fig, ax = plt.subplots()
    plt.bar(loss_by_state.index, loss_by_state['total_loss(%)'])
    avg_loss = np.mean(loss_by_state['total_loss(%)'])
    plt.hlines(avg_loss, 'Alabama', 'Wyoming', label='Average loss (%.02f)' % avg_loss, colors='g', linestyles='dashed')
    plt.title("Average winter colony loss by state (2007-2017)")
    plt.xticks(rotation=90)
    plt.ylabel("Percentage of hives lost")
    plt.legend()
    fig.tight_layout()
    plt.show()


def correlation():
    pesticides = pd.read_csv("data/combined_small_EPest_county.csv")
    colony_loss = pd.read_csv("data/total_winter_colony_losses.csv")
    pest_usage_by_state = pesticides.groupby(['state_name', 'YEAR'], as_index=False)['EPEST_LOW_KG'].sum()
    pest_usage_by_state = pest_usage_by_state.rename(columns={'state_name': 'state'})
    colony_loss['YEAR'] = [int(x.split("/")[0]) for x in colony_loss['year']]
    merged = pd.merge(colony_loss, pest_usage_by_state, on=['state', 'YEAR'])
    # merged = merged2[merged2['YEAR'] == 2017]
    print(np.corrcoef(merged['total_loss(%)'], merged['EPEST_LOW_KG']))
    plt.scatter(merged['total_loss(%)'], merged['EPEST_LOW_KG'])
    plt.title("scatter of correlation %.03f" % np.corrcoef(merged['total_loss(%)'], merged['EPEST_LOW_KG'])[0][1])
    plt.show()
    # all of the correlations are very weak [+0.06 to -0.23] depending on year, -0.067 overall


# which states use the most sulfoxaflor
def state_sulfoxaflor():
    pesticides = pd.read_csv("data/combined_small_EPest_county.csv")
    # don't include 2017 because there is no data for california
    pesticides = pesticides[pesticides['YEAR'] < 2017]
    pesticides_sulf = pesticides[pesticides['COMPOUND'] == 'SULFOXAFLOR'].groupby("state_name")['EPEST_LOW_KG'].sum()
    fig, ax = plt.subplots()
    plt.bar(pesticides_sulf.index, pesticides_sulf.values)
    plt.xticks(rotation=90)
    plt.ylabel("EPEST_LOW_KG")
    plt.title("Total amount of sulfoxaflor used in each state from 2007-2016")
    fig.tight_layout()
    plt.show()


def sulfoxaflor_by_year():
    pesticides = pd.read_csv("data/combined_small_EPest_county.csv")
    pesticides = pesticides[pesticides['COMPOUND'] == 'SULFOXAFLOR'].groupby("YEAR")['EPEST_LOW_KG'].sum()
    ax = plt.subplot(111)
    plt.plot(pesticides.index, pesticides.values)
    plt.axvline(x=2010, label='Creation', color='#68e823')
    plt.axvline(x=2013, label='EPA approval', color='#367d10')
    plt.axvline(x=2015, label='Overturned and banned', color='#82ab1a')
    plt.axvline(x=2016, label='Approved for non-blooming crops', color='#d4cb20')
    plt.axvline(x=2018, label='Total Approval (July)', color='#d45020')
    plt.ylabel("EPEST_LOW_KG")
    plt.title("Total amount of sulfoxaflor used by year")
    # fig.tight_layout()
    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=5)
    # plt.legend()
    plt.show()


def main():
    # average_loss_by_year()
    # pesticde_usage_by_state()
    # pesticide_use_by_year()
    # average_loss_by_state()
    # correlation()
    # state_sulfoxaflor()
    sulfoxaflor_by_year()


if __name__ == "__main__":
    main()
