import csv,json,os
from logger import logger
data_folder = str(os.getcwd()) + '/data/'

def add_pos():
    # read maskdata
    try:
        maskdata = open(data_folder + 'csv/maskdata.csv','r',newline='')
        logger.info('open maskdata.csv => Success')
    except:
        logger.warning('open maskdata.csv => Failed')
        return False
    # read dict table
    try:
        pos_data = open(data_folder + 'json/positions.json','r',newline='')
        logger.info('open positions.json => Success')
    except:
        logger.warning('open positions.json => Failed')
        return False
    # update positions
    try:
        out = open(data_folder + 'csv/positions.csv','w')
        logger.info('open positions.csv => Success')
    except:
        logger.warning('open positions.csv => Failed')
        return False
    sheets = csv.reader(maskdata)
    pos = json.load(pos_data)
    writer = csv.writer(out)
    for sheet in sheets:
        arr = sheet
        try:
            lat = pos[sheet[0]]['lat']
            lng = pos[sheet[0]]['lng']
        except KeyError:
            logger.warning('[add_pos] KeyError in line ' + str(sheet[0]))
            continue
        arr.append(lat)
        arr.append(lng)
        writer.writerow(arr)
    return True