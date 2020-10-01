import csv,os
from logger import logger
from get_distance import distance
data_folder = str(os.getcwd()) + '/data/'

def get_mask(event):
    if(event.message.type == 'location'):
        try:
            positions = open(data_folder + 'csv/positions.csv','r')
            logger.info('open positions.csv => Success')
        except:
            logger.warning('open positions.csv => Failed')
        radius = 1.0 #km
        result = []
        mask_data = csv.reader(positions)
        lat1 = float(event.message.latitude)
        lng1 = float(event.message.longitude)
        for data in mask_data:
            try:
                lat2 = float(data[7])
                lng2 = float(data[8])
            except:
                continue
            if(distance(lat1, lng1, lat2, lng2) <= radius):
                result.append(data)
        result = sorted(result, key=lambda x:(int(x[4]) + int(x[5]))*-1)
        return result[:10] # 10 maximun