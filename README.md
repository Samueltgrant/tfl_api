# tfl_api

A personal project using the tfl api to create a Flask application that allows users to find the best station to meet at.

Similar to the popular app "Citymapper" this project aims to solve a slightly different problem. Whilst Citymapper shows
the best route between locations A-B, this project aims to show the most convenient place for groups of people to meet
at. It does this by using a look-up table of expected journey times between tube stations to find the three most 
conveinent tube stations, then returns the live journey for all users to these three stations.

This is a Flask based application, which also utilises JavaScript, HTML, CSS and jinja2.

## How to use
The server can be run by running main.py. The necessary packages are described in requirements.txt. The credentials for 
running the server are left as plain text in api_keys.py to allow users to run the server without creating their own 
access keys. This is obviously not generally good practice though!

## Future Improvements
The project is largely working although there are a whole load of additions that need to be added before it could be 
considered useful. The additions I'd like to slowly add are:

### add phone dimensions

### add 'load more options' button

#### Better error handling
-   Sometimes I encounter significant errors using the tfl api. This is likely to be me not fully understanding the 
response from tfl and I can hopefully fix when I have some more time to investigate it. I have found the tfl documentation
    a bit slim here though so might need some playing around with the data outputs.

- ####Effective asynchronous GET requests.
  
    This is likely to speed up the processing time significantly. I have 
been using multiprocessing, which decreased the wait time by 2x but I'm not sure if this is sensible to use in a Flask
  server (not sure how this would affect mobile use - one to check).


- #### Database options
    Currently, the station to station look up table is based purely off a 3pm Saturday leaving time journey. This would 
    not be a good estimate for other times, or when the tube is not running. If I created an hourly table look up for 
    each day (168 tables), I could just search the most relevant table depending on the time it's being used. 
  
    It would also be better to continually add to the data, by collecting data from different days, then use a mean 
    score, to reduce the impact of delays during the time when the look-up table was created.
  
#### Actual location input
-   Currently, the application only allows for users to input their nearest station. However, this assumes that their 
    nearest station is inherently the station to go to. Other stations are ofcourse possible or the journey may not 
include the tube at all.
    
    Implementing the search between coordinates would be really easy, as that is already supported by the tfl api.
A "use current location" functionality would definitely be useful but users obviously would struggle to input other
    users coordinates. It would probably be best to use something similar to google geolocation api, where a user can
    enter the location of a known place and then google will convert it into coordinates. This would need a fair amount 
    of error handling, and I would somehow need the autofill functionality for this too (although I'm sure similar code
    is available online).
    
    The other side of this is that it would be good to suggest actual pubs / venues etc to meet at. This would be a lot 
    of additional work but could actually make this a really interesting app. 
        

#### Convert to a front-end server
-   I think this might potentially be faster to use Node JS as I'd be able to be load more results etc in the background?
I don't have a good working knowledge of Node JS however.


