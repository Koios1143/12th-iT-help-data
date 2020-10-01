import datetime,csv,json,requests,os
from logger import logger
from add_pos import add_pos
data_folder = str(os.getcwd()) + '/data/'

def update():
    position_out = open(data_folder + 'csv/positions.csv','r',newline='')
    nowtime = datetime.datetime.now()
    pasttime = datetime.datetime.strptime(list(csv.reader(position_out))[0][6],'%Y/%m/%d %H:%M:%S')
    minutes = datetime.timedelta(minutes=30)
    if(nowtime-pasttime >= minutes):
        # download maskdata.csv
        logger.info('========== downloading ==========')
        url = 'https://data.nhi.gov.tw/resource/mask/maskdata.csv'
        request_data = requests.get(url).content.decode('utf-8')
        # update maskdata.csv
        try:
            with open(data_folder + 'csv/maskdata.csv','w') as maskdata:
                logger.info('open maskdata.csv => Success')
                maskdata.write(request_data)
                logger.info('========== Download Success ==========')
        except:
            logger.warning('open maskdata.csv => Failed')
            logger.warning('========== Download Failed ==========')
            return False
        # update positions.csv
        res = add_pos()
        if(res == True):
            logger.info('create positions.csv => Success')
            return True
        else:
            logger.warning('create positions.csv => Failed')
            return False