import time
import json
import requests


def get_competition_id(url):
    competition_id = None

    req = requests.get(url)
    if req.status_code == 200:
        text = [line.strip() for line in req.text.split('\n')]
        for line in text:
            pattern = 'competitionId='
            pos = line.find(pattern)
            if pos > 0:
                content, _ = line[pos:].split(',', 1)
                competition_id = content.split('=')[1][:-1]
                break
    elif req.status_code == 404:
        print('Not Found')

    return competition_id


def get_leaderboard(competition_name, competition_id):
    if competition_id is None:
        return None

    url = f'https://www.kaggle.com/c/{competition_id}/leaderboard.json?\
          includeBeforeUser=true&includeAfterUser=true'
    req = requests.get(url)
    if req.status_code == 200:
        content = req.text
        with open(f'db-kaggle/{competition_name}.json', 'w') as fw:
            fw.write(content)
        return content
    else:
        print('Not Found')
        return None


def make_ranks(competition_name, content):
    if content is None:
        return None

    results = json.loads(content) 
    with open(f'db-kaggle/{competition_name}.leaderboard', 'w') as fw:
        '''
         {'teamId': 3948842,
          'rank': 50,
          'change': None,
          'medal': 'silver',
          'teamName': 'Daizu',
          'teamMembers': [{'profileUrl': '/daizutabi',
            'thumbnailUrl': 'https://storage.googleapis.com/kaggle-avatars/thumbnails/2871269-gr.jpg',
            'tier': 'contributor',
            'displayName': 'Daizu'}],
          'score': '0.01321',
          'entries': 32,
          'lastSubmission': '2019-11-27T13:53:32.1033333Z',
          'sourceKernelName': None,
          'sourceKernelUrl': None}
        '''
        for dic in results['beforeUser']:
            fw.write(f"{dic['rank']},{dic['teamName']},{dic['score']}\n")
        for dic in results['afterUser']:
            fw.write(f"{dic['rank']},{dic['teamName']},{dic['score']}\n")


if __name__ == '__main__':
    names = [
        'nfl-big-data-bowl-2020',
        'data-science-bowl-2019',
        'homesite-quote-conversion',
        'GiveMeSomeCredit',
        'DontGetKicked',
        'porto-seguro-safe-driver-prediction',
        'bioresponse',
        'predict-who-is-more-influential-in-a-social-network',
        'bike-sharing-demand',
        'avazu-ctr-prediction',
        'stumbleupon',
        'springleaf-marketing-response',
        'restaurant-revenue-prediction',
        'kobe-bryant-shot-selection',
        'allstate-claims-severity',
        'house-prices-advanced-regression-techniques',
        'facebook-recruiting-iv-human-or-bot',
        'tmdb-box-office-prediction',
        'predict-west-nile-virus',
        'caterpillar-tube-pricing',
        'amazon-employee-access-challenge',
        'dont-overfit-ii',
        'home-credit-default-risk',
        'liberty-mutual-fire-peril',
        'nyc-taxi-trip-duration',
        'elo-merchant-category-recommendation',
        'mercedes-benz-greener-manufacturing',
        'santander-customer-transaction-prediction',
        'ieee-fraud-detection',
        'sberbank-russian-housing-market',
        'loan-default-prediction',
        'criteo-display-ad-challenge',
        'favorita-grocery-sales-forecasting',
        'walmart-recruiting-store-sales-forecasting',
        'talkingdata-adtracking-fraud-detection',
        'rossmann-store-sales'
            ]
    names = ['santander-value-prediction-challenge']
 

    for competition_name in names:
        url = f'https://www.kaggle.com/c/{competition_name}/leaderboard'
        print(f'processing {competition_name}: {url}')
        competition_id = get_competition_id(url)
        content = get_leaderboard(competition_name, competition_id)
        make_ranks(competition_name, content)
        time.sleep(5)

