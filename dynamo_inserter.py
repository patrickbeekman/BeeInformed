import boto3
import pandas as pd
from decimal import Decimal
import numpy as np

with open("access.txt") as f:
    full = f.read().split("\n")
    access_key = full[0]
    secret_key = full[1]

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name='us-east-2')


def insert_winter_colony_loss():
    table = dynamodb.Table('winter_colony_loss')

    print(table.creation_date_time)

    colony_loss = pd.read_csv("data/total_winter_colony_losses.csv", header=0,
                              dtype={'total_loss(%)':np.dtype(Decimal),
                                     'beekeepers_exclusive_to_state(%)':np.dtype(Decimal),
                                     'colonies_exclusive_to_state(%)':np.dtype(Decimal)})

    for row in colony_loss.iterrows():
        item = row[1].to_dict()
        item.pop('Unnamed: 0')
        table.put_item(Item=item)
