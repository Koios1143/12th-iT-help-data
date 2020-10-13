import requests, json

def GetPlayer(name):
    url = 'https://tw.global.nba.com/stats2/player/stats.json?ds=profile&locale=zh_TW&playerCode={}'.format(name)
    Data = json.loads(requests.get(url).text)['payload']
    Data_Player = Data['player']
    Data_PlayerProfile = Data_Player['playerProfile']
    Data_TeamProfile = Data_Player['teamProfile']
    Data_StatAvg = Data_Player['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']
    
    # PlayerCard needs
    PlayerName = Data_PlayerProfile['displayName']
    PlayerTeam = '{} {}'.format(Data_TeamProfile['city'], Data_TeamProfile['displayAbbr'])
    PlayerPosition = Data_PlayerProfile['position']
    PlayerCode = Data_PlayerProfile['jerseyNo']
    PlayerId = Data_PlayerProfile['playerId']

    # PlayerProfile needs
    PlayerHW = '{} 公尺 / {}'.format(Data_PlayerProfile['height'], Data_PlayerProfile['weight'])
    PlayerdraftYear = Data_PlayerProfile['draftYear']
    PlayExperience = Data_PlayerProfile['experience']

    # PlayerAvg needs
    PlayerGames = Data_StatAvg['games']
    PlayerGameStarted = Data_StatAvg['gamesStarted']
    PlayerMinsPg = Data_StatAvg['minsPg']
    PlayerFgpct = Data_StatAvg['fgpct']
    PlayerTppct = Data_StatAvg['tppct']
    PlayerFtpct = Data_StatAvg['ftpct']
    PlayerRebsPg = Data_StatAvg['rebsPg']
    PlayerAssistsPg = Data_StatAvg['assistsPg']
    PlayerPointsPg = Data_StatAvg['pointsPg']

    # Open files
    PlayerDetail = json.load(open('json/Player/PlayerDetail.json','r',encoding='utf-8'))
    PlayerDetail_Card = json.load(open('json/Player/PlayerDetail-Card.json','r',encoding='utf-8'))
    PlayerDetail_Profile = json.load(open('json/Player/PlayerDetail-Profile.json','r',encoding='utf-8'))
    PlayerDetail_Avg = json.load(open('json/Player/PlayerDetail-Avg.json','r',encoding='utf-8'))
    Seperater = json.load(open('json/Player/Seperater.json','r',encoding='utf-8'))

    PlayerBox = PlayerDetail['body']['contents']

    # Card
    PlayerDetail_Card['contents'][0]['contents'][0]['url'] = 'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{}.png'.format(PlayerId)
    PlayerDetail_Card['contents'][2]['contents'][0]['text'] = PlayerName
    PlayerDetail_Card['contents'][2]['contents'][1]['text'] = PlayerTeam
    PlayerDetail_Card['contents'][2]['contents'][2]['text'] = PlayerPosition
    PlayerDetail_Card['contents'][3]['contents'][0]['text'] = PlayerCode

    # Profile
    PlayerDetail_Profile['contents'][2]['contents'][1]['text'] = PlayerHW
    PlayerDetail_Profile['contents'][3]['contents'][1]['text'] = PlayerdraftYear
    PlayerDetail_Profile['contents'][4]['contents'][1]['text'] = PlayExperience

    # Avg
    PlayerDetail_Avg['contents'][2]['contents'][1]['text'] = str(PlayerGames)
    PlayerDetail_Avg['contents'][3]['contents'][1]['text'] = str(PlayerGameStarted)
    PlayerDetail_Avg['contents'][4]['contents'][1]['text'] = str(PlayerMinsPg)
    PlayerDetail_Avg['contents'][5]['contents'][1]['text'] = str(PlayerFgpct)
    PlayerDetail_Avg['contents'][6]['contents'][1]['text'] = str(PlayerTppct)
    PlayerDetail_Avg['contents'][7]['contents'][1]['text'] = str(PlayerFtpct)
    PlayerDetail_Avg['contents'][8]['contents'][1]['text'] = str(PlayerRebsPg)
    PlayerDetail_Avg['contents'][9]['contents'][1]['text'] = str(PlayerAssistsPg)
    PlayerDetail_Avg['contents'][10]['contents'][1]['text'] = str(PlayerPointsPg)

    PlayerDetail['body']['contents'].append(PlayerDetail_Card)
    PlayerDetail['body']['contents'].append(Seperater)
    PlayerDetail['body']['contents'].append(PlayerDetail_Profile)
    PlayerDetail['body']['contents'].append(Seperater)
    PlayerDetail['body']['contents'].append(PlayerDetail_Avg)
    PlayerDetail['body']['contents'].append(Seperater)
    PlayerDetail['footer']['contents'][0]['action']['uri'] = 'https://tw.global.nba.com/players/#!/{}'.format(name)

    return PlayerDetail