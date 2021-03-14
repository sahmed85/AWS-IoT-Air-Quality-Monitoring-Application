import math
import boto3
import time
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table('AirQualityData')
table_output = dynamodb.Table('AirQualityDataOutput')

BREAKPOINTS = {}

BREAKPOINTS['pm10'] = [{'data': (0,54),    'aqi': (0,50)}, 
                     {'data': (55,154),  'aqi': (51,100)}, 
                     {'data': (155,254), 'aqi': (101,150)}, 
                     {'data': (255,354), 'aqi': (151, 200)}, 
                     {'data': (355,424), 'aqi': (201,300)}, 
                     {'data': (425,504), 'aqi': (301,400)}, 
                     {'data': (505,604), 'aqi': (401,500)}]

BREAKPOINTS['pm2_5'] = [{'data': (0,15.4),     'aqi': (0,50)}, 
                     {'data': (15.5,40.4),   'aqi': (51,100)}, 
                     {'data': (40.5,65.4),   'aqi': (101,150)}, 
                     {'data': (65.5,150.4),  'aqi': (151, 200)}, 
                     {'data': (150.5,250.4), 'aqi': (201,300)}, 
                     {'data': (250.5,350.4), 'aqi': (301,400)}, 
                     {'data': (350.5,500.4), 'aqi': (401,500)}]

BREAKPOINTS['co'] = [{'data': (0.0,4.4),    'aqi': (0,50)}, 
                     {'data': (4.5,9.4),  'aqi': (51,100)}, 
                     {'data': (9.5,12.4), 'aqi': (101,150)}, 
                     {'data': (12.5,15.4), 'aqi': (151, 200)}, 
                     {'data': (15.5,30.4), 'aqi': (201,300)}, 
                     {'data': (30.5,40.4), 'aqi': (301,400)}, 
                     {'data': (40.5,50.4), 'aqi': (401,500)}]

BREAKPOINTS['so2'] = [{'data': (0.000,0.034),    'aqi': (0,50)}, 
                     {'data': (0.035,0.144),  'aqi': (51,100)}, 
                     {'data': (0.145,0.224), 'aqi': (101,150)}, 
                     {'data': (0.225,0.304), 'aqi': (151, 200)}, 
                     {'data': (0.305,0.604), 'aqi': (201,300)}, 
                     {'data': (0.605,0.804), 'aqi': (301,400)}, 
                     {'data': (0.805,1.004), 'aqi': (401,500)}]

def lambda_handler(event, context):

    stations = ['ST102', 'ST105']
    pollutants = ["pm2_5", "pm10", "co", "so2"]

    now = int(time.time())
    timestampDayAgo = now - 86400

    for station in stations:
        AQI = []

        response = table.scan(
            FilterExpression=Key('stationID').eq(station) & Attr('timestamp').gt(timestampDayAgo)
        )

        items = response['Items']

        AQI_output_json = {}
        AQI_output_json["stationID"] = station
        AQI_output_json["timestamp"] = now

        if len(items) > 0:

            for key in pollutants:
                readings = []

                for item in items:
                    readings.append(float(item['data'][key]))

                readings_avg = sum(readings) / len(readings)
                C_p = readings_avg

                for i in range(0,len(BREAKPOINTS[key])):
                    BP_Lo = BREAKPOINTS[key][i]['data'][0]
                    BP_Hi = BREAKPOINTS[key][i]['data'][1]

                    I_Lo = BREAKPOINTS[key][i]['aqi'][0]
                    I_Hi = BREAKPOINTS[key][i]['aqi'][1]

                    if C_p >= BP_Lo and C_p < BP_Hi:
                        I_p = (I_Hi - I_Lo) * (C_p - BP_Lo) / (BP_Hi - BP_Lo) + I_Lo
                        result = int(math.ceil(I_p))

                        AQI_output_json[key] = result
                        AQI_output_json["latitude"] = item['data']["latitude"]
                        AQI_output_json["longitude"] = item['data']["longitude"]
                        AQI.append((key, result))
                        
                        break

            AQI_sorted = sorted(AQI, key=lambda x: x[-1], reverse=True)
            AQI_final = AQI_sorted[0][1]
            main_pollutant = AQI_sorted[0][0]
            AQI_output_json["aqi"] = AQI_final
            AQI_output_json["main_pollutant"] = main_pollutant
            
            table_output.put_item(Item=AQI_output_json)

            outputstring = "For station " + station + ", at time " + str(now) + ", AQI is " + str(AQI_final) + " and main pollutant is " + str(main_pollutant)

            print(outputstring)

    return True
