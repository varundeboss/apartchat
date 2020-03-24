# ApartChat

Apartchat is a NLP based search engine for searching apartment seeking and sharing posts by users

## Installation

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip3 install git+git://github.com/couchbase/couchbase-python-client
pip3 install spacy
```

## Dependencies

```text
generate_data.py is used for generating user, apartment and post related data based on user input count

generate_load_data.sh executes generate_data.py to generate the following data and load them 
	into couchbase(NoSQL DB)
	1) posts
	2) users
	3) apartments

search_apartment.py is the NLP based search engine which uses `spacy` to do natural language processing 
	and connects to the backend DB for quering out data based on posts, users and apartments
```

## Welcome page

```text
APARTCHAT: Welcome SHARER. "Sharing is Caring!!!" -Anonymous
           Please input your search text in free english text! Yes, you heard that right!!!
                  You could search using following attributes
                      - gender
                      - food_type
                      - user_tags
                      - distance
                      - price_range
                      - bhk
                      - balcony
                      - furnish
                      - apartment_tags
           Examples
                  SHARER
                      - Looking to share my apartment with a vegetarian
                      - Need a male tenant who is preferably a dog lover
                      - Looking for a non vegetarian female tenant preferably
                      - Need a flatmate who preferably doesn't smoke and don't drink
                  SEEKER
                      - Need a 3 bhk apartment with a swimming pool in the range of 10 to 12k
                      - Need a flat, preferably nearby a metro with at least 2 balconies
                      - Looking for a apartment near me
                      - Looking for a semi furnished apartment which is pet friendly and preferably sea side
           *** Type 'C/c' to clear your search criterias!!! *** 
           *** Type 'N/n' to show next post!!! *** 
           *** Type 'P/p' to show previous post!!! *** 
           *** Type 'Q/q' to quit the program!!! *** 
           *** Type 'W/w' to show the welcome message!!! ***
```

## Enum values

The following are the enum values which are used for NLP and is expandable in the future based on market research
```python
USER_TYPES = [
	"SHARER", # One who is already a renter looking to share an apartment
	"SEEKER" # One who is looking for an apartment to rent
]

GENDERS = {
	"M": ["Male", "Guy", "Man", "He"],
	"F": ["Female", "Girl", "Woman", "She"],
}

FOOD_TYPES = {
	'Vegetarian': ["veg", "Vegetarian"],
	'Non Vegetarian': ["non veg", "non Vegetarian"],
}

USER_TAGS = [ "Dog Friendly", "Cat Friendly", "Party", "Dog Lover", "Cat Lover", "Loves Cat", "Loves Dog", "Easy Going",
	"Non Smoker", "Non Smoking", "Non Drinker", "Non Drinking", "Doesnt Drink", "Doesn't Drink", "Doesnt Smoke", 
	"Doesn't Smoke", "Dont Smoke", "Don't Smoke", "Don't Drink", "Dont Drink", "Not Drink", "Not Smoke", "Loves Pet",
	"Pet Lover",
]

APARTMENT_FURNISH_TYPE = [ "FULLY-FURNISHED", "SEMI-FURNISHED", "UN-FURNISHED", ]

APARTMENT_TAGS = [ "Air Conditioned", "Elevator", "Swimming Pool", "Parking", "Dog Friendly", "Cat Friendly", "Park", 
	"Bus stop", "Lake view", "Sea Side", "Pet Friendly", "Pets Allowed", "Metro", "Beach Side",
]
```

## Usage

```bash
cd /home/varun/workspace/personal/apartchat
python3 search_apartment.py
```
1) Execute the Apartment Search Program
![Start Apartment Search Program](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/1_start_search_program.png)
2) Get User's type (SHARER / SEEKER)
![User Question](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/2_user_question.png)
3) Enter the welcome page
![Welcome page](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/3_welcome_page.png)
4) Get the first post
![First post](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/4_first_post.png)
5) Get next post (By entering 'n')
![Next post](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/5_next_post.png)
6) Clear the searching params (By entering 'c')
![Clear params](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/6_cleared_post.png)
7) Move on to second post
![Second post](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/6_second_post.png)
8) Post belonging to apartments nearme based on geospatial calculation between geocodes
![Nearme posts](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/7_nearme_apartment.png)
9) Nearby posts
![Nearby posts](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/8_nearby_post.png)
10) Posts based on price range
![Price posts](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/9_price_range.png)
11) End of posts (No more)
![No posts](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/10_no_more_posts.png)
12) Thank you note to use
![Thank you](https://raw.githubusercontent.com/varundeboss/apartchat/master/screenshots/11_thank_you.png)

## Disclaimer

The NLP based search engine is only a prototype for POC that searches for online based posts (user / apartments) could be 
done using machine learning models and NLP when trained on proper corpus of data set 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
