import requests
import pandas as pd
import xlsxwriter

mini_league_url = 'https://fantasy.premierleague.com/api/leagues-classic/1820907/standings'
url_str = 'https://fantasy.premierleague.com/api/entry/'
exeption_players = []
event_number = int(input('enter GameWeek number:'))


def is_chip_active(event, data):
    for item in data:
        if item['event'] == event:
            return item['name']


def pure_point_rank_cal(url):
    req = requests.get(url)
    data = req.json()
    live_point = data['current'][-1]['points'] - data['current'][-1]['event_transfers_cost']
    chip = is_chip_active(event=event_number, data=data['chips'])
    if chip != '':
        temp = url.split('/')[-3]
        exeption_players.append(temp)
        print('player with entry {entry} use {ch} chip'.format(entry=temp, ch=chip))
    return [live_point,
            data['current'][-1]['overall_rank'],
            ]


def remove_chip_points():
    pass


def get_point_and_rank(player_url):
    player_dict = {'live_point': [], 'overall_rank': []}
    for i in range(len(player_url)):
        temp = pure_point_rank_cal(player_url[i])
        player_dict['live_point'].append(temp[0])
        player_dict['overall_rank'].append(temp[1])
    return player_dict


def get_data_from_api(data):
    player_url = []
    for manager in data['standings']['results']:
        player_url.append(url_str + str(manager['entry']) + '/history/')
    player_data = get_point_and_rank(player_url)
    my_data = {'entry': [], 'player_name': [], 'live_points': [], 'total': [], 'overall_rank': []}
    for i in range(len(data['standings']['results'])):
        my_data['entry'].append(data['standings']['results'][i]['entry'])
        my_data['player_name'].append(data['standings']['results'][i]['player_name'])
        my_data['live_points'].append(player_data['live_point'][i])
        my_data['total'].append(data['standings']['results'][i]['total'])
        my_data['overall_rank'].append(player_data['overall_rank'][i])

    df = pd.DataFrame.from_dict(my_data)
    df.to_csv('standings')


def gp_to_df(data, players):
    df = data.loc[data['entry'] == players[0]]
    for i in range(1, len(players)):
        df = df.append(data.loc[data['entry'] == players[i]])
    return df


def add2sheet(sheet, gp, number):
    pass


def get_col_widths(dataframe):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]


def write_to_excel(groups):
    df = pd.read_csv('standings')
    df = df.drop(['Unnamed: 0', 'live_points'], axis=1)

    # --------------creating excel-------------------
    gp1 = gp_to_df(df, groups['group1'])
    gp1 = gp1.drop(['entry'], axis=1)
    gp1 = gp1.sort_values(['total'], ascending=False)
    # gp1 = gp1.values.tolist()

    gp2 = gp_to_df(df, groups['group2'])
    gp2 = gp2.drop(['entry'], axis=1)
    gp2 = gp2.sort_values(['total'], ascending=False)
    # gp2 = gp2.values.tolist()

    gp3 = gp_to_df(df, groups['group3'])
    gp3 = gp3.drop(['entry'], axis=1)
    gp3 = gp3.sort_values(['total'], ascending=False)
    # gp3 = gp3.values.tolist()

    gp4 = gp_to_df(df, groups['group4'])
    gp4 = gp4.drop(['entry'], axis=1)
    gp4 = gp4.sort_values(['total'], ascending=False)
    # gp4 = gp4.values.tolist()

    gp5 = gp_to_df(df, groups['group5'])
    gp5 = gp5.drop(['entry'], axis=1)
    gp5 = gp5.sort_values(['total'], ascending=False)
    # gp5 = gp5.values.tolist()

    gp6 = gp_to_df(df, groups['group6'])
    gp6 = gp6.drop(['entry'], axis=1)
    gp6 = gp6.sort_values(['total'], ascending=False)
    # gp6 = gp6.values.tolist()

    gp7 = gp_to_df(df, groups['group7'])
    gp7 = gp7.drop(['entry'], axis=1)
    gp7 = gp7.sort_values(['total'], ascending=False)
    # gp7 = gp7.values.tolist()

    gp8 = gp_to_df(df, groups['group8'])
    gp8 = gp8.drop(['entry'], axis=1)
    gp8 = gp8.sort_values(['total'], ascending=False)
    # gp8 = gp8.values.tolist()

    with pd.ExcelWriter('tournament.xlsx') as writer:
        gp1.to_excel(writer, sheet_name='group1')
        gp2.to_excel(writer, sheet_name='group2')
        gp3.to_excel(writer, sheet_name='group3')
        gp4.to_excel(writer, sheet_name='group4')
        gp5.to_excel(writer, sheet_name='group5')
        gp6.to_excel(writer, sheet_name='group6')
        gp7.to_excel(writer, sheet_name='group7')
        gp8.to_excel(writer, sheet_name='group8')


def main():
    req = requests.get(url=mini_league_url)
    data = req.json()
    groups = {'group1': [7920571, 819492, 140198, 741437],
              'group2': [264137, 31170, 38361, 2906292],
              'group3': [2394736, 463353, 1222107, 500175],
              'group4': [666945, 2323635, 591903, 4035275],
              'group5': [6288151, 2350965, 2851917, 486370],
              'group6': [923618, 947904, 66222, 849015],
              'group7': [360376, 1754002, 850550, 58798],
              'group8': [1731625, 7489425, 499751, 2363324]}
    inp = input('enter \'0\' for exit, \'1\' for get data from api, \'2\' for create excel.\nenter your number:')
    while inp != '0':
        if inp == '1':
            print('LOADING ...')
            get_data_from_api(data)
        elif inp == '2':
            try:
                print('CREATING EXCEL ...')
                write_to_excel(groups)
            except:
                print('there is no data, first get data from api')
        inp = input('enter \'0\' for exit, \'1\' for get data from api, \'2\' for create excel.\nenter your number:')


if __name__ == '__main__':
    main()
