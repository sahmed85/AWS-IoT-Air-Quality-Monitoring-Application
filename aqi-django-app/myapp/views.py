from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.shortcuts import redirect
from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, Permission, User
from django.db.models import Count, Min, Sum, Avg
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import sys, os
# import pwd
# import grp
# import json, simplejson
# from datetime import datetime, date, timedelta
# from dateutil import relativedelta
import time
from django.shortcuts import render
# import csv
# import requests
# import operator
# from lxml.html import fromstring
# import glob
# import zipfile
# import random
# import re
# import sha
# from .models import *
import boto3
from django.utils import timezone
# import json
from boto3.dynamodb.conditions import Key, Attr
# import datetime
# from dateutil.tz import tzoffset
# import the csv lib 
import csv

sys.path.append(os.path.abspath(os.path.join('..', 'utils')))
from env import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_REGION

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=AWS_REGION)

table = dynamodb.Table('AirQualityData')
table_output = dynamodb.Table('AirQualityDataOutput')

def home_page(request):
    #ts=datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    #timestampold=str(ts.strftime("%Y-%m-%dT:%H:%M:%S"))
    now=int(time.time())
    timestampold=now-86400

    response = table_output.scan(
        FilterExpression=Attr('timestamp').gt(timestampold)
    )

    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-computed.html', variables)


def raw_data_page(request):
    #ts=datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    #timestampold=str(ts.strftime("%Y-%m-%dT:%H:%M:%S"))
    now=int(time.time())
    timestampold=now-86400

    response = table.scan(
        FilterExpression=Attr('timestamp').gt(timestampold)
    )

    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-dashboard.html', variables)


def filter_data(request,asset_filter):
    now=int(time.time())
    timestampold=now-86400

    if asset_filter=='all':
        stationID=''
        response = table_output.scan(
            FilterExpression=Attr('timestamp').gt(timestampold)
        )
    elif asset_filter=='ST102':
        stationID='ST102'
        response = table_output.scan(
            FilterExpression=Key('stationID').eq(stationID) & Attr('timestamp').gt(timestampold)
        )
    elif asset_filter=='ST105':
        stationID='ST105'
        response = table_output.scan(
            FilterExpression=Key('stationID').eq(stationID) & Attr('timestamp').gt(timestampold)
        )
    
    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-computed.html',variables)


def filter_data_time(request,time_filter):
    timestampold=''
    now=int(time.time())
    if time_filter=='1':
        timestampold=now - 60
    elif time_filter=='2':
        timestampold=now - 900
    elif time_filter=='3':
        timestampold=now - 3600
    elif time_filter=='4':
        timestampold=now - 21600
    elif time_filter=='5':
        timestampold=now - 43200
    elif time_filter=='6':
        timestampold=now - 86400
            
    print(timestampold)
    response = table_output.scan(
            FilterExpression=Attr('timestamp').gt(timestampold)
        )
    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-computed.html',variables)

def filter_raw_data(request,asset_filter):
    now=int(time.time())
    timestampold=now-86400

    if asset_filter=='all':
        stationID=''
        response = table.scan(
            FilterExpression=Attr('timestamp').gt(timestampold)
        )
    elif asset_filter=='ST102':
        stationID='ST102'
        response = table.scan(
            FilterExpression=Key('stationID').eq(stationID) & Attr('timestamp').gt(timestampold)
        )
    elif asset_filter=='ST105':
        stationID='ST105'
        response = table.scan(
            FilterExpression=Key('stationID').eq(stationID) & Attr('timestamp').gt(timestampold)
        )
    
    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-dashboard.html',variables)


def filter_raw_data_time(request,time_filter):
    timestampold=''
    now=int(time.time())
    if time_filter=='1':
        timestampold=now - 60
    elif time_filter=='2':
        timestampold=now - 900
    elif time_filter=='3':
        timestampold=now - 3600
    elif time_filter=='4':
        timestampold=now - 21600
    elif time_filter=='5':
        timestampold=now - 43200
    elif time_filter=='6':
        timestampold=now - 86400
            
    print(timestampold)
    response = table.scan(
            FilterExpression=Attr('timestamp').gt(timestampold)
        )
    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-dashboard.html',variables)    

def dashboard_home(request):    
    variables = RequestContext(request, {})
    return render_to_response('aqi-dashboard.html', variables)

# this function will create a csv file of all the raw data for all stations
def report_page(request):
    # return a MIME type, text/csv to the requester
    # Create the HTTPResponse object with the CSV header
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename = "rawdata.csv"'
    writer = csv.writer(response)
    writer.writerow(['StationID','timestamp','pm10','pm2_5','so2'])
    # fetch the data from the database table and use writerow member function to add to the csv rows
    dyanamodb_response = table.scan()
    items = dyanamodb_response['Items']
    # loop through each item returned from DynamoDB and write the csv row
    for item in items:
        writer.writerow([item['stationID'],int(item['timestamp']),float(item['data']['pm10']),float(item['data']['pm2_5']),float(item['data']['so2'])])
    # return the csv
    return response


# this function will render the graph view for real time data visualization
def analytics_page(request):
    # return the template raw-data-graphs.html 
    return render(request, 'raw-data-graphs.html', {})



