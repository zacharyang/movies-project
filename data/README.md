# Movie Data #

In this project, I'll be analysing data from:

1.	[iTunes RSS Feed and iTunes Search API](#itunes)
2.	[Open Movie Database](#omdb)
3.	[Box Office Mojo](#mojo)

<h2> <a name="itunes"> iTunes Data </a></h2>

The data comes from the iTunes store, where I've collected data from the iTunes RSS feed and iTunes Search API. You can follow my data collection process through my Github repository and README. I've collected a total of 1,800 of the latest and most popular movies on iTunes across 9 different countries. These are mainly countries in the APAC market, ie. Australia, Indonesia, Malaysia, New Zealand, The Philippines, Singapore, Thailand and Vietnam. I've also included movies from the US iTunes store.

This is a description of the major data fields that I'll be focusing on in my analysis. There are other features within the data that I'll be excluding from the analysis but these can be viewed from the [iTunes API documentation](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/UnderstandingSearchResults.html#//apple_ref/doc/uid/TP40017632-CH8-SW1).

| Variable Name |  Type   |Description|
| :----------:  | :-----: |:------------:|
|     artistId   |  String | Unique artist identifier|
|     artistName      | String | Artist Name, usually refers to director or production studio|
|     country | String| 3-letter country ISO 3166 ALPHA-3 code  |
|     currency      | String | 3-letter currency ISO 4217 code |
|     longDescription   |  String | Synopsis of the movie as listed in the iTunes store|
|     primaryGenreName     | String| Genre of the movie|
|    releaseDate   | String | Date when movie was first released |
|     shortDescription    | String | Short synopsis of the movie as listed in the iTunes store |
|     trackId   |  Float| Unique Movie ID listed on the iTunes Store|
|     trackHdRentalPrice     | Float | Listed Unit Price of renting a movie in HD in local currency |
|     trackHdPrice   | Float | Listed Unit Price of buying a movie in HD in local currency |
|     trackPrice     | Float | Listed Unit Price of buying a movie in local currency |
|     trackRentalPrice   |  Float | Listed Unit Price of renting a movie in local currency|
|     trackTimeMillis      | Float | Run Time of movie in milliseconds|


<h2><a name="omdb"> Open Movie Database </a></h2>

The OMdb data has two main components. The search parameters contained in the OMdb_search_dat JSON file, which contain the keyword search strings and IMdb IDs used to query the OMdb API. Crucially, each search string and unique IMdb ID contains a corresponding unique iTunes ID, which will then be used to join the iTunes data and the OMdb data.

The OMdb_data JSON file contains the results that have come back from the OMdb API. These contain information on the movie, including information on the cast, box office returns, critic ratings etc. 

In my analysis, I'll be joining the two data files into a common dataframe. I've listed the definitions of most of the features below but please check in with the [OMdb API documentation](http://www.omdbapi.com/) for further reference.


| Variable Name |  Type   |Description|
| :----------:  | :-----: |:------------:|
|     Actors   | String | List of actors credit to the movie separated by commas|
|     Awards    | String | Description of number of awards and nominations for the movie|
|     Country | String| List of countries that the movie is set in, separated by commas |
|     DVD     | String | Date released on DVD |
|     Director   |  String | List of actors credit to the movie separated by commas|
|     IMdb_score    | Float| IMdb rating for the movie, ranging from 0 to 100|
|    Language  | String | List of languages that the movie is released in, separated by commas |
|     Metascore   | String | Metascore rating for the movie, ranging from 0 to 100 |
|     Plot  |  String| Synopsis of the movie|
|     Production     | Float | Production Studio that produced the movie |
|     RT_score   | Float | Rotten Tomatoes rating for the movie, ranging from 0 to 100 |
|     Title    | String | Movie Title |
|     imdbVotes   |  Float | Number of votes on IMdb|
|     Runtime     | String | Run Time of movie in minutes|
|     Year  | String | Year of Release |
|     actor_1   | String | First credited actor in the "Actors" column. Parsed out in `collect_data.py` |
|     actor_2    | Float | Second credited actor in the "Actors" column. Parsed out in `collect_data.py` |
|     num_actor   |  Float | Number of actors credited |
|     director_1      | String | First credited Director in the "Director" column. Parsed out in `collect_data.py`|
|     director_2  | String | Second credited Director in the "Director" column. Parsed out in `collect_data.py` |
|     num_director   | Float | Number of directors credited |
|     IMdb_ID  |  String | Unique IMdb ID taking the form of "tt" + 9-digit string|
|     TMdb_ID     | String | Possible TMdb IDs obtained from TMdb API queries. Could be a string or a single unique ID|
|     iTunes_ID    | String | Unique iTunes ID as listed on iTunes Store|
|     search_strs      | String | Movie Title transformed to pass through a search string, eg. "Field+of+Dreams"|


<h2><a name="mojo"> Box Office Mojo </a></h2>

Box Office information is obtained from respective movies by scraping [Box Office Mojo](https://www.boxofficemojo.com/alltime/), after discovering a bunch of missing data in the OMdb data. You can look at how I collected the data in [this script](https://github.com/zacharyang/movies-project/blob/master/collect_box_office.py).

| Variable Name |  Type   |Description|
| :----------:  | :-----: |:------------:|
| worldwide-gross| Float | Worldwide box office earnings, obtained from [Box Office Mojo](https://www.boxofficemojo.com)|
| domestic-gross | Float | US box office earnings, obtained from [Box Office Mojo](https://www.boxofficemojo.com)|
| overseas-gross | Float | Overseas box office earnings, obtained from [Box Office Mojo](https://www.boxofficemojo.com)|
| domestic-pct | Float | % of total earnings coming from US box office earnings|
| overseas-pct | Float | % of total earnings coming from overseas box office earnings| 
| years | Integer | Year of release, according to Box Office Mojo|
| mojo_title| String | Title of movie, according to Box Office Mojo|

