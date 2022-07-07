# Pub Wednesday DemocracyBot

Pub Wednesday went to Whitby -this was a quick and dirty attempt to help decide on a group holiday accommataion choice fairly, using an alternative vote runoff method. User-provided votes were read directly from a Google Sheets document. A `Flask` app was hosted in a [Heroku Dyno](https://www.heroku.com/dynos) (because it was free), exposing two endpoints; one to simply return the accommodation choices ranked in order of preference, as determined by the runoff system, and a second endpoint detailing the intermediate scores at each round of the runoff. 
 
