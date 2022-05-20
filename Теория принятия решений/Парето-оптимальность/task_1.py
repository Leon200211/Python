import numpy as np
import pandas as pd

df = pd.read_csv('/content/drive/MyDrive/ТПР Предметная область - ТПР Предметная область.csv')

df_iterrable_columns = df.columns[2:]
df_iterrable_columns
paretto_table = np.ones((len(df), len(df))) * -1

for i in range(len(df)):
  for j in range(len(df)): #Перебор всех пар
    if(i != j):
      marker_a = 0
      marker_b = 0 
      for colon_name in df_iterrable_columns: #Сравнение строки
        if(colon_name.find('+') != -1):
          if(df.iloc[i][colon_name] > df.iloc[j][colon_name]):
            marker_a += 1
          elif(df.iloc[j][colon_name] > df.iloc[i][colon_name]): 
            marker_b += 1
          else:
            marker_b += 1
            marker_a += 1
        elif(colon_name.find('-') != -1):
          if(df.iloc[i][colon_name] < df.iloc[j][colon_name]):
            marker_a += 1
          elif(df.iloc[j][colon_name] < df.iloc[i][colon_name]): 
            marker_b += 1
          else:
            marker_b += 1
            marker_a += 1
      if(marker_a == len(df_iterrable_columns)):
        paretto_table[i][j] = i
      elif(marker_b == len(df_iterrable_columns)):
        paretto_table[i][j] = j

paretto_plenty = set()

for line_index in range(len(paretto_table)):
  temp = -1
  for underline_index in range(len(paretto_table[line_index])):
    if(paretto_table[line_index][underline_index] != -1): 
      temp = paretto_table[line_index][underline_index]
      if(temp != line_index): 
        break
  if(temp != -1): paretto_plenty.add(temp)
    
paretto_plenty_df = df.loc[list(paretto_plenty)]
paretto_plenty_df

def minmax(data):
    data = data.drop(data[data['Цена, ₽\n (-)'] > 90000].index)
    data = data.drop(data[data['Частота CPU, ГГц\n (+)'] < 3].index)
    return data.iloc[0]

def subopt(data):
    data = data.drop(data[data['Частота CPU, ГГц\n (+)'] <= 3].index)
    data = data.sort_values('Цена, ₽\n (-)')
    return data.iloc[0]

def lexgraph(data):
    data = data.sort_values(['Объем оперативной памяти, Гб\n (+)','Объем GPU, Гб\n (+)', 'Частота CPU, ГГц\n (+)'])
    return data.iloc[-1]

minmax(paretto_plenty_df)

subopt(paretto_plenty_df)

lexgraph(paretto_plenty_df)
