import os
import pandas as pd

count = 0
link = r'L:\\NEC\\excel\\'
dirls = []
dirls = os.listdir(link)
ln = len(dirls)
print(*dirls, sep = '\n')

for file in dirls:
    print(file + ' - open file')
    path = link + file
    df = pd.read_excel(path,'Report', index_col=None)
    df = df.iloc[:, [0,3,7,8,9,11,12]]
    df = df.loc[((df['Name.1'] == 'MDP-400MB-1BB')  
                 |(df['Name.1'] == 'MODEM-EA')
                 |(df['Name.1'] == 'MODEM-EV')
                 |(df['Name.1'] == 'MODEM-AV')
                 |(df['Name.1'] == 'MODEM-A')
                 |(df['Name.1'] == 'MDP-400MB-1AA')
                 |(df['Name.1'] == 'MDP-1200MB-1AA')
                 |(df['Name.1'] == 'MDP-1200MB-1BB')                
                 |(df['Name.1'] == 'MC-AV')                    
                 |(df['Name.1'] == 'GbE4e-AV')
                 |(df['Name.1'] == 'GbE4f-AV')                                      
                 |(df['Name.1'] == 'GbE-A')
                 |(df['Name.1'] == 'IAG')                   
                 )]
    df = df.drop_duplicates()
    df.to_csv('data.txt', sep='\t', index=None, mode='a')

    count = count + 1
    print('Read', count, 'files from', ln)
  
print('__________________________________________________')
print('Script is finished, read', count, 'files from', ln)
