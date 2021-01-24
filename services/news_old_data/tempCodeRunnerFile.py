for i in range(22):
        for j in range (len(df[0]['polarity_scores'])):
            
            neg = df[i]['polarity_scores'][j]['neg']
            neu = df[i]['polarity_scores'][j]['neu']
            pos = df[i]['polarity_scores'][j]['pos']
            comp = df[i]['polarity_scores'][j]['compound']

            total_pos += pos
            total_neg += neg

            if comp > 0:
                total_pos += neu
            elif comp < 0:
                total_neg += neu
            else:
                total_neu += neu

    print(neg)
    print(pos)
    print(neu)