# Analysing Movies # 
In this project, I will be analysing movies on iTunes and other open movie databases as part of my capstone project at under a data science course at [General Assembly](https://www.generalassemb.ly).

## Should I see this movie in the cinema or on iTunes? ## 

![Deer Popcorn](images/giphy.gif)

I watch **a lot** of movies but I can't always afford to go to the movies and Netflix doesn't always have a good selection of the *latest* movies. So I've been watching more on Video On Demand (VOD) platforms such as [iTunes](https://itunes.apple.com/sg/genre/movies/id33), [Amazon Prime Video](https://www.primevideo.com/) or [Hooq](https://www.hooq.tv). 

So is it really *worth it* for me to wait for the DVD release? How can I predict the price a movie will be listed on iTunes? 

**For a VOD provider, how can I predict the price of a movie of that a rival VOD provider would list at?**

## Data Collection ## 

The first step in my project is to collect a bunch of data. You can access the movie data [here](https://github.com/zacharyang/movies-project/data). I've gotten data from:

* [iTunes RSS feed](https://rss.itunes.apple.com/en-gb) - Supplying the latest and hottest movies on the iTunes store across different countries.
* [iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html) - Allows us to search through the iTunes store by movie or movie ID, return data such as the listing price on the iTunes store
* [Open Movie Database API (OMdb)](http://www.omdbapi.com/) - Contains information on movies such as the IMdb ID, IMdb Rating, Cast, Directors etc. 
* [The Movie Database API (TMdb)](https://developers.themoviedb.org) - Similar kind of thing to OMdb, but less complete information and supports more queries per minute. 
* [Box Office Mojo](https://www.boxofficemojo.com/) - Details on box office earnings from tons of movies over the years. 


If you'd like to follow my data collection process, you can clone my repository and run the `python collect_data.py` in the cloned local repository. However, before you do that, you'll need to do a few things:

1.	Obtain the OMdb and TMdb API keys from their websites.
2.	Create a file in your local repo, `private.py` that contains two keys as `TMDB_API_KEY="yourkeyhere"` and `OMDB_API_KEY='yourkeyhere'`.
3.	Tweak `settings.py` to set up your data collection parameters.
4.	Run the `collect_data` script! 

## Exploration ## 

Over the next few weeks, I'll be exploring the data and deciding on how I'd like to model the data. Check back for updates in [this repository](https://github.com/zacharyang/movies-project/tree/master/data_exploration). 

## Model Training and Selection ## 

Check back here for updates on my progress for modelling. I'll be updating this section as I learn more about new machine learning models every week. 

## Prediction results ## 

Check back soon for updates to whether I can successfully predict the prices of movies on the iTunes store! 

## Feedback ## 

Your feedback on my data collection, exploration and modelling are much appreciated! Get in touch with me on [LinkedIn](https://www.linkedin.com/in/zachary-ang-824b2632/) or on my [blog](https://medium.com/@zachary.ahw)