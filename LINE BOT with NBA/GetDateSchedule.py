import requests, json, time, datetime, pytz

def tz_from_utc_ms_ts(utc_ms_ts, tz_info):
    """Given millisecond utc timestamp and a timezone return dateime

    :param utc_ms_ts: Unix UTC timestamp in milliseconds
    :param tz_info: timezone info
    :return: timezone aware datetime
    """
    # convert from time stamp to datetime
    utc_datetime = datetime.datetime.utcfromtimestamp(utc_ms_ts / 1000.)

    # set the timezone to UTC, and then convert to desired timezone
    return utc_datetime.replace(tzinfo=pytz.timezone('UTC')).astimezone(tz_info)

def GetDateSchedule(Team, Date):
    url = 'https://tw.global.nba.com/stats2/team/schedule.json?countryCode=TW&locale=zh_TW&teamCode={}'.format(Team)
    Schedule = json.loads(requests.get(url).text)['payload']
    url = 'https://tw.global.nba.com/stats2/team/standing.json?locale=zh_TW&teamCode={}'.format(Team)
    Standing = json.loads(requests.get(url).text)['payload']

    year = str(Schedule['season']['year'])
    Card = json.load(open('json/Card.json','r',encoding='utf-8'))

    t = time.time()
    dt = datetime.datetime.fromtimestamp(t)
    dt = datetime.datetime.strptime(Date,'%Y-%m-%dT%H:%M')
    month = dt.month
    for monthGroup in Schedule['monthGroups']:
        n_month = monthGroup['number']
        if(n_month != month):
            continue
        for game in monthGroup['games']:
            if(game['profile']['dateTimeEt'] != Date):
                continue
            Our = None
            Oppo = None
            if(game['awayTeam']['profile']['code'] == Team):
                Oppo = 'homeTeam'
                Our = 'awayTeam'
            else:
                Oppo = 'awayTeam'
                Our = 'homeTeam'
            # Game Info
            dt = tz_from_utc_ms_ts(float(game['profile']['utcMillis']) ,pytz.timezone('Asia/Taipei'))
            Game_Date = '{}/{}'.format(str(dt.month).rjust(2, '0'), str(dt.day).rjust(2, '0'))
            Game_Time = '{}:{}'.format(str(dt.hour).rjust(2, '0'), str(dt.minute).rjust(2, '0'))
            Game_Location = game['profile']['arenaName']
            Game_First_Score = None
            Game_Second_Score = None
            Game_Final_Result = None
            if(game['boxscore']['status'] == '1'):
                # Not Yet Started
                Game_First_Score = '-'
                Game_Second_Score = '-'
                Game_Final_Result = '-'
            elif(game['boxscore']['status'] == '2'):
                # Playing
                Game_First_Score = str(game['boxscore']['{}Score'.format(Our)])
                Game_Second_Score = str(game['boxscore']['{}Score'.format(Oppo)])
                Game_Final_Result = '-'
            elif(game['boxscore']['status'] == '3'):
                # Over
                Game_First_Score = str(game['boxscore']['{}Score'.format(Our[:-4])])
                Game_Second_Score = str(game['boxscore']['{}Score'.format(Oppo[:-4])])
                if(Game_First_Score > Game_Second_Score):
                    Game_Final_Result = '勝'
                else:
                    Game_Final_Result = '負'
            
            # Team Info
            Team_logo = 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Schedule['profile']['abbr'])
            Team_name = '{} {}'.format(Schedule['profile']['city'], Schedule['profile']['displayAbbr'])
            Tema_WL = '{} - {}'.format(Standing['team']['standings']['wins'], Standing['team']['standings']['losses'])
            
            # Oppo Info
            Oppo_name = '{} {}'.format(game[Oppo]['profile']['city'], game[Oppo]['profile']['displayAbbr'])
            Oppo_logo = 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(game[Oppo]['profile']['abbr'])
            Oppo_WL = '{} - {}'.format(game[Oppo]['matchup']['wins'], game[Oppo]['matchup']['losses'])
            
            # URL Info
            Hightlight = None
            Live = None
            for i in game['urls']:
                if(i['type'] == 'Highlights'):
                    Hightlight = i['value']
                elif(i['type'] == 'Live'):
                    Live = i['value']
            print('OppoName: {}'.format(Oppo_name))
            MoreInfo = json.load(open('json/Schedule/MoreInformation.json','r',encoding='utf-8'))
            MoreInfo['body']['contents'][0]['contents'][0]['contents'][0]['url'] = Team_logo
            MoreInfo['body']['contents'][0]['contents'][0]['contents'][1]['text'] = Team_name
            MoreInfo['body']['contents'][0]['contents'][0]['contents'][2]['text'] = Tema_WL
            MoreInfo['body']['contents'][0]['contents'][2]['contents'][0]['url'] = Oppo_logo
            MoreInfo['body']['contents'][0]['contents'][2]['contents'][1]['text'] = Oppo_name
            MoreInfo['body']['contents'][0]['contents'][2]['contents'][2]['text'] = Oppo_WL
            MoreInfo['body']['contents'][2]['contents'][0]['text'] = Game_Final_Result
            MoreInfo['body']['contents'][2]['contents'][1]['text'] = '{} : {}'.format(Game_First_Score, Game_Second_Score)
            MoreInfo['body']['contents'][4]['contents'][0]['contents'][1]['text'] = Game_Date
            MoreInfo['body']['contents'][4]['contents'][1]['contents'][1]['text'] = Game_Time
            MoreInfo['body']['contents'][4]['contents'][2]['contents'][1]['text'] = Game_Location
            if(Live != None):
                Buttom = json.load(open('json/Schedule/GameButtom.json','r',encoding='utf-8'))
                Buttom['action']['label'] = '收看直播'
                Buttom['action']['uri'] = Live
                MoreInfo['footer']['contents'].append(Buttom)
            if(Hightlight != None):
                Buttom = json.load(open('json/Schedule/GameButtom.json','r',encoding='utf-8'))
                Buttom['action']['label'] = 'Hightlights'
                Buttom['action']['uri'] = Hightlight
                MoreInfo['footer']['contents'].append(Buttom)
            Card['contents'].append(MoreInfo)
            break
    return Card