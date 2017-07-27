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



def doPickle():

    main_df=pd.DataFrame()
    all_states=pd.read_pickle('all_states.pickle')

    for state in all_states:

        query = "FMAC/HPI_"+str(state)
        df=quandl.get(query, authtoken=myKey)
        df.columns = [str(state)]
        if main_df.empty:
           main_df=df
           
        else:
          main_df= main_df.join(df)

    #print(main_df)    

    # Pickle using pickle provided by Python

    my_pickle_out= open('pickletext.pickle','wb')

    pickle.dump(main_df , my_pickle_out )

    my_pickle_out.close()


#doPickle()
my_pickle_in = open('pickletext.pickle' , 'rb')

my_data=pickle.load(my_pickle_in)

#print(my_data)

#my_data['AL2']=my_data['AL'] * 2


#print(my_data[['AL','AL2']])

# Pandas Pickle

#my_data.to_pickle('pickle.pickle')
#my_data2 = pd.read_pickle('pickle.pickle')
#print(HPI_data2)


my_data.plot()

#plt.legend().remove()

plt.show()





