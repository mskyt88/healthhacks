
import urllib
import urllib2
import decimal
import sys
from bs4 import BeautifulSoup

import json

base_url = "www.yelp.com"

def scrap_menu_items( rest_id, req_submenu_id = "" ):
	if req_submenu_id == "":
		url = base_url + "/menu/" + rest_id
	else:
		url = base_url + "/menu/" + rest_id + "/" + req_submenu_id

	print "parsing ... "+url

	response = urllib2.urlopen( "http://"+urllib.quote(url.encode("utf8")) )
	html = response.read()
	soup = BeautifulSoup( html, 'html.parser')

	ret = {}

	submenus = soup.find( "ul", class_="sub-menus" )
	
	if req_submenu_id == "" and submenus is not None:
		for submenu in submenus.find_all( "li" ):
			if submenu.a is None:
				submenu_id = submenu.get_text().strip()	# currently selected submenu
			else:
				submenu_link = submenu.a.get("href")
				another_submenu_id = submenu_link[ submenu_link.rfind("/")+1: ]
				if another_submenu_id != submenu_id:
					submenu_items = scrap_menu_items( rest_id, another_submenu_id )
					for k,v in submenu_items.items():
						ret[k] = v
	else:
		submenu_id = req_submenu_id

	print "submenu: ", submenu_id

	items = soup.find_all( "div", class_="menu-item-details" )
	for item in items:
		if item.h4.a is not None:
			name, link = item.h4.a.get_text().strip(), item.h4.a.get("href")
			link = "http://"+base_url + link
		elif item.h4 is not None:
			name, link = item.h4.get_text().strip(), ""

		desc = ""
		if item.find("p", class_="menu-item-details-description" ) is not None:
			desc = item.find("p", class_="menu-item-details-description" ).get_text().strip()
		ret[ name ] = (rest_id, submenu_id, name, desc, link)

	return ret

	

#fd = open( "menus.csv", "w" )
#fd.write( u"Hol\xe1, A-Migas".encode("utf-8") )
#fd.close()
#asdf


if __name__ == "__main__":

	all_restaurants = []

	fd = open( "restaurants.json" )
	for line in fd:
		all_restaurants.append( json.loads( line ) )
	fd.close()

	try:
		fd = open( "menus.csv" )
		for line in fd:
			last_rid = line.split(",")[0]
		fd.close()

		last_index = 0
		for i in range(len(all_restaurants)):
			if all_restaurants[i]["id"] == last_rid:
				last_index = i+1
				break

	except:
		last_index = 0

	fd = open( "menus.csv", "a" )
	fd.write( "ID,CATEGORY,NAME,DESCRIPTION,LINK\n".encode("utf-8") )
	for r in all_restaurants[ last_index : ]:
		menus = scrap_menu_items( r["id"] )
		print "%d items were fetched ..." % len(menus)

		for m in menus.values():
			print m
			fd.write( ('%s,%s,"%s","%s",%s\n' % m).encode("utf-8") )
	fd.close()

	#print scrap_menu_items( "flat-top-new-york" )
	
