'''
This code works to clean the train_small and train_medium datasets.
To clean the actual train dataset, open and run clean_train.py
'''

import pandas as pd
import numpy as np

dtypes = {'store_nbr': np.dtype('int64'),
          'item_nbr': np.dtype('int64'),
          'unit_sales': np.dtype('float64'),
          }

'''Read in files'''
pd_train = pd.read_csv('data/train_medium.csv', dtype=dtypes)
stores = pd.read_csv('data/stores.csv',  dtype=dtypes)
items = pd.read_csv('data/items.csv',  dtype=dtypes)
#trans = pd.read_csv('data/transactions.csv',  dtype=dtypes)
oil = pd.read_csv('data/oil.csv')
holidays = pd.read_csv('data/holidays_events.csv', dtype=dtypes)

# print('DATATYPES: items')
# print(items.dtypes)
# print(pd_train.head())
# print('stores')
# print(stores.head())

'''Merging'''
pd_train = pd_train.drop(['onpromotion'], axis = 1)
# print(pd_train.head())
pd_train = pd_train.merge(stores, left_on='store_nbr', right_on='store_nbr', how='left')

pd_train = pd_train.merge(items, left_on='item_nbr', right_on='item_nbr', how='left')
# print('merged item')
# print(pd_train.head())
pd_train = pd_train.merge(holidays, left_on='date', right_on='date', how='left')
# print('merged holidays')
# print(pd_train.head())
pd_train = pd_train.merge(oil, left_on='date', right_on='date', how='left')
# print('merged oil')
# print(pd_train.head())
pd_train = pd_train.drop(['description', 'state', 'locale_name', 'class', 'dcoilwtico'], axis = 1)
# print('dropped bunch of stuff')
# print(pd_train.head())

'''Change date column to reflect month only'''
for idx, date in enumerate(pd_train['date']):
  sdate = int(str(date).split("/", 1)[0])
  pd_train['date'][idx] = sdate

#Rearranging, renaming columns
cols = pd_train.columns.tolist()
cols.insert(len(cols)-1, cols.pop(cols.index('unit_sales')))
pd_train = pd_train[cols]
pd_train = pd_train.rename(index=str, columns={"type_x": "type_store", "type_y": "type_holiday"})
pd_train = pd_train.sort_values(by=['id'])

print('after merging and rearranging:')
print(pd_train.head())
print(pd_train.dtypes)



'''Write results to cleaned_train_medium.csv '''
pd_train.to_csv('data/cleaned_train_medium.csv', index=False)

print('after merging ')
print(list(pd_train.columns.values))
print('head:')
print(pd_train.head())
print('# of lines in cleaned dataframe: '+ str(pd_train.count()))
print('final column names: \n')
print(pd_train.columns.values)
