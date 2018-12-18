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

**Under Construction**

<h2><a name="mojo"> Box Office Mojo </a></h2>

**Under Construction**

