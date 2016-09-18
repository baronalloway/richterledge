#import image_scraper
#image_scraper.scrape_images('http://10.179.2.87/axis-cgi/jpg/image.cgi')
#image-scraper -s mygifs http://10.179.2.87/axis-cgi/jpg/image.cgi --formats jpg
axisip='10.179.2.87'
basename='umiami'
import urllib.request, urllib.error, urllib.parse, time, os, re, getopt, sys
auth_handler = urllib.request.HTTPBasicAuthHandler()
opener = urllib.request.build_opener(auth_handler)
urllib.request.install_opener(opener)
axis_jpg=urllib.request.urlopen('http://10.179.2.87/axis-cgi/jpg/image.cgi')

filename='%s_%s_%s.jpg' % ( basename, time.strftime('%Y%m%d'), time.strftime('%H%M%S') )
local_jpg=open(filename,'wb')
local_jpg.write(axis_jpg.read())
local_jpg.close()
