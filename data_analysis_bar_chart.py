import pandas as pd
import glob
import seaborn
import matplotlib.pyplot as plt

pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 36)
files = glob.glob('C:/*.csv')
df = pd.concat((pd.read_csv(file) for file in files), ignore_index=True)
df = df.apply(lambda x: x.str.replace('"', '')).apply(lambda x: x.str.replace('=', ''))


def to_datetime(columnname):
    for items in list(columnname):
        df[items] = pd.to_datetime(df[items])


to_datetime(['Entered', 'Received', 'Completed'])

# create new column
df['Entered - Received'] = df['Entered'] - df['Received']

df = df.stack().reset_index()  # stack is pivot

new_df = pd.DataFrame(df)
new_df = new_df.xs(['level_1', 0], axis=1, drop_level=True)  # keep the level you want
new_df = new_df.sort_values(0)  # sort value
new_df = new_df.drop_duplicates(subset=0)  # drop duplicate, subset is the column that you want to drop duplicates on
new_df['allocation'] = new_df[0].diff()  # subtract from previous row for the timestamp column
new_df = new_df.rename(columns={'level_1': 'function', 0: 'timestamp'})  # rename column

new_df['minutes'] = pd.to_timedelta(new_df['allocation']).astype('timedelta64[m]')  # convert time to minutes
new_df2 = pd.DataFrame(data=new_df[['function', 'minutes']])
new_df2 = new_df2.groupby('function', as_index=False).sum()  # groupby function
new_df2 = pd.DataFrame(new_df2)

graph = seaborn.barplot(x=new_df2['function'], y=new_df2['minutes'])

for p in graph.patches:
    graph.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

plt.legend(['Entered', 'Completed'], )
graph.get_legend().legendHandles[0].set_color('blue')
graph.get_legend().legendHandles[1].set_color('yellow')
plt.xlabel('Function')
plt.ylabel('Minutes')
plt.style.use('seaborn')
plt.title('Minutes per function')
plt.show()
