import pandas as pd
import numpy as np

df = pd.read_csv("C:/Customer_Service.csv",
                 usecols=["ID", "OLD VALUE", "NEW VALUE","FIELD CHANGED", "DATE", "USER"])
cs_df = df.loc[(df['NEW VALUE'].str.startswith("Customer Service Dept")) & (df["FIELD CHANGED"] == "Label"), :]
cs_id = cs_df['ID'].to_list()
df = df[df['ID'].isin(cs_id)]

conditions = [(df['NEW VALUE'] == "Good"),
              (df['OLD VALUE'] == "Not Good") & (df['NEW VALUE'] == "Excellent")]
result = ["ID APPROVED", "NOT ID APPROVED"]
df['ID APPROVED?'] = np.select(conditions, result, default="")

df['ID'] = pd.to_numeric(df['ID'].str[:6])  # left function
df['ID_ext'] = df['ID'].str.split('-').str[1]
df.sort_values(by=['ID', 'DATE'], ascending=True, inplace=True)

df = df.loc[(df['PA APPROVED?'] == 'Good') | (df['PA APPROVED?'] == 'Excellent')]
df['ID compare'] = df['ID'].eq(df['ID'].shift())
df['ID APPROVED? compare'] = df['ID APPROVED?'].eq(df['ID APPROVED?'].shift())

conditions = [
    (df['ID APPROVED?'] == "ID APPROVED") & (df['ID compare'] == True) & (df['ID APPROVED? compare'] == False)]
result = ["Not approved"]
df['FINAL ID APPROVED'] = np.select(conditions, result, default="approved")

notapproved = df.loc[df['FINAL ID APPROVED'] == 'Not approved', :]

approved = df.groupby("FINAL ID APPROVED").count()
