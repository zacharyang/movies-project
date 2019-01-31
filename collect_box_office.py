from bs4 import BeautifulSoup
import requests as rq
import re
import pandas as pd
import numpy as np

def convdollar(x):
    """
    Just a parsing function converting 2.5k to 2500, 1mil to 1000000
    """
    if 'k' in x:
        return float(x.replace('k',''))*1000
    else:
        return float(x)*1000000

def scrape():
    """
    Gets all box office data from 1989 to 2018 from boxofficemojo.com

    """
    years=[str(a) for a in range(1989,2019)]
    df_list=[]
    for year in years:
        r=rq.get('https://www.boxofficemojo.com/yearly/chart/?view2=worldwide&yr=%s&p=.htm' % year)
        print('Box Office data for %s scraped' % year)
        p=BeautifulSoup(r.text,'html.parser')
        ### Look for the table ### 
        b=p.find_all('table')
        ### Usually the fourth table object on page ### 
        tb=b[3].find_all('td')
        data=[]
        for i in tb:
            if i.find('a')!=None:
                data.append(i.find('a').contents[0])
            elif i.find('font')!=None:
                 data.append(i.find('font').contents[0])
            elif i.find('b')!=None:
                data.append(i.find('b').contents[0])
        ### Still a <b> tag left for <font> tags ## 
        data=[a.contents[0] if type(a)!=bs4.element.NavigableString else a for a in data]
        ### Strip special characters ### 
        data=[re.sub('[^A-Za-z0-9-. ]+', '', a) for a in data]
        ### Fill NaNs ### 
        data=[np.nan if a =='na' else a for a in data]
        columns=['bo_year_rank','title','studio','worldwide-gross','domestic-gross','domestic-pct','overseas-gross','overseas-pct']
        to_df=data[6:]
        if len(to_df)%len(columns) != 0:
            print('Possible table misalignment in table for year %s' % year)
            break 
        nrow=int(len(to_df)/len(columns))
        df=pd.DataFrame(np.array(to_df).reshape(nrow,8),columns=columns)
        df[['worldwide-gross','domestic-gross','overseas-gross']]=df[['worldwide-gross','domestic-gross','overseas-gross']].applymap(lambda x:convdollar(x))
        df['bo_year']=int(year)
        df_list.append(df)

    main=pd.concat(df_list)

    main.to_csv('./data/annual_mojo.csv')

    
if __name__ == "__main__": 

    scrape()









