import pandas as pd

myDF=pd.read_csv('ZILL-Z50035_TT.csv')

#myDF.set_index('Date',inplace=True)
#print(myDF.head())

#newDF=pd.DataFrame(myDF['Value'])

#newDF.to_csv('thenewll.csv')

#print(newDF)

#latestDF=pd.read_csv('ZILL-Z50035_TT.csv',index_col=0)
#print(latestDF.head())

#latestDF.columns=['manual_column']

#print(latestDF.head())

#latestDF.to_csv('csv3.csv',header=False)


##latestDF=myDF[['Value','Date']]
##print(latestDF.head().set_index('Value'))


myDF.to_csv('Abhicsv.csv',header=False)

newDF=pd.read_csv('Abhicsv.csv', names=['Date','Price'])
newDF.set_index('Date',inplace=True)
newDF.rename(columns={'Price':'Actual_price'},inplace=True)
print(newDF.head())
