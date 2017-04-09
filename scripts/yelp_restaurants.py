
import urllib
import urllib2
import decimal
import sys, traceback
from bs4 import BeautifulSoup


import oauth2
import requests
import json

# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
CLIENT_ID 		= "jzr3C5IxCv5DpEnzPQj9XA"
CLIENT_SECRET 	= "N4cuxZSLdkAbPl0XAB6hMb7ZP0wB6jduaosEeKvAXaDtMGfbrJkJzsw1XFmMMem7"


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

SEARCH_LIMIT = 50

def obtain_bearer_token(host, path):
	url = '{0}{1}'.format(host, urllib2.quote(path.encode('utf8')))
	assert CLIENT_ID, "Please supply your client_id."
	assert CLIENT_SECRET, "Please supply your client_secret."
	data = urllib.urlencode({
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'grant_type': GRANT_TYPE,
	})
	headers = {
		'content-type': 'application/x-www-form-urlencoded',
	}
	response = requests.request('POST', url, data=data, headers=headers)
	bearer_token = response.json()['access_token']
	return bearer_token


def request(host, path, bearer_token, url_params=None):
	url_params = url_params or {}
	url = '{0}{1}'.format(host, urllib2.quote(path.encode('utf8')))
	headers = {
		'Authorization': 'Bearer %s' % bearer_token,
	}

	print u'Querying {0} ...'.format(url), url_params

	try:
		response = requests.request('GET', url, headers=headers, params=url_params)
		ret = response.json()
	except:
		traceback.print_exc()
		ret = json.loads("{businesses':[]}")


	return ret


def search(bearer_token, latitude, longitude, radius):
	url_params = {
		'term': "restaurants",
		'longitude': longitude,
		'latitude': latitude,
		'radius' : radius,
		'limit': SEARCH_LIMIT
	}
	return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def scrap_restaurants( bearer_token, latitude, longitude, radius ):
	print bearer_token
	response = search(bearer_token, latitude, longitude, radius)
	#print response
	businesses = response.get('businesses')

	#
	if not businesses:
		#print(u'No businesses for {0} in {1} found.'.format(term, location))
		print "no business"
		return []
		
	else:

		"""
		{u'rating': 4.5, u'review_count': 78, u'name': u'Marufuku Ramen', 
		u'transactions': [], u'url': u'https://www.yelp.com/biz/marufuku-ramen-san-francisco?adjust_creative=jzr3C5IxCv5DpEnzPQj9XA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=jzr3C5IxCv5DpEnzPQj9XA', 
		u'price': u'$$', 
		u'distance': 2712.1886761339997, 
		u'coordinates': {u'latitude': 37.7852337, u'longitude': -122.4315788}, 
		u'phone': u'+14158729786', 
		u'image_url': u'https://s3-media2.fl.yelpcdn.com/bphoto/R0ACqI5GP691co8yBZmLIQ/o.jpg', 
		u'categories': [{u'alias': u'ramen', u'title': u'Ramen'}], 
		u'display_phone': u'(415) 872-9786', 
		u'id': u'marufuku-ramen-san-francisco', 
		u'is_closed': False, 
		u'location': {u'city': u'San Francisco', u'display_address': [u'1581 Webster St', u'Ste 235', u'San Francisco, CA 94115'], u'country': u'US', u'address2': u'Ste 235', u'address3': None, u'state': u'CA', u'address1': u'1581 Webster St', u'zip_code': u'94115'}}
		"""

		print len(businesses), " restaurants retrieved"

		return businesses



def ccw(A,B,C):
	return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def point_in(pt, corners, inf):
	result = False
	for i in range(len(corners)-1):
		if intersect(corners[i], corners[i+1], pt, (inf, pt[1])):
			result = not result
	if intersect(corners[-1], corners[0], pt, (inf, pt[1])):
		result = not result
	return result

def arange(start, end, step):
	ret = []
	r = start
	while r < end:
		ret.append( r )
		r += step
	return ret

if __name__ == "__main__":
	#print scrap_restaurants( (-73.95831942558289,40.8122783182074,-73.96153807640076,40.80984222148306) )
	#print scrap_one_restaurant( "flat-top-new-york" )
	#print scrap_menu_items( "flat-top-new-york" )
	
	bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

	booundaries = [ 
		(40.814231,-73.965712),
		(40.800589,-73.928719),
		(40.752069,-74.009056),
		(40.740462,-73.971376) ]

	grid_size = 0.005
	radius = 1000

	min_lat = min( b[0] for b in booundaries )
	max_lat = max( b[0] for b in booundaries )
	min_lon = min( b[1] for b in booundaries )
	max_lon = max( b[1] for b in booundaries )

	fd = open( "restaurants.json", "w", 0 )
	rids = set()

	for lat in arange( min_lat, max_lat, grid_size ):
		for lon in arange( min_lon, max_lon, grid_size ):

			if point_in( (lat,lon), booundaries, 1000 ) == False:
				continue

			print "query ... (%f,%f)" % (lat,lon)
			#continue

			retrieved = scrap_restaurants( bearer_token, lat, lon, radius )

			if len(retrieved) > 0:
				print retrieved[0]["name"], retrieved[0]["location"]["address1"]
			
			for res in retrieved:
				if res["id"] in rids:
					continue
				rids.add( res["id"] )
				fd.write( json.dumps(res)+"\n" )
				
	fd.close()
