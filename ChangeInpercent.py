import quandl

import pandas as pd

import pickle

import matplotlib.pyplot as plt

from matplotlib import style

style.use('fivethirtyeight')


myKey=open('quandlApi.txt','r').read()




def getState_List():

    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')

    all_states= fiddy_states[0][0][1:]

    all_states.to_pickle('all_states.pickle')

def HPI_Benchmark():
    
    df=quandl.get("FMAC/HPI_USA", authtoken=myKey)
    # print(df)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    
    return df

def doPickle():
    
    main_df=pd.DataFrame()
    all_states=pd.read_pickle('all_states.pickle')

    for state in all_states:

        query = "FMAC/HPI_"+str(state)
        df=quandl.get(query, authtoken=myKey)
        df.columns = [str(state)]
        df[state]=(df[state] - df[state][0]) / df[state][0] * 100.0
        
        if main_df.empty:
           main_df=df
           
        else:
          main_df= main_df.join(df)
    
    main_df.to_pickle('newDFpickle.pickle')   


my_data=pd.read_pickle('newDFpickle.pickle')

my_data_correlation=my_data.corr()


print(my_data_correlation.describe())

   
#doPickle()

##ax1=plt.subplot2grid((1,1),(0,0))
##
##benchmark=HPI_Benchmark()
##
##
##
##
##my_data=pd.read_pickle('newDFpickle.pickle')
##
##my_data.plot(ax=ax1)
##benchmark.plot(color='k',ax=ax1,linewidth=10)
##plt.legend().remove()
##
##plt.show()





