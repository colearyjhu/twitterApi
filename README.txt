user flow:
if the main function is run on favorite.py (aka if you type python favorite.py)

You will see the following after authentification(numbers added for clarity):

1) list all keyWords you want to check 
cam
the following keywords were taken: cam
2) whats the location you are looking for? 
none
None, TO, PIE, Italia
the following lattitude and longitude was taken: 44.9331437.540121
3) do you only want hashtags? (yes/no) 
yes

For 1 it will find tweets with ALL OF THOSE KEYWORDS. So if you look for CAM WINTER AMERICA, you won't get many tweets but if you look for those 3 in three different searches you should be ok. Also if you enter the same word twice it will look for instances with that word twice.

For 2, if you don't want a location, hit enter. Otherwise you can enter almost anything and it will find somewhere that the location is true. For Instance above none doesn't do what you think.

For 3, the idea is whether you only want hashtags. If you say no, hashtags will still be included in the search, but of you say yes, it will look ONLY for tweets where all entered keywords are hashtags.





OutputFiles;
tweetRead: read the tweets that have been favorited
IDsOfFavorited: the ids of that which has been favorited so far, don't delete if you want to run unfav.py to destroy those favorited so far
Identification : a pickle of your authentification, not the safest way to do it but if the script is kept as a local utilty I figured it wasn't worth the time to try and set up a permenant more secure system, since it is your computer.

Design Note: Everything has been designed to print to files so that when you run a cron job, rather than an input from main, you will have record and the ability to unfav. Only user input pritns to stdout.
