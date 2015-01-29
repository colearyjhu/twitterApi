# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import json
from requests_oauthlib import OAuth1Session, OAuth1
from urlparse import parse_qs
import pickle
import codecs

IDFile = "IDsOfFavorited.txt"
import fileinput
from geopy.geocoders import Nominatim


#gets all the tweets with all hashtags listed
def getTweetsWithHashtags(hashtags, auth, latitude = None, longitude = None):
	twitterURL = "https://api.twitter.com/1.1/search/tweets.json?q="
	for  hashtag in hashtags:
	 	twitterURL = twitterURL + "+%23" + hashtag
	if latitude and longitude:
		twitterURL = twitterURL + "&geocode=" + latitude + "," + longitude + ",45mi"
	r = requests.get(twitterURL, auth = auth)
	data = json.loads(r.text)

	return data

#gets tweets with all keywords
def getTweetsWithKeywords(keywords, auth, latitude = None, longitude = None):
	twitterURL = "https://api.twitter.com/1.1/search/tweets.json?q="
	for  keyword in keywords:
	 	twitterURL = twitterURL + "+%22" + keyword
	if latitude and longitude:
		twitterURL = twitterURL + "&geocode=" + latitude + "," + longitude + ",45mi"
	r = requests.get(twitterURL, auth = auth)
	data = json.loads(r.text)

	return data

#favourites a tweet with an ID
def favATweet(idString, auth):
	twitterURL ="https://api.twitter.com/1.1/favorites/create.json?id=" + idString 	
	requests.post(twitterURL, auth = auth)

#writes the id to a IDFile
def writeIDstoFile(fileName, dataDict):
	try:
		IDFileObj = open(fileName, "a+")
	except:
		print "failure to print to ID file"
	for tweet in dataDict["statuses"]:
		IDFileObj.write(str(tweet["id"]) + "\n")
	IDFileObj.close()

#edits the dataDict, with repeated tweets eliminated; repeated tweets have their 
def eliminateAlreadyFavorited(fileName, dataDict):	
	try:
		compareFile = open(fileName, "r")
	except:
		#no need to print failure sicne it just means there is no file
		return
	for line in compareFile:
		for tweet in dataDict["statuses"]:
			if tweet["id"]== int(line):
				dataDict["statuses"].remove(tweet)
				break
	compareFile.close()

#keywordsToCheck should be an array
#longitude and lattidue should be Strings
#hashtag is whether you want hashtags turned on
#QB method to call what needs to be called
def favoriteTweets(keywordsToCheck, auth, latitude=None, longitude=None, hashtag=False):
	#get the tweets with the hashtag
	if hashtag:
		dataDict = getTweetsWithHashtags(keywordsToCheck, auth, latitude, longitude)
	#get the tweets with the keyword
	else:
		dataDict = getTweetsWithKeywords(keywordsToCheck, auth, latitude, longitude)
	#make sure none of the tweets have previously be favorited
	#print dataDict
	eliminateAlreadyFavorited(IDFile, dataDict)
	#favourite all tweets
	for tweet in dataDict["statuses"]:
		 favATweet(str(tweet["id"]), auth)
		#save favorited tweets
	writeIDstoFile(IDFile, dataDict)
	tweetPrinter(dataDict)

#get the latitude and longitude of input and prints the location found by geolocator
#returns None None if latitude and longitude not found
def getLatitudeAndLongitude(location):
	geolocator = Nominatim()
	found = geolocator.geocode(location)
	print found
	try:
		return (str(found.latitude), str(found.longitude))
	except:
		return None, None

#function that prints the tweets out in a readable Format after favoriting
#extension that needs fixing due to character conversions
def tweetPrinter(dataDict):
	try:
		tweeetFile = codecs.open("tweetRead.txt", "a+", "utf-8")
	except:
		print "failed to print tweets to file"
		return
	for tweet in dataDict["statuses"]:
		try:
			tweeetFile.write("Text:\t")
			tweeetFile.write((tweet["text"]))
			tweeetFile.write("\n")
			tweeetFile.write("Author: \t")
			tweeetFile.write(tweet["user"]["screen_name"])
			tweeetFile.write("----------------------------------------------------------------------\n")
		except:
			tweeetFile.write("tweet had undecphierable characters")
			tweeetFile.write("----------------------------------------------------------------------\n")
			#some tweets have weird characters so this ignores them to bypass errors
	tweeetFile.close()
#unfavorite all the saved tweets in the file
def unfavorite(fileName, auth):
	try:
		compareFile = open(fileName, "r+")
	except:
		return
	for line in compareFile:
		twitterURL = "https://api.twitter.com/1.1/favorites/destroy.json?id=" + line.strip()
		r = requests.post(twitterURL, auth = auth)
	#elimiante the file since you have unfaovrited everything
	compareFile.seek(0)
	compareFile.truncate()
	compareFile.close()

def authenticate():
	#The Applications Key and Secret
	client_key = "J0Pv6P4RlxGC6mMomb6WxHEIi"
	client_secret = "ALBVyx0VXtdo1CgnOuHRt6C2Wt2mAfWorX3IScDZgLarTZZEOZ"
	#autheticiation given these
	oauth = OAuth1Session(client_key, client_secret =client_secret)

	#get the resource owner key and secret
	fetch_response = oauth.fetch_request_token("https://twitter.com/oauth/request_token")
	resource_owner_key = fetch_response.get('oauth_token')
	resource_owner_secret = fetch_response.get('oauth_token_secret')

	#get user to enter their authorization pin
	authorization_url = oauth.authorization_url("https://api.twitter.com/oauth/authorize")
	print "Go here an authorize Then enter your pin!"
	print  authorization_url
	pin = raw_input("Whats your pin?")

	#with the pin retrieve the userToken and Secret
	oauth = OAuth1Session(client_key,
					client_secret=client_secret,
					resource_owner_key=resource_owner_key,
					resource_owner_secret=resource_owner_secret,
					verifier=pin)
	access_token_url = "https://api.twitter.com/oauth/access_token"
	oauth_tokens = oauth.fetch_access_token(access_token_url)
	resource_owner_key = oauth_tokens.get('oauth_token')
	resource_owner_secret = oauth_tokens.get('oauth_token_secret')
	#print resource_owner_secret
	#print resource_owner_key
	oauth = OAuth1(client_key, client_secret, resource_owner_key, resource_owner_secret)

	return oauth
	

def pickleAuth(auth):
	AuthFile = open("Identification.txt", "w")
	pickle.dump(auth, AuthFile)
	AuthFile.close()

def pickleLoad():
	AuthFile = open("Identification.txt", "r")
	Auth = pickle.load(AuthFile)
	AuthFile.close()
	return Auth

#GetArguments
#!/usr/bin/python
#gets the input to run favorite tweets
def main():
	try:
		auth = pickleLoad()
	except:
		auth = authenticate()
		pickleAuth(auth)
	keyWords = raw_input("list all keyWords you want to check \n")
	print "the following keywords were taken: " + keyWords
	location = raw_input("whats the location you are looking for? \n")
	try:
		#errors in this block
		(latitude, longitude) = getLatitudeAndLongitude(location)
		print "the following lattitude and longitude was taken: " + latitude + longitude
	except (UnicodeEncodeError, TypeError):
		#in this case either the input to get was weird and got an odd location sent back or nothing was specified
		print "no location taken"
		(latitude, longitude) = None, None
	hashtag = raw_input("do you only want hashtags? (yes/no) \n")
	print "Hashtags will be checked: " + str("yes" == hashtag)
	favoriteTweets(keyWords.split(), auth, latitude, longitude, "yes" == hashtag)

if __name__ == "__main__":
    main()

	