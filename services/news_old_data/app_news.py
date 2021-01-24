import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

def graph_make(daily_data):
    pos_data = []
    neg_data = []
    neu_data = []

    names = []
    N = 21
    i = 1
    for day in daily_data:
        pos_data.append(day[0])
        neu_data.append(day[1])
        neg_data.append(day[2])
        names.append("Jan " + str(i))
        i += 1

    ind = np.arange(N) # the x locations for the groups
    width = 0.35
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])

    bottom_two = np.add(pos_data, neu_data).tolist()

    ax.bar(ind, pos_data, width, color='g', edgecolor='white')
    ax.bar(ind, neu_data, width,bottom=pos_data, color='#7f6d5f', edgecolor='white')
    ax.bar(ind, neg_data, width,bottom=bottom_two, color='r', edgecolor='white')

    

    #ax.set_ylabel('Scores')
    #ax.set_title('Scores by group and gender')
    #ax.set_xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    #ax.set_yticks(np.arange(0, 81, 10))
    #ax.legend(labels=['Men', 'Women'])
    plt.show()

def daily_analysis(df):

    daily_data = [] 

    total_pos = 0
    total_neg = 0
    total_neu = 0
    #print(df[0]['polarity_scores'][0]['neg'])
    for i in range(21):
        total_neg = 0
        total_neu = 0
        total_pos = 0
        for j in range(len(df[i]['polarity_scores'])):
            
            neg = df[i]['polarity_scores'][j]['neg']
            neu = df[i]['polarity_scores'][j]['neu']
            pos = df[i]['polarity_scores'][j]['pos']
            comp = df[i]['polarity_scores'][j]['compound']

            total_pos += pos
            total_neg += neg
            #print(comp)
            if comp > 0:
                total_pos += neu
                total_pos += comp
            elif comp < 0:
                total_neg += neu
                total_neg -= comp
            elif comp == 0:
                total_neu += neu
        
        total_neg = round(total_neg, 3)
        total_pos = round(total_pos, 3)
        total_neu = round(total_neu, 3)
        
        
        print(i)
        print(total_neg)
        print(total_pos)
        print(total_neu)
        print("\n")

        #daily_data.append([total_pos, total_neg])
        daily_data.append([total_pos, total_neu, total_neg])
    graph_make(daily_data)

df = []
day = []

for i in range(1,22):
    date = '2021-01-'+str(i)+'&to=2021-01-'+str(i)
    print(date)
    data = json.load(open('./scraped_data/bitcoin_news_' + date + '.json'))
    df.append(pd.DataFrame(data["articles"])) 
    #print("TEST")
    #print(df[i-1]['polarity_scores'])

daily_analysis(df)

    

# for i in range(5):
#     print(df["polarity_scores"][i])