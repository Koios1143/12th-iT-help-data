import json, requests

def GetTeamLeaders(Team):
    url = 'https://tw.global.nba.com/stats2/team/leader.json?locale=zh_TW&teamCode={}'.format(Team)
    Data = json.loads(requests.get(url).text)['payload']
    pointLeader = Data['pointLeader']['players']
    reboundLeader = Data['reboundLeader']['players']
    assistLeader = Data['assistLeader']['players']
    blockLeader = Data['blockLeader']['players']
    stealLeader = Data['stealLeader']['players']
    threePtPctLeader = Data['threePtPctLeader']['players']
    fgPctLeader = Data['fgPctLeader']['players']
    ftPctLeader = Data['ftPctLeader']['players']
    minLeader = Data['minLeader']['players']

    url = 'https://tw.global.nba.com/stats2/team/standing.json?locale=zh_TW&teamCode={}'.format(Team)
    Data2 = json.loads(requests.get(url).text)['payload']['team']
    profile = Data2['profile']
    standings = Data2['standings']
    
    Leaders = [pointLeader, reboundLeader, assistLeader, blockLeader, stealLeader, threePtPctLeader, fgPctLeader, ftPctLeader, minLeader]
    types = ['平均得分', '平均籃板', '平均助攻','阻攻/場', '抄截/場', '三分球%', '投籃%', '罰球%', '場均時間']
    Card = json.load(open('json/Card.json','r',encoding='utf-8'))
    
    # Cover needs
    Team_abbr = profile['abbr']
    Team_Name = '{} {}'.format(profile['city'], profile['displayAbbr'])
    Team_Rank = '{}聯盟中排名#{}'.format(profile['displayConference'], standings['confRank'])
    Team_WL = '{} 勝 - {} 負'.format(standings['wins'], standings['losses'])

    # Set Cover
    cover = json.load(open('json/Team/cover.json','r',encoding='utf-8'))
    cover['hero']['url'] = 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Team_abbr)
    cover_box = cover['body']['contents'][0]['contents'][0]['contents']
    cover_box[0]['text'] = Team_Name
    cover_box[1]['text'] = Team_Rank
    cover_box[2]['text'] = Team_WL
    Card['contents'].append(cover)

    # Set leader
    for i in range(len(Leaders)):
        NowSelectedLeder = Leaders[i]
        LeaderOutput = json.load(open('json/Team/leader.json','r',encoding='utf-8'))
        LeaderOutput['body']['contents'][0]['contents'][0]['text'] = types[i]
        for player in NowSelectedLeder:
            player_output = json.load(open('json/Team/playerInfo.json','r',encoding='utf-8'))
            player_output['contents'][0]['text'] = player['rank']
            player_output['contents'][1]['text'] = player['profile']['displayName']
            player_output['contents'][2]['text'] = player['value']
            LeaderOutput['body']['contents'].append(player_output)
        
        Card['contents'].append(LeaderOutput)
    return Card
