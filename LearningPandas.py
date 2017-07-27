import pandas as pd

df=pd.read_html('http://www.bollymoviereviewz.com/2013/08/shahrukh-khan-movie-list-1992-2013.html')

##df=df[1][1:]
##
##finalDF=df[[1,2]]
##
##finalDF.rename(columns={1:'State',2:'Code'},inplace=True)
###finalDF.columns(['State','Code'])
##
##finalDF.set_index('Code' , inplace=True)

myDF=df[0][[0,1]][1:]

myDF.rename(columns={1:'release_date',0:'movie_name'},inplace=True)
myDF.set_index('movie_name',inplace=True)
print(myDF)
