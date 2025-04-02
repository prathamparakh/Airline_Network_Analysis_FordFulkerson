"""this script extracts all the unique aircraft models (type designators) and exports it to csv"""
import csv
import pandas as pd

unique_models = set()

airline_df = pd.read_csv("data_cleaning/datasets/airlines.csv")

for models in airline_df["Plane"].dropna():
    l = models.split()
    unique_models.update(l)

unique_models = sorted(unique_models)

with open("data_cleaning/datasets/flight_models.csv", 'w', newline='', encoding='utf8') as file:
    writer = csv.writer(file)

    writer.writerow(['model_code'])
    for i in unique_models:
        writer.writerow([i])
