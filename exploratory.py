import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv("data/total_winter_colony_losses.csv")


def average_loss_by_year():
    yearly_average = data.groupby(data['year']).mean()
    plt.plot(yearly_average.index, yearly_average['total_loss(%)'], 'y*-')
    plt.title("Yearly average total colony winter loss")
    plt.ylabel("Percentage of loss")
    plt.xlabel("Years")
    plt.xticks(rotation=45)
    plt.show()
    print("y")



def main():
    average_loss_by_year()


if __name__ == "__main__":
    main()
