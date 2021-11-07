# GoBike
## by Walid Alashry


## Dataset

> This data consists of 183412 bike trips in Feb-2019. it provides information about start and end time of each trip, duration, start and end station for each trip, start and end station id for each trip, start and end station latitude and longitude, bike_id, user's birthday and gender, customer type and bike share information. 


## Summary of Findings


>There are 183412 trips in our dataset, we have 4646 unique bikes and the data is collected for Feb2019, we have 329 unique stations and we have 197 trip with no station name or id and by investigating those 197 trip we found that all of those trips started or ended in San Jose,Ca (I investigated the max and min longitude and latitude in google maps).Most users use the bikes at workdays(Mondays to Fridays) and the traffic is decreasing up to 50% at the weekend. Most of the trips happens between (7:00 am-10:00am) when people are going to their work and between(16:00pm -19:00pm) when people returning from their work. We could see that most of the top stations has biomodal distribution as the whole distribution with some expetions. there are a strong relation between type of day(weekend or workday) and number of trips. everyday there are some bikes that stop working maybe because it is broken, out of service, changing its id or stolen! At the end day of the month which was a workday(Thu), there are about 2500 bikes doing trips from 4646 bikes in our dataset (about 54%) .. we need to improve this metric if we need to gain more profits. We discvered that some bikes transfered from a station to another with no trip that may mean two things: company transfer bikes to satisfy the high demand in some stations or people use those bikes with no trip! there are 15097 transfered trip.
we went deep in our dataset to find what times of day that there are no bikes in any station.

## Key Insights for Presentation

> I am going to show the realtionship between station and time and type of day, then I will show the numbers of trips that happens in each weekday. After that I will show the distibution of duration of trips and why there are some trips with too long duration. I will see how many trips with transferred bike Finally I will show the number of bikes that stop at top 3 stations at end of each day.
