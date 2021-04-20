import pandas as pd
import seaborn as sns
import glob
pd.set_option('display.width',500)
pd.set_option('display.max_columns',50)

files = glob.glob('C:/*.csv')

df = pd.concat((pd.read_csv(file,dtype='unicode') for file in files), ignore_index=True)

df = df.loc[df['startTime'].notnull(),:]  #filter out null

df['Location'] = df['destinationAddress'].apply(lambda x: x[x.rindex(',')+1:-5])       #pull string
df['Location'].replace([' nj ',' NJ ',' NEW JERSEY '], ' New Jersey ', inplace=True)


df['startTime']=pd.to_datetime(df['startTime'])
count_of_succeed = pd.DataFrame(df[['startTime','completed','quantity','Id','Location']])

count_of_succeed['Year'] = [x.strftime('%Y') for x in count_of_succeed['startTime'].tolist()]
count_of_succeed['Month'] = [x.strftime('%m') for x in count_of_succeed['startTime'].tolist()]
count_of_succeed['Date'] = [x.strftime('%Y-%m-%d') for x in count_of_succeed['startTime'].tolist()]
count_of_succeed['Time'] = [x.strftime('%H:%M:%S') for x in count_of_succeed['startTime'].tolist()]

pivot_table = count_of_succeed[(count_of_succeed['Location']==' New York ') |
                               (count_of_succeed['Location']==' New Jersey ') |
                               (count_of_succeed['Location']==' Pennsylvania ')].pivot_table(index=['Year','Month'],
                                                                                             values='Id',
                                                                                             columns='Location',
                                                                                             aggfunc='count',
                                                                                             margins=True,
                                                                                             margins_name='Total')

pivot_table.sort_values(by='Total', ascending= False)
pivot_table.fillna('')

pivot_table_no_totals = count_of_succeed[(count_of_succeed['Location']==' New York ') |
                               (count_of_succeed['Location']==' New Jersey ') |
                               (count_of_succeed['Location']==' Pennsylvania ')].pivot_table(index=['Year','Month'],
                                                                                             values='shortId',
                                                                                             columns='Location',
                                                                                             aggfunc='count')


pivot_table_no_totals.fillna('')

graph = sns.barplot(data=pivot_table_no_totals)

for p in graph.patches:
    graph.annotate(str(p.get_height()),(p.get_x()*1.005,p.get_height()*1.005))



