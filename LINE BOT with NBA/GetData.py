import requests,datetime,json,pytz

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

def Get_Card(date):
    url = 'https://tw.global.nba.com/stats2/scores/daily.json?countryCode=TW&gameDate={}&locale=zh_TW&tz=%2B8'
    Data = requests.get(url.format(date))
    Data = json.loads(Data.text,encoding='utf-8')

    # Game Basic Information
    payload = Data['payload']
    NBA_season = payload['season']
    NBA_date = payload['date']
    nextAvailableDateMillis = float(payload['nextAvailableDateMillis'])
    nextAvailableDate = tz_from_utc_ms_ts(nextAvailableDateMillis, pytz.timezone('Asia/Taipei'))
    
    # No game this day
    if(NBA_date == None):
        responce = json.load(open('json/Score/NoGame.json','r',encoding='utf-8'))
        responce['body']['contents'][2]['text'] = str(nextAvailableDate)[:-6]
        responce['footer']['contents'][0]['action']['data'] = 'Get{}'.format(str(nextAvailableDate)[:-6])
        return responce
    
    # Search Games
    NBA_games = NBA_date['games']
    Card = json.load(open('json/Card.json','r',encoding='utf-8'))
    for NBA_game in NBA_games:
        bubble = json.load(open('json/Score/Bubble.json','r',encoding='utf-8'))

        # Get Game profile
        NBA_profile = NBA_game['profile']
        NBA_boxscore = NBA_game['boxscore']
        NBA_gameId = NBA_profile['gameId']

        # Home/Away Team
        NBA_homeTeam = NBA_game['homeTeam']
        NBA_awayTeam = NBA_game['awayTeam']

        # HomeTeam - Profile
        Home_profile = NBA_homeTeam['profile']
        Home_name = Home_profile['displayAbbr']
        Home_conference = Home_profile['displayConference']
        Home_division = Home_profile['division']
        Home_id = Home_profile['id']
        Home_abbr = Home_profile['abbr']
        Home_logo_url = 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Home_abbr)

        # AwayTeam - Profile
        Away_profile = NBA_awayTeam['profile']
        Away_name = Away_profile['displayAbbr']
        Away_conference = Away_profile['displayConference']
        Away_division = Away_profile['division']
        Away_id = Away_profile['id']
        Away_abbr = Away_profile['abbr']
        Away_logo_url = 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Away_abbr)

        # HomeTeam - matchup
        Home_matchup = NBA_homeTeam['matchup']
        # 區排
        Home_confRank = Home_matchup['confRank']
        # 組排
        Home_divRank = Home_matchup['divRank']
        Home_losses = Home_matchup['losses']
        Home_wins = Home_matchup['wins']

        # AwayTeam - matchup
        Away_matchup = NBA_awayTeam['matchup']
        # 區排
        Away_confRank = Away_matchup['confRank']
        # 組排
        Away_divRank = Away_matchup['divRank']
        Away_losses = Away_matchup['losses']
        Away_wins = Away_matchup['wins']

        # Not yet started
        if(NBA_boxscore['status'] == '1'):
            responce = json.load(open('json/Score/NotYetStarted.json','r',encoding='utf-8'))
            
            # Set HomeTeam responce
            responce['body']['contents'][0]['contents'][0]['contents'][1]['url'] = str(Home_logo_url)
            responce['body']['contents'][0]['contents'][0]['contents'][2]['text'] = '{} - {}'.format(Home_wins, Home_losses)
            
            # Set AwayTeam responce
            responce['body']['contents'][0]['contents'][2]['contents'][0]['contents'][1]['url'] = str(Away_logo_url)
            responce['body']['contents'][0]['contents'][2]['contents'][0]['contents'][2]['text'] = '{} - {}'.format(Away_wins, Away_losses)
            
            # Set URL
            responce['footer']['contents'][0]['contents'][0]['action']['uri'] = 'https://tw.global.nba.com/preview/#!/'.format(NBA_gameId)

            Card['contents'].append(responce)
            continue
        
        # URLs
        NBA_Hightlight = None
        NBA_Live = None
        if(len(NBA_game['urls']) > 0):
            NBA_Hightlight = NBA_game['urls'][0]['value']
            NBA_Live = NBA_game['urls'][1]['value']

        # HomeTeam - score
        Home_score = NBA_homeTeam['score']
        Home_main_score = []
        for i in range(4):
            Home_main_score.append(Home_score['q{}Score'.format(i+1)])
        for i in range(10):
            Home_main_score.append(Home_score['ot{}Score'.format(i+1)])
        
        Home_totScore = Home_score['score']

        # Home - pointGameLeader
        Home_pointGameLeader = NBA_homeTeam['pointGameLeader']
        Home_pointGameLeader_Name = Home_pointGameLeader['profile']['displayName']
        Home_pointGameLeader_Points = Home_pointGameLeader['statTotal']['points']

        # Home - assistGameLeader
        Home_assistGameLeader = NBA_homeTeam['assistGameLeader']
        Home_assistGameLeader_Name = Home_assistGameLeader['profile']['displayName']
        Home_assistGameLeader_Assists = Home_assistGameLeader['statTotal']['assists']

        # Home - reboundGameLeader
        Home_reboundGameLeader = NBA_homeTeam['reboundGameLeader']
        Home_reboundGameLeader_Name = Home_reboundGameLeader['profile']['displayName']
        Home_reboundGameLeader_Rebs = Home_reboundGameLeader['statTotal']['rebs']

        # AwayTeam - score
        Away_score = NBA_awayTeam['score']
        Away_main_score = []
        for i in range(4):
            Away_main_score.append(Away_score['q{}Score'.format(i+1)])
        for i in range(10):
            Away_main_score.append(Away_score['ot{}Score'.format(i+1)])
        Away_totScore = Away_score['score']

        # Away - pointGameLeader
        Away_pointGameLeader = NBA_awayTeam['pointGameLeader']
        Away_pointGameLeader_Name = Away_pointGameLeader['profile']['displayName']
        Away_pointGameLeader_Points = Away_pointGameLeader['statTotal']['points']

        # Away - assistGameLeader
        Away_assistGameLeader = NBA_awayTeam['assistGameLeader']
        Away_assistGameLeader_Name = Away_assistGameLeader['profile']['displayName']
        Away_assistGameLeader_Assists = Away_assistGameLeader['statTotal']['assists']

        # Away - reboundGameLeader
        Away_reboundGameLeader = NBA_awayTeam['reboundGameLeader']
        Away_reboundGameLeader_Name = Away_reboundGameLeader['profile']['displayName']
        Away_reboundGameLeader_Rebs = Away_reboundGameLeader['statTotal']['rebs']

        # Set HomeTeam Bubble
        bubble['body']['contents'][0]['contents'][0]['contents'][1]['url'] = str(Home_logo_url)
        bubble['body']['contents'][0]['contents'][0]['contents'][2]['text'] = '{} - {}'.format(Home_wins, Home_losses)

        # Set Total Score
        bubble['body']['contents'][0]['contents'][1]['contents'][2]['text'] = str(Home_totScore)
        bubble['body']['contents'][0]['contents'][2]['contents'][2]['text'] = str(Away_totScore)

        # Set AwayTeam Bubble
        bubble['body']['contents'][0]['contents'][3]['contents'][0]['contents'][1]['url'] = str(Away_logo_url)
        bubble['body']['contents'][0]['contents'][3]['contents'][0]['contents'][2]['text'] = '{} - {}'.format(Away_wins, Away_losses)

        # Set Name
        bubble['body']['contents'][2]['contents'][0]['contents'][1]['text'] = Home_name
        bubble['body']['contents'][2]['contents'][0]['contents'][2]['text'] = Away_name
        bubble['body']['contents'][4]['contents'][1]['contents'][0]['text'] = Home_name
        bubble['body']['contents'][4]['contents'][3]['contents'][0]['text'] = Away_name

        # Set Scores
        for i in range(4):
            Score = json.load(open('json/Score/Score.json','r',encoding='utf-8'))
            Score['contents'][0]['text'] = '第{}局'.format(i+1)
            Score['contents'][1]['text'] = str(Home_main_score[i])
            Score['contents'][2]['text'] = str(Away_main_score[i])
            bubble['body']['contents'][2]['contents'].append(Score)
        for i in range(4,14):
            if(Home_main_score[i] == 0 and Away_main_score[i] == 0):
                break
            else:
                Score = json.load(open('json/Score/Score.json','r',encoding='utf-8'))
                Score['contents'][0]['text'] = 'OT{}'.format(i-4)
                Score['contents'][1]['text'] = str(Home_main_score[i])
                Score['contents'][2]['text'] = str(Away_main_score[i])
                bubble['body']['contents'][2]['contents'].append(Score)

        # Set Kings
        # Set HomeTeam pointGameLeader
        bubble['body']['contents'][4]['contents'][1]['contents'][1]['text'] = Home_pointGameLeader_Name
        bubble['body']['contents'][4]['contents'][2]['contents'][1]['text'] = str(Home_pointGameLeader_Points)
        # Set HomeTeam reboundGameLeader
        bubble['body']['contents'][4]['contents'][1]['contents'][2]['text'] = Home_reboundGameLeader_Name
        bubble['body']['contents'][4]['contents'][2]['contents'][2]['text'] = str(Home_reboundGameLeader_Rebs)
        # Set HomeTeam assistGameLeader
        bubble['body']['contents'][4]['contents'][1]['contents'][3]['text'] = Home_assistGameLeader_Name
        bubble['body']['contents'][4]['contents'][2]['contents'][3]['text'] = str(Home_assistGameLeader_Assists)
        # Set AwayTeam pointGameLeader
        bubble['body']['contents'][4]['contents'][3]['contents'][1]['text'] = Away_pointGameLeader_Name
        bubble['body']['contents'][4]['contents'][4]['contents'][1]['text'] = str(Away_pointGameLeader_Points)
        # Set AwayTeam reboundGameLeader
        bubble['body']['contents'][4]['contents'][3]['contents'][2]['text'] = Away_reboundGameLeader_Name
        bubble['body']['contents'][4]['contents'][4]['contents'][2]['text'] = str(Away_reboundGameLeader_Rebs)
        # Set AwayTeam assistGameLeader
        bubble['body']['contents'][4]['contents'][3]['contents'][3]['text'] = Away_assistGameLeader_Name
        bubble['body']['contents'][4]['contents'][4]['contents'][3]['text'] = str(Away_assistGameLeader_Assists)

        # Set URLs
        if(NBA_Live is not None):
            Buttom = json.load(open('json/Score/GameButtom.json','r',encoding='utf-8'))
            Buttom['contents'][0]['action']['label'] = '收看直播'
            Buttom['contents'][0]['action']['uri'] = str(NBA_Live)
            bubble['footer']['contents'].append(Buttom)
        if(NBA_gameId is not None):
            Buttom = json.load(open('json/Score/GameButtom.json','r',encoding='utf-8'))
            Buttom['contents'][0]['action']['label'] = '數據統計'
            Buttom['contents'][0]['action']['uri'] = 'https://tw.global.nba.com/boxscore/#!/{}'.format(NBA_gameId)
            bubble['footer']['contents'].append(Buttom)
        if(NBA_Hightlight is not None):
            Buttom = json.load(open('json/Score/GameButtom.json','r',encoding='utf-8'))
            Buttom['contents'][0]['action']['label'] = 'Hightlights'
            Buttom['contents'][0]['action']['uri'] = str(NBA_Hightlight)
            bubble['footer']['contents'].append(Buttom)

        Card['contents'].append(bubble)
    print(Card)
    return Card
#Get_Card('2020-10-10')