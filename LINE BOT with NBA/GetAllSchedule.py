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

def GetAllSchedule(Team):
    url = 'https://tw.global.nba.com/stats2/team/schedule.json?countryCode=TW&locale=zh_TW&teamCode={}'.format(Team)
    Schedule = json.loads(requests.get(url).text)['payload']
    url = 'https://tw.global.nba.com/stats2/team/standing.json?locale=zh_TW&teamCode={}'.format(Team)
    Standing = json.loads(requests.get(url).text)['payload']

    year = str(Schedule['season']['year'])
    Card = json.load(open('json/Card.json','r',encoding='utf-8'))
    cnt = 0
    for monthGroup in Schedule['monthGroups']:
        Schedule_out = json.load(open('json/Schedule/Schedule.json', 'r', encoding='utf-8'))
        month = monthGroup['name'][:-1]
        if(month == '一'):
            year = str(int(year)+1)
        for game in monthGroup['games']:
            # Team logo
            Schedule_out['body']['contents'][0]['contents'][0]['url'] = 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Schedule['profile']['abbr'])

            # Team name
            Schedule_out['body']['contents'][0]['contents'][1]['contents'][1]['text'] = '{} {}'.format(Schedule['profile']['city'], Schedule['profile']['displayAbbr'])

            # Team Rank in Group
            Schedule_out['body']['contents'][0]['contents'][1]['contents'][2]['text'] = '{}聯盟中排名#{}'.format(Schedule['profile']['displayConference'], Standing['team']['standings']['confRank'])

            # Team coach
            Schedule_out['body']['contents'][0]['contents'][1]['contents'][3]['text'] = '總教練: {}'.format(Standing['team']['coach']['headCoach'])

            # Team W/L
            Schedule_out['body']['contents'][2]['contents'][0]['text'] = '{} - {}'.format(Standing['team']['standings']['wins'], Standing['team']['standings']['losses'])

            # Game month
            Schedule_out['body']['contents'][4]['contents'][0]['text'] = '{} 年 {} 月'.format(year, month)

            # Games Info
            Game_Info = json.load(open('json/Schedule/GameInfo.json','r',encoding='utf-8'))
            # Game Time
            Game_Time = tz_from_utc_ms_ts(float(game['profile']['utcMillis']) ,pytz.timezone('Asia/Taipei'))
            Game_Info['contents'][0]['text'] = '{}/{}'.format(str(Game_Time.month).rjust(2, '0'), str(Game_Time.day).rjust(2, '0'))
            Game_Info['contents'][1]['text'] = '{}:{}'.format(str(Game_Time.hour).rjust(2, '0'), str(Game_Time.minute).rjust(2, '0'))
            
            # Game opponent
            if(game['awayTeam']['profile']['displayAbbr'] == Standing['team']['profile']['displayAbbr']):
                Game_Info['contents'][2]['text'] = game['homeTeam']['profile']['displayAbbr']
            else:
                Game_Info['contents'][2]['text'] = game['awayTeam']['profile']['displayAbbr']
            
            # PostBack Action
            Game_Info['contents'][3]['contents'][0]['action']['data'] = 'Schedule {} {}'.format(Team, game['profile']['dateTimeEt'])
            Schedule_out['body']['contents'].append(Game_Info)
        Card['contents'].append(Schedule_out)
        cnt+=1
        if(cnt>=10):
            return Card
    return Card