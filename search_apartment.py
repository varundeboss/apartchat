import os
import sys
import re

import spacy

from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator
from couchbase.cluster import QueryOptions

from math import radians, cos, sin, asin, sqrt

import generate_data as gd


user = "Anonymous"
search_response = "Sorry I have difficulty understanding!!! Could you please be rephrase???"
min_distance = 30

COUNTER = 0

nlp = spacy.load('en_core_web_sm')

cluster = Cluster('couchbase://localhost', ClusterOptions(PasswordAuthenticator('vc-search', 'vc-search')))
cb = cluster.bucket('vc-search')
coll = cb.default_collection()

user_json = coll.get("user::1").content
apartment_json = coll.get("apartment::1").content

USER_TYPES = {
	"SHARER": "1",
	"SEEKER": "2"
}

ENTITIES = {
	"gender": gd.GENDERS,
	"food_type": gd.FOOD_TYPES,
	"user_tags": gd.USER_TAGS,
	"furnish_type": gd.APARTMENT_FURNISH_TYPE,
	"apartment_tags": gd.APARTMENT_TAGS,
	"bhk": gd.BHKS,
	"balcony": gd.BALCONIES,
	"bathroom": gd.BATHROOMS,
	# "age": [],
	"geoCodes": gd.GEOCODES,
	"price_range": gd.PRICE_RANGE,
	"user_type": [],
}

USER_TYPE_INV = []

USER_ENTITIES = ["gender", "food_type", "user_type"]
APARTMENT_ENTITIES = ["furnish_type", "bhk", "balcony"]

def init_entities_search():
	return  {key: [] for key in ENTITIES}

ENTITIES_SEARCH = init_entities_search()


def clear_screen():
	os.system("clear")

def print_empty_line():
	print()

def print_host(msg):
	# print_empty_line()
	print("APARTCHAT:", msg)
	print_empty_line()

def print_guest(msg):
	print_empty_line()
	print("{:>50}".format("GUEST:" + str(msg)))
	print_empty_line()

def print_welcome_msg():
	clear_screen()
	print_host("Hello %(name)s!!! I am APARTCHAT!!! Your smart assistant for all your apartment/tenant sharing solutions!!!" % {
		"name": user_json["name"],
	})

def print_get_user_type():
	print("           Press 1 if you are a SHARER (One who is already a renter looking to share an apartment)")
	print("           Press 2 if you are a SEEKER (One who is looking for an apartment to rent)")
	print_empty_line()

def get_search_text():
	return re.sub("\s+", " ",input("{:>50}".format("GUEST: ")).strip().lower())

def get_price_range(search_text, key, val, entity_list):
	doc = nlp(search_text)
	for ent in doc.ents:
		# print(ent.text, ent.start_char, ent.end_char, ent.label_)		
		if ent.label_ in ["DATE", "CARDINAL", "QUANTITY"]:
			ent_text = ent.text.replace("k", "000")
			ent_texts = list(map(int, re.findall(r'\d+', ent_text)))			
			if "k" in ent.text:
				ent_texts = [ et * 1000 if (et % 1000) > 0 else et for et in ent_texts ]
			for word in val:
				if word.lower() in ent.text:
					entity_list.extend(ent_texts)

	entity_list.sort()
	if len(entity_list) > 1:
		entity_list = [entity_list[0], entity_list[-1]]
	return entity_list

def rows_to_str(entities, user_master_resp, apartment_master_resp):
	global COUNTER	

	post_str = """=====================================================|
			POST #%(counter)d                      |
=====================================================|
          User Details                               |
=====================================================|
| Name       : %(name)s
| Age        : %(age)s
| Gender     : %(gender)s
| Contact    : %(contact)s
| Food Type  : %(food_type)s
| User Tags  : %(user_tags)s
| User Type  : %(user_type)s
"""
	apartment_str = """=====================================================|
        Apartment Details                            |
=====================================================|
| Name       : %(apartment_name)s
| Address    : %(address)s
| Price      : %(price_range)s
| BHKs       : %(bhk)s
| Bathrooms  : %(bathroom)s
| Balconies  : %(balcony)s
| Furnish    : %(furnish_type)s
| Apart Tags : %(apartment_tags)s
| Distance   : %(distance)s
=====================================================|
"""
	user_type = "SHARER" if entities["user_type"][0] == "SEEKER" else "SEEKER"
	post_master_str = "You are a '%(user_type)s' searching for\nSEARCH PARAMS: %(entities)s\n\n" % {
		"user_type": user_type,
		"entities": entities,
	}

	# for user_index in range(1):
	user_index = COUNTER
	if COUNTER >= (len(user_master_resp) - 1):
		post_master_str = "That's all posts for today folks!!!\n"
	else:
		user_master_resp[user_index]["counter"] = COUNTER + 1
		post_master_str += post_str % user_master_resp[user_index]
		if apartment_master_resp:
			apartment_master_resp[user_index]["apartment_name"] = apartment_master_resp[user_index]["name"]
			post_master_str += apartment_str % apartment_master_resp[user_index]

	post_master_str += """=====================================================|
*** Type 'C/c' to clear your search criterias!!! *** |
*** Type 'N/n' to show next post!!! ***              |
*** Type 'W/w' to show the welcome message!!! ***    |
=====================================================|"""

	return post_master_str

def convert_post_to_str(entities, user_resp, apartment_resp):	
	apartment_master_resp = []

	user_ids = [i["vc-search"]["id"] for i in user_resp]
	
	if apartment_resp:
		apartment_ids = [i["vc-search"]["id"] for i in apartment_resp]
		user_ids = list(set(user_ids).intersection(set(apartment_ids)))
		apartment_master_resp = [i["vc-search"] for i in apartment_resp if i["vc-search"]["id"] in user_ids]

	user_master_resp = [i["vc-search"] for i in user_resp if i["vc-search"]["id"] in user_ids]

	return rows_to_str(entities, user_master_resp, apartment_master_resp)

def distance(lat1, lat2, lon1, lon2):
	# The math module contains a function named 
	# radians which converts from degrees to radians. 
	lon1 = radians(lon1) 
	lon2 = radians(lon2) 
	lat1 = radians(lat1) 
	lat2 = radians(lat2) 
	   
	# Haversine formula  
	dlon = lon2 - lon1  
	dlat = lat2 - lat1 
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a))  
	 
	# Radius of earth in kilometers. Use 3956 for miles 
	r = 6371
	   
	# calculate the result 
	return(c * r)

def get_apartments_within_range(geo_codes, apartment_full_resp):
	apartment_resp = []
	
	lat1 = float(geo_codes[0])
	lon1 = float(geo_codes[1])

	for apartment in apartment_full_resp:
		lat2 = float(apartment["vc-search"]["geoCodes"][0]["latitude"])
		lon2 = float(apartment["vc-search"]["geoCodes"][0]["longitude"])

		distance_km = distance(lat1, lat2, lon1, lon2)

		apartment["vc-search"]["distance"] = "%.2f" % round(distance_km,2) + "km (away)"
		apartment_resp.append(apartment)

	return apartment_resp


def convert_json_to_post(entities):
	user_query = "select * from `vc-search` where type='user'"
	apartment_query = "select * from `vc-search` where type='apartment'"

	apartment_full_resp = []	

	user_resp = []
	apartment_resp = []

	user_flag = False
	apartment_flag = False

	if entities["geoCodes"]:
		apartment_flag = True
		entities["geoCodes"] = [apartment_json["geoCodes"][0]["latitude"], 
								apartment_json["geoCodes"][0]["longitude"]]

	geoCodes = [apartment_json["geoCodes"][0]["latitude"], 
				apartment_json["geoCodes"][0]["longitude"]]
	apartment_full_resp = cluster.query(apartment_query).rows()
	apartment_full_resp = get_apartments_within_range(geoCodes, apartment_full_resp)

	for k, v in entities.items():
		if k in USER_ENTITIES and v:
			user_flag = True
			user_query += " and " + str(k) + " in " + str(v)
		elif k in APARTMENT_ENTITIES and v:
			apartment_flag = True
			apartment_query += " and " + str(k) + " in " + str(v)

	if entities["user_tags"]:
		user_flag = True
		for user_tag in entities["user_tags"]:
			user_query += ' and ARRAY_CONTAINS(user_tags, "%(user_tag)s")' % {"user_tag": user_tag}

	if entities["apartment_tags"]:
		apartment_flag = True
		for apartment_tag in entities["apartment_tags"]:
			apartment_query += ' and ARRAY_CONTAINS(apartment_tags, "%(apartment_tag)s")' % {"apartment_tag": apartment_tag}

	if entities["price_range"]:
		apartment_flag = True
		pr = entities["price_range"]
		apartment_query += " and (price_range.min <= %(min)d and price_range.max >= %(max)d)" % {
			"min": pr[0],
			"max": pr[1],
		}	

	# print(entities)
	# print(user_flag, ":", user_query)
	# print(apartment_flag, ":", apartment_query)

	if user_flag:
		user_resp = cluster.query(user_query).rows()
	if apartment_flag:
		apartment_resp = cluster.query(apartment_query).rows()
		if apartment_full_resp:
			apartment_q_ids = [i["vc-search"]["id"] for i in apartment_resp]
			apartment_resp = [i for i in apartment_full_resp if i["vc-search"]["id"] in apartment_q_ids]
		if entities["geoCodes"]:
			apartment_resp = sorted(apartment_resp, key = lambda i: i["vc-search"]["distance"])

	post_str = convert_post_to_str(entities, user_resp, apartment_resp)

	return post_str

def find_search_entities(search_text):
	global ENTITIES_SEARCH
	global USER_TYPE_INV

	for entity_key, entity_val in ENTITIES.items():
		if (type(entity_val) == type({})):
			for key, val in entity_val.items():
				if entity_key == "price_range":
					ent_texts = get_price_range(search_text, key, val, ENTITIES_SEARCH[entity_key])
					# if ent_texts:
					# 	ENTITIES_SEARCH[entity_key] = []
					ENTITIES_SEARCH[entity_key] = ent_texts
				elif entity_key in ["food_type", "gender"]:
					ENTITIES_SEARCH[entity_key].extend([key for word in val if word.lower() in search_text.split()])
				else:
					ENTITIES_SEARCH[entity_key].extend([key for word in val if word.lower() in search_text])
		elif (type(entity_val) == type([])):
			ENTITIES_SEARCH[entity_key].extend([entity_key for word in entity_val if word.lower() in search_text])

		ENTITIES_SEARCH[entity_key] = list(set(ENTITIES_SEARCH[entity_key]))

	ENTITIES_SEARCH["user_type"] = USER_TYPE_INV

	posts = convert_json_to_post(ENTITIES_SEARCH)

	return posts

def parse_search_text(search_text, search_type):
	global ENTITIES_SEARCH
	global USER_TYPE_INV
	global COUNTER

	if search_type == "user_type":
		while search_text not in ["1", "2"]:
			print_host("OOPS!!! Wrong input! Please enter either 1(SHARER) OR 2(SEEKER) to proceed...")
			search_text = get_search_text()

		search_response = "Welcome %(user_type)s. %(user_type_msg)s\n\
           Please input your search text in free english text! Yes, you heard that right!!!\n\
                  You could search using following attributes\n\
                      - gender\n\
                      - food_type\n\
                      - user_tags\n\
                      - distance\n\
                      - price_range\n\
                      - bhk\n\
                      - balcony\n\
                      - furnish\n\
                      - apartment_tags\n\
           Examples\n\
                  SHARER\n\
                      - Looking to share my apartment with a vegetarian\n\
                      - Need a female tenant who is preferably a dog lover\n\
                      - Looking for a non vegetarian male tenant preferably in his early 20s\n\
                      - Need a flatmate who preferably doesn't smoke and don't drink\n\
                  SEEKER\n\
                      - Need a 3 bhk apartment with a swimming pool in the range of 10 to 12k\n\
                      - Need a flat, preferably nearby a metro with at least 2 balconies\n\
                      - Looking for a apartment near me\n\
                      - Looking for a semi furnished apartment which is pet friendly and preferably sea side\n\
           *** Type 'C/c' to clear your search criterias!!! *** \n\
           *** Type 'N/n' to show next post!!! *** \n\
           *** Type 'W/w' to show the welcome message!!! *** " % {
			"user_type": "SHARER" if search_text == "1" else "SEEKER",
			"user_type_msg": "\"Sharing is Caring!!!\" -Anonymous" if search_text == "1" \
							 else "\"I am seeking, I am striving, I am in it with all my heart!!!\" -Van Gogh",
		}
		ENTITIES["user_type"] = ["SHARER"] if search_text == "1" else ["SEEKER"]
		USER_TYPE_INV = ["SEEKER"] if search_text == "1" else ["SHARER"]
	else:
		if search_text.lower() == "c":
			ENTITIES_SEARCH = init_entities_search()
			COUNTER = 0
		elif search_text.lower() == "w":
			return parse_search_text(USER_TYPES[ENTITIES["user_type"][0]], "user_type")
		elif search_text.lower() == "n":
			COUNTER += 1
		elif search_text.lower() == "q":
			return "Thank you %(name)s for using APARTCHAT! Hope to see you soon!!!" % {
				"name": user_json["name"],
			}

		search_response = find_search_entities(search_text)
	
	return search_response

def main():
	search_text = ""
	search_type = "user_type"
	print_welcome_msg()
	print_get_user_type()
	while(search_text != "q"):
		search_text = get_search_text()
		clear_screen()
		print_host(parse_search_text(search_text, search_type))
		search_type = ""

if __name__ == '__main__':
	main()