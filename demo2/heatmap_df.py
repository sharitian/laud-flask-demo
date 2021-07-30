import pandas as pd
import numpy as np

df = pd.read_csv("laud/df.csv") #df has only sample id, species, and count columns

first_sample = df.iloc[0][0]
species_cols = df[df["sample_id"] == first_sample]["taxa_name"].tolist()
new_columns = ["sample_id"] + species_cols 
unique_samples = np.unique(df["sample_id"]).tolist()

heat_df = pd.DataFrame(columns = new_columns)
for sample in unique_samples:
    new_row = pd.DataFrame()
    new_row["sample_id"] = [sample]
    tab = df[df["sample_id"] == sample]
    for i in range(len(tab)):
        row = tab.iloc[i]
        species = [row[1]]
        count = [row[2]]
        new_row[species] = [count]
    heat_df = heat_df.append(new_row)

heat_df.to_csv("laud/heat_df.csv")