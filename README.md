# Weather
A python script intended to be set executable and run by cronjob on a linux box.  Requires an API key obtained from http://www.wunderground.com/  A file named config.py must be included in the same directory as this script with the following lines:

```
# config.py
APIKEY = 'xxxxxxxxxxxxxxx'
sender = 'forecast@example.com'
recipient1 = '2125555555@txt.att.net'
recipient2 = '2125555556@txt.att.net'
```

```
Usage: set up as a cronjob
sample line:  30 8,20 * * * /home/username/weather.py
```

Report bugs as an issue in this github.  https://github.com/zully/weather
