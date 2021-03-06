#!/usr/bin/env python
# -*- coding: utf-8

import urllib2, json, sys, smtplib
import config

#####################################################################
# Small python script to query the weather underground API and parse
# that data as desired.  The approach is object oriented so that
# the script is versatile and can be easily altered to pull and parse
# various other json objects from the API.  The result is then 
# e-mailed or texted to the recipient.
#####################################################################

# Validate input before continuing
if len(sys.argv) >= 2:
    zipcode = sys.argv[1]
    if zipcode.isdigit() == False:
        print 'Zip codes are numeric!'
        sys.exit(1)
    if len(zipcode) != 5:
        print 'Zip codes are 5 digits!'
        sys.exit(1)
else:
    print 'You must supply the zip code!'
    sys.exit(1)

# Lowercase first letter in string
def subitalize(s):
    return s[0].lower() + s[1:]

# Fetch the subkey of a dictionary
def fetch_subkey(d, keylist):
    if keylist[0] not in d: return False
    return d[keylist[0]] if len(keylist) == 1 else fetch_subkey(d[keylist[0]], keylist[1:])

# Get the current conditions for the supplied zipcode and type of data
def get_data(zipcode, dtype):
    if dtype == 'forecast':
        url = 'conditions/forecast'
    if dtype == 'almanac':
        url = 'almanac/conditions'
    if dtype == 'astronomy':
        url = 'astronomy'

    json_string = urllib2.urlopen('http://api.wunderground.com/api/%s/%s/q/%s.json' % (config.APIKEY, url, zipcode)).read()
    parsed_json = json.loads(json_string)

    if fetch_subkey(parsed_json, ['response', 'features', dtype])  != 1:
        print 'Error fetching json! Response missing...'
        sys.exit(1)
    return parsed_json

def get_chances(c_fcast):
    forecast = c_fcast['forecast']['txt_forecast']['forecastday']
    msg = '\nNo High Chances of Rain.'
    i = 0
    for tframe in forecast:
        if tframe['pop'] >= '40':
            if i == 0:
                msg = '\n--------------------\nHigh Chances of Rain'
            msg += '\n' + tframe['title'] + ': ' + tframe['pop'] + '%'
            i+=1
    return msg

def get_tomorrow(c_fcast):
    forecast = c_fcast['forecast']['txt_forecast']['forecastday']
    for tframe in forecast:
        if tframe['period'] == 2:
            msg = '\n' + tframe['title'] + ' will be ' + subitalize(tframe['fcttext'])
    return msg

# Send the email message
def send_msg(sndr, rcvr, m, loc):
    msg = 'Subject: Weather in %s\n%s' % (loc, m)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sndr, rcvr, msg)
    except SMTPException:
        print 'Error: Unable to send message'
        sys.exit(1)
    return

# Pull and parse desired data
c_fcast = get_data(zipcode, 'forecast')
#c_almanac = get_data(zipcode, 'almanac')
#c_astronomy = get_data(zipcode, 'astronomy')

# Assemble to message to mail to the user
loc = c_fcast['current_observation']['display_location']['full']
msg = 'Currently %s and %s' % (c_fcast['current_observation']['weather'], c_fcast['current_observation']['temperature_string'])
msg += ' with wind out of the %s @ %s mph.' % (c_fcast['current_observation']['wind_dir'], str(c_fcast['current_observation']['wind_mph']))
msg += get_tomorrow(c_fcast)
msg += get_chances(c_fcast)

# Switch to email sending, once message is prepped
print msg   #Print to screen for now
#send_msg(config.sender, config.recipient1, msg, loc)
#send_msg(config.sender, config.recipient2, msg, loc)
