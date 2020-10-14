import requests, json

def GetTeam():
    url = 'https://tw.global.nba.com/stats2/league/conferenceteamlist.json?locale=zh_TW'
    Data = json.loads(requests.get(url).text)
    res = {}

    Groups = Data['payload']['listGroups']

    for Group in Groups:
        Group_Name = Group['conference']
        if(Group_Name == 'Eastern'):
            Group_Name = '東區 聯盟'
        else:
            Group_Name = '西區 聯盟'
        res[Group_Name] = {}
        Teams = Group['teams']
        for Team in Teams:
            if(Team['profile']['division'] not in res[Group_Name]):
                res[Group_Name][Team['profile']['division']] = [{
                    "name" : '{} {}'.format(Team['profile']['city'].strip(), Team['profile']['displayAbbr'].strip()),
                    "logo" : 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Team['profile']['abbr'].strip()),
                    "code" : Team['profile']['code'].strip()
                }]
            else:
                res[Group_Name][Team['profile']['division']].append({
                    "name" : '{} {}'.format(Team['profile']['city'].strip(), Team['profile']['displayAbbr'].strip()),
                    "logo" : 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Team['profile']['abbr'].strip()),
                    "code" : Team['profile']['code'].strip()
                })

    Card = json.load(open('json/Card.json','r',encoding='utf-8'))
    for Group in res:
        for Teams in res[Group]:
            Team_Bubble = json.load(open('json/Schedule/BubbleTeam.json','r',encoding='utf-8'))
            Team_Bubble['body']['contents'][0]['text'] = Group
            Team_Bubble['body']['contents'][1]['contents'][0]['text'] = Teams
            cnt = 0
            Teams_out = json.load(open('json/Schedule/Teams.json','r',encoding='utf-8'))
            for Team in res[Group][Teams]:
                #print(Team)
                Team_out = json.load(open('json/Schedule/Team.json','r',encoding='utf-8'))
                if(cnt==2):
                    cnt=1
                    Team_Bubble['body']['contents'][1]['contents'].append(Teams_out)
                    Teams_out = json.load(open('json/Schedule/Teams.json','r',encoding='utf-8'))
                else:
                    cnt+=1
                Team_out['contents'][0]['url'] = Team['logo']
                Team_out['contents'][1]['text'] = Team['name']
                Team_out['contents'][0]['action']['data'] = 'SelectScheduleFrom {}'.format(Team['code'])
                Team_out['contents'][1]['action']['data'] = 'SelectScheduleFrom {}'.format(Team['code'])
                Teams_out['contents'].append(Team_out)
            Team_Bubble['body']['contents'][1]['contents'].append(Teams_out)
            Card['contents'].append(Team_Bubble)
    return Card

def GetTeam2():
    url = 'https://tw.global.nba.com/stats2/league/conferenceteamlist.json?locale=zh_TW'
    Data = json.loads(requests.get(url).text)
    res = {}

    Groups = Data['payload']['listGroups']

    for Group in Groups:
        Group_Name = Group['conference']
        if(Group_Name == 'Eastern'):
            Group_Name = '東區 聯盟'
        else:
            Group_Name = '西區 聯盟'
        res[Group_Name] = {}
        Teams = Group['teams']
        for Team in Teams:
            if(Team['profile']['division'] not in res[Group_Name]):
                res[Group_Name][Team['profile']['division']] = [{
                    "name" : '{} {}'.format(Team['profile']['city'].strip(), Team['profile']['displayAbbr'].strip()),
                    "logo" : 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Team['profile']['abbr'].strip()),
                    "code" : Team['profile']['code'].strip()
                }]
            else:
                res[Group_Name][Team['profile']['division']].append({
                    "name" : '{} {}'.format(Team['profile']['city'].strip(), Team['profile']['displayAbbr'].strip()),
                    "logo" : 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Team['profile']['abbr'].strip()),
                    "code" : Team['profile']['code'].strip()
                })

    Card = json.load(open('json/Card.json','r',encoding='utf-8'))
    for Group in res:
        for Teams in res[Group]:
            Team_Bubble = json.load(open('json/Schedule/BubbleTeam.json','r',encoding='utf-8'))
            Team_Bubble['body']['contents'][0]['text'] = Group
            Team_Bubble['body']['contents'][1]['contents'][0]['text'] = Teams
            cnt = 0
            Teams_out = json.load(open('json/Schedule/Teams.json','r',encoding='utf-8'))
            for Team in res[Group][Teams]:
                #print(Team)
                Team_out = json.load(open('json/Schedule/Team.json','r',encoding='utf-8'))
                if(cnt==2):
                    cnt=1
                    Team_Bubble['body']['contents'][1]['contents'].append(Teams_out)
                    Teams_out = json.load(open('json/Schedule/Teams.json','r',encoding='utf-8'))
                else:
                    cnt+=1
                Team_out['contents'][0]['url'] = Team['logo']
                Team_out['contents'][1]['text'] = Team['name']
                Team_out['contents'][0]['action']['data'] = 'SelectPlayerFrom {}'.format(Team['code'])
                Team_out['contents'][1]['action']['data'] = 'SelectPlayerFrom {}'.format(Team['code'])
                Teams_out['contents'].append(Team_out)
            Team_Bubble['body']['contents'][1]['contents'].append(Teams_out)
            Card['contents'].append(Team_Bubble)
    return Card

def GetTeam3():
    url = 'https://tw.global.nba.com/stats2/league/conferenceteamlist.json?locale=zh_TW'
    Data = json.loads(requests.get(url).text)
    res = {}

    Groups = Data['payload']['listGroups']

    for Group in Groups:
        Group_Name = Group['conference']
        if(Group_Name == 'Eastern'):
            Group_Name = '東區 聯盟'
        else:
            Group_Name = '西區 聯盟'
        res[Group_Name] = {}
        Teams = Group['teams']
        for Team in Teams:
            if(Team['profile']['division'] not in res[Group_Name]):
                res[Group_Name][Team['profile']['division']] = [{
                    "name" : '{} {}'.format(Team['profile']['city'].strip(), Team['profile']['displayAbbr'].strip()),
                    "logo" : 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Team['profile']['abbr'].strip()),
                    "code" : Team['profile']['code'].strip()
                }]
            else:
                res[Group_Name][Team['profile']['division']].append({
                    "name" : '{} {}'.format(Team['profile']['city'].strip(), Team['profile']['displayAbbr'].strip()),
                    "logo" : 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Team['profile']['abbr'].strip()),
                    "code" : Team['profile']['code'].strip()
                })

    Card = json.load(open('json/Card.json','r',encoding='utf-8'))
    for Group in res:
        for Teams in res[Group]:
            Team_Bubble = json.load(open('json/Schedule/BubbleTeam.json','r',encoding='utf-8'))
            Team_Bubble['body']['contents'][0]['text'] = Group
            Team_Bubble['body']['contents'][1]['contents'][0]['text'] = Teams
            cnt = 0
            Teams_out = json.load(open('json/Schedule/Teams.json','r',encoding='utf-8'))
            for Team in res[Group][Teams]:
                #print(Team)
                Team_out = json.load(open('json/Schedule/Team.json','r',encoding='utf-8'))
                if(cnt==2):
                    cnt=1
                    Team_Bubble['body']['contents'][1]['contents'].append(Teams_out)
                    Teams_out = json.load(open('json/Schedule/Teams.json','r',encoding='utf-8'))
                else:
                    cnt+=1
                Team_out['contents'][0]['url'] = Team['logo']
                Team_out['contents'][1]['text'] = Team['name']
                Team_out['contents'][0]['action']['data'] = 'SelectLeaderFrom {}'.format(Team['code'])
                Team_out['contents'][1]['action']['data'] = 'SelectleaderFrom {}'.format(Team['code'])
                Teams_out['contents'].append(Team_out)
            Team_Bubble['body']['contents'][1]['contents'].append(Teams_out)
            Card['contents'].append(Team_Bubble)
    return Card