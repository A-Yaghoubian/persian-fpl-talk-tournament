import requests
import pandas as pd


def get_total_players_number():
    req = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
    data = req.json()['elements']
    return len(data)


def get_gw_numbers():
    url = 'https://fantasy.premierleague.com/api/element-summary/1/'
    req = requests.get(url)
    data = req.json()['history']
    return len(data)


class DataCollector:
    base_urls = ['https://fantasy.premierleague.com/api/bootstrap-static/',
                 'https://fantasy.premierleague.com/api/element-summary/']
    players_number = get_total_players_number()
    gw_numbers = get_gw_numbers()

    def player_data_collector(self, player_id):
        req = requests.get(self.base_urls[1] + player_id + '/')
        data = pd.DataFrame(req.json()['history'])
        data = data[['selected', 'transfers_balance', 'transfers_in', 'transfers_out', 'ict_index', 'value']]
        label_list = [0]
        for i in range(1, len(data)):
            label = data.iloc[i]['value'] - data.iloc[i - 1]['value']
            if label > 0:
                label = 1
            elif label < 0:
                label = -1
            else:
                label = 0
            label_list.append(label)
        data['label'] = label_list
        test = data.iloc[-1]
        data = data.drop(data.index[-1])
        return [data, test]

    def all_players_train_data_collector(self):
        req = requests.get(self.base_urls[0])
        elements_data = req.json()['elements']
        train_data, test_data = self.player_data_collector('1')
        for i in range(1, self.players_number):
            if elements_data[i]['status'] != "u":
                print('loading {name}\'s data'.format(name=elements_data[i]['web_name']))
                temp = self.player_data_collector(str(elements_data[i]['id']))
                train_data = train_data.append(temp[0])
                test_data = test_data.append(temp[1])

        # train_data = train_data.reset_index(drop=True)
        # test_data = test_data.reset_index(drop=True)
        return train_data, test_data

    def load_data_to_csv(self):
        train, test = self.all_players_train_data_collector()
        train.to_csv('train_data.csv')
        test.to_csv('test_data.csv')
