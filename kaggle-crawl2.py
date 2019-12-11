import random
import time
import json
import requests


def url2name(line):
    pat = 'https://www.kaggle.com/c/'
    pos = line.find(pat)
    name, _ = line[len(pat):].split('/', 1)
    return name


class compInfo(object):
    def __init__(self, url):
        self.name = url2name(url)
        self.id = None
        self.lb_url = None
        self.public = None
        self.private = None 


def make_comp_info(url):
    comp_info = compInfo(url)
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
        comp_info.id = competition_id
        comp_info.lb_url = f'https://www.kaggle.com/c/{comp_info.id}/leaderboard.json?\
                            includeBeforeUser=true&includeAfterUser=true'
    elif req.status_code == 404:
        print('Not Found')
    return comp_info


def get_leaderboard(comp_info, lb_type):
    if comp_info.lb_url is None:
        return None

    url = f'{comp_info.lb_url}&type={lb_type}'
    
    req = requests.get(url)
    if req.status_code != 200:
        print('Not Found')
        return None

    text = req.text
    with open(f'db-kaggle/{comp_info.name}-{comp_info.id}-{lb_type}.json', 'w') as fw:
        fw.write(text)

    results = json.loads(text) 
    with open(f'db-kaggle/{comp_info.name}-{comp_info.id}-{lb_type}.leaderboard', 'w') as fw:
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
            fw.write(f"{dic['rank']};{dic['teamName']};{dic['score']}\n")
        for dic in results['afterUser']:
            fw.write(f"{dic['rank']};{dic['teamName']};{dic['score']}\n")


if __name__ == '__main__':
    names = [
        # 'nfl-big-data-bowl-2020',
        # 'data-science-bowl-2019',
        # 'homesite-quote-conversion',
        # 'GiveMeSomeCredit',
        # 'DontGetKicked',
        # 'porto-seguro-safe-driver-prediction',
        # 'bioresponse',
        # 'predict-who-is-more-influential-in-a-social-network',
        # 'bike-sharing-demand',
        # 'avazu-ctr-prediction',
        # 'stumbleupon',
        # 'springleaf-marketing-response',
        # 'restaurant-revenue-prediction',
        # 'kobe-bryant-shot-selection',
        # 'allstate-claims-severity',
        # 'house-prices-advanced-regression-techniques',
        # 'facebook-recruiting-iv-human-or-bot',
        # 'tmdb-box-office-prediction',
        # 'predict-west-nile-virus',
        # 'caterpillar-tube-pricing',
        # 'amazon-employee-access-challenge',
        # 'dont-overfit-ii',
        # 'home-credit-default-risk',
        # 'liberty-mutual-fire-peril',
        # 'nyc-taxi-trip-duration',
        # 'elo-merchant-category-recommendation',
        # 'mercedes-benz-greener-manufacturing',
        # 'santander-customer-transaction-prediction',
        # 'ieee-fraud-detection',
        # 'sberbank-russian-housing-market',
        # 'loan-default-prediction',
        # 'criteo-display-ad-challenge',
        # 'favorita-grocery-sales-forecasting',
        # 'walmart-recruiting-store-sales-forecasting',
        # 'talkingdata-adtracking-fraud-detection',
        # 'rossmann-store-sales',
        # 'bioresponse',
        # 'facebook-recruiting-iv-human-or-bot',
        'kdd-cup-2014-predicting-excitement-at-donors-choose'
    ]
    # urls = [
    #         'https://www.kaggle.com/c/rsna-intracranial-hemorrhage-detection/leaderboard',
    #         'https://www.kaggle.com/c/porto-seguro-safe-driver-prediction/leaderboard',
    #         'https://www.kaggle.com/c/data-science-bowl-2019/leaderboard',
    #         ]
    for competition_name in names:
        url = f'https://www.kaggle.com/c/{competition_name}/leaderboard'
        print(f'processing: {url}')
        comp_info = make_comp_info(url)
        # get_leaderboard(comp_info, 'public')
        # time.sleep(1 + random.choice([1, 2, 3]))
        get_leaderboard(comp_info, 'private')
        time.sleep(1 + random.choice([1, 2, 3]))

