import requests
import json
import sentiment

vader = sentiment.get_config()

base_url = 'http://newsapi.org/v2/everything?q='
api_key = '&apiKey=d3fb8c426d0d4bb383a06ac1df4b61a5'
lang = '&language=en'
num = '&pageSize=100'

def news_new(query):
    for i in range(1, 22):
        date = '2021-01-'+str(i)+'&to=2021-01-'+str(i)
        print(date)
        news(query, date)
        

def news(query, date, sort_by='popularity'):#='2021-1-19&to=2021-01-22'
    start_date = '&from=' + date
    sort = '&sortBy=' + sort_by
    res = (requests.get(base_url + query + start_date + lang + sort + num + api_key)).json()
    parsed_results = {
        'date_range': date,
        'total_results':0,
        'articles': [],
        'sentiment': {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0},
    }
    for article in res['articles']:
        pol = vader.polarity_scores(article['title'])
        parsed_results['articles'].append({
            'title': article['title'],
            'url': article['url'],
            'published_at': article['publishedAt'],
            'polarity_scores': pol
        })

        sent = 0
        parsed_results['total_results']+=1
        if pol['neg'] > pol['pos']:
            parsed_results['sentiment']['neg'] += 1
        elif pol['pos'] > pol['neg']:
            sent = 1
            parsed_results['sentiment']['pos'] += 1
        else:
            sent = 1
            parsed_results['sentiment']['neu'] += 1

        parsed_results['sentiment']['compound'] += sent

    parsed_results['sentiment']['compound'] /= parsed_results['total_results']
    
    with open('./scraped_data/' + str(query) + '_news_' + date + '.json', 'w+') as outfile:
        json.dump(parsed_results, outfile)

    return 'nf'

if __name__ == "__main__":
    news_new("hi")