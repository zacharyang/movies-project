import requests as rq
import regex as re
import json
import settings 
from bs4 import BeautifulSoup

def collect_rss_movies():

    """

    Query the RSS feed to get 200 latest movies from each country from a specified 
    list of countries and across different specified genres

    """
    
    genres=settings.GENRES
    countries=settings.COUNTRIES

    results={}
    rss_url ='https://rss.itunes.apple.com/api/v1/%s/movies/top-movies/%s/200/explicit.json'
    
    print('Getting iTunes data...')

    for country in countries:
        country_results=[]
        
        for genre in genres:
            r = rq.get(rss_url % (country,genre)).json()
            genre_results=r['feed']['results']
            country_results+= genre_results
            
        results[country]=country_results
        
        print('%d movies indexed from %s iTunes Store' %((len(results[country]),country.upper())))
        
    return results

def get_info_by_id(movies_dict):
    
    """ 
    
    Get all iTunes movie information using the iTunes Search API, looking up by iTunes ID
    Caches all the data into the data directory

    """
    
    results=[]
    
    for country in movies_dict.keys():
        country_movies=[]
        country_movie_ids=[ a['id'] for a in movies_dict[country]]
        
        for i in country_movie_ids:
            r=rq.get('https://itunes.apple.com/lookup?id=%s&country=%s' % (i,country)).json()
            country_movies += r['results']
            
        results+= country_movies
        
    # Put all the itunes results into a json file in the data directory #
    with open('./data/itunes_data.json', 'w') as outfile:
        json.dump(results, outfile)
        
    return results



def get_search_dat(data):
    
    """
    This is to set up the iTunes data for searching by keyword in the TMdb database

       Step 1 - Remove all "bundled" movies, eg. collections
       Step 2 - Parse the data, removing all spaces, special characters. 
                eg. Gangs of New York => Gangs+of+New+York
       Step 3 - Drop all the duplicates that arise after parsing.
                eg. Full Metal Jacket (1987) => Full Metal Jacket => Full+Metal+Jacket
       Step 4 - Compile a dictionary of 4 variables, i. Movie Titles, ii. Year of Release, 
                iii. Formatted Search Strings, iv. iTunes ID. The last is essential to keep in
                search data to link back to the iTunes data. 

    """ 
    
    titles=[]
    years=[]
    itunes_id=[]
    dropped_dat=[]

    
    for a in data:
        if a['wrapperType'] =='track':
            titles.append(a['trackName'])
            years.append(a['releaseDate'][:4])
            itunes_id.append(a['trackId'])
    
    # Drop all "bundle" type movies, eg. sequel bundles # 
        else:
            dropped_dat.append(a['collectionName'])
    print( '%s collection bundles dropped from search' % ((str(len(dropped_dat)))) )
    
    # Parsing - removing spaces, special characters not permitted in search string # 
    
    names_without_bracket_y=[re.sub(r' \([^)]*\)', '',a) for a in titles] 
    names_without_punctuation=[re.sub(r"[^\w\d-'\s]",'',a) for a in names_without_bracket_y]
    names_without_punctuation_double_space=[a.replace('  ',' ') for a in names_without_punctuation]
    search_str=[a.replace(' ','+') for a in names_without_punctuation_double_space]

    # Dropping duplicates from the search # 

    seen_ind=[]
    seen=set()
    for i, v in enumerate(search_str):
        if v not in seen:
            seen_ind.append(i)
        seen.add(v)
    
    search_dat={
        
        'titles':[titles[i] for i in seen_ind],
        
        'years':[years[i] for i in seen_ind],
        
        'search_strs':[search_str[i] for i in seen_ind],
        
        'itunes_id':[itunes_id[i] for i in seen_ind]
    
    }
    print( '%s duplicates removed from search' % (str((len(search_str)-len(search_dat['titles'])))))
    
    
    return search_dat


def get_TMDB_ids(search_dat,specify_year=True):
    
    """
       Queries the TMdb API to get movie information, searching by keyword.
       We want to obtain a unique TMdb ID, so that we can hit the TMdb API again by ID to get a 
       IMdb ID, which can be used to make better queries on the OMdb database. 
       

       We allow to pass an argument to choose whether one can specify the year of the movie title.
       In the first instance, we would want to choose a stricter criteria so that we can narrow down 
       to a specific movie.

       We will then split the data into three parts: Those that return i. exact matches for keyword string to
       TMdb ID; ii. multiple matches to different TMdb IDs; iii. no matches to TMdb IDs.

    """
    
    print('Getting TMdb IDs from TMDdb database...')

    url="https://api.themoviedb.org/3/search/movie?api_key=%s&query=%s"
    api_key=settings.TMDB_API_KEY
    
    id_list=[]
    exact_matches=multiple_matches=no_matches=bad_response=0
    
    for a in range(len(search_dat['search_strs'])):
        
        if specify_year==True: 
            url_full=url%(api_key,search_dat['search_strs'][a])+'&year='+str(search_dat['years'][a])
        else:
            url_full=url%(api_key,search_dat['search_strs'][a])
            
            
        r=rq.get(url_full)

        if r.status_code==200:
            
            m=r.json()
            TMdb_titles=[a['title'] for a in m['results']]
            TMdb_id=[a['id'] for a in m['results']]

            # Search for exact title match # 
            if search_dat['titles'][a] in TMdb_titles:
                id_list.append(TMdb_id[TMdb_titles.index(search_dat['titles'][a])])
                exact_matches+=1
            # Search for result exact hit #
            elif m['total_results']==1:
                id_list.append(m['results'][0]['id'])
                exact_matches+=1
            # Search for multiple result hit, append a list of IDs to the results list #
            elif m['total_results']>1:
                id_list.append(TMdb_id)
                multiple_matches+=1
            # Search for null result hit, append an empty list to results list #
            elif m['total_results']==0:
                id_list.append(TMdb_id)
                no_matches+=1
        # Record Bad Response #
        else:
            id_list.append(None)
            bad_response+=1

    search_dat['TMdb_id']=id_list

    if specify_year==True:
        print('TMdb Keyword + Year Search Results: Exact Matches = %d, Multiple matches=%d, No matches=%d, Bad Response=%d' %(exact_matches,multiple_matches,no_matches,bad_response))

    else:
        print('TMdb Keyword-only Search Results: Exact Matches = %d, Multiple matches=%d, No matches=%d, Bad Response=%d' %(exact_matches,multiple_matches,no_matches,bad_response))


    # Subsetting the data into those with exact matches, multiple matches and no matches # 

    mult_ind=[isinstance(a,list) and len(a)>0 for a in id_list]
    multiple_match={k:[v for i,v in enumerate(search_dat[k]) if mult_ind[i]==True] for k in search_dat.keys()}
    no_Ind=[isinstance(a,list) and len(a)==0 for a in id_list]
    no_match={k:[v for i,v in enumerate(search_dat[k]) if no_Ind[i]==True] for k in search_dat.keys()}
    exact_ind=[isinstance(a,int)for a in id_list]
    exact_match={k:[v for i,v in enumerate(search_dat[k]) if exact_ind[i]==True] for k in search_dat.keys()}


    return search_dat, exact_match, no_match, multiple_match

def combine_search_results(results):

    """

    This function collapases a list of search results back together again arising from
    the get_TMdb_ids or get_search_dat functions.

    """    

    result={}
    # Set the keys first #
    keys=list(results[0].keys())

    for k in keys:
        result[k]=[]
    # Add the list of data by key #
    for d in results:
        for k,v in d.items():
            if len(v)>0:
                result[k]+= v  
            else:
                pass
    return result

def get_imdb_id_from_tmdb_id(search_dat):

    """
    This function takes a dictionary resulting from get_search_dat and queries the TMdb database by TMdb ID
    The purpose of this is to extract the IMdb IDs from the TMdb API, which can then be used to query the 
    OMdb database to extract more relevant info. 

    """

    results=[]
    missed=[]
    bad_response=0
    api_key=settings.TMDB_API_KEY
    
    print('Now getting IMdb IDs from TMdb database...')
    for a in search_dat['TMdb_id']:
        r = rq.get('https://api.themoviedb.org/3/movie/%s?api_key=%s' % (str(a),api_key))
        
        if r.status_code== 200:
            m = r.json()
            results.append(m)
        else:
            print('Bad Response')
            bad_response+=1
    
    imdb_ids=[a['imdb_id'] for a in results]
    search_dat['IMdb_id']=imdb_ids

    missed_ind=[a=='' for a in imdb_ids]
    missed={k:[v for i,v in enumerate(search_dat[k]) if missed_ind[i]==True] for k in search_dat.keys()}
    missed.pop('IMdb_id')
    leftover_ind= [not i for i in missed_ind]
    leftover={k:[v for i,v in enumerate(search_dat[k]) if leftover_ind[i]==True] for k in search_dat.keys()}

    # We're not going to use the TMdb data features, but we'll cache it nonetheless#

    with open('./data/tmdb_search_by_id_results.json', 'w') as outfile:
    	json.dump(results, outfile)

    print('Number of Bad Responses from TMdb database while looking for IMdb ID= ' + str(bad_response))
    return missed, leftover


def google_for_imdb_id(search_dat):

    """
        Takes a dictionary in the returned from get_serch_dat and extracts the IMdb ID from the first
        Google hit. 
    """

    IMDB_ids_list=[]
    successful_hits=0
    no_hits=0

    print('Googling for %s records with no match and multiple matches off the TMdb database' %str(len(search_dat['years'])))

    for a in range(len(search_dat['years'])):
        
        # Google 'Movie Name' + 'imdb' using BS#
        r=rq.get('https://www.google.com/search?q=%s+%s+imdb'% (search_dat['search_strs'][a],search_dat['years'][a] )) 
        p= BeautifulSoup(r.text,'html.parser')
        
        # Take the first search result hyper link # 
        
        first_google_hit=p.find_all('h3', {'class':'r'})[0] 
        m=re.search('title/(.+?)/&',str(first_google_hit))
        
        # If successful, store IMdb ids to a list, if not, store a NaN value #
        if m:
            IMDB_id=m.group(1)
            IMDB_ids_list.append(IMDB_id)
            successful_hits+=1
        else:
            IMDB_ids_list.append('NaN')
            no_hits+=1
    
    print('Successful IMDB_ids found via Google = ' + str(successful_hits) + ' No results = '+ str(no_hits))
    
    # Store in the original dictionary with key 'IMdb_id' # 
    search_dat['IMdb_id']=IMDB_ids_list


    return search_dat


def get_data_from_omdb(search_dat):
   
    """
        Takes a dictionary returned from get_search_dat and looks up the OMdb data base, 
        querying by IMdb ID, then unpacks and parses ratings data. 

    """
    print('Getting data on %d titles from OMdb...' % len(search_dat['IMdb_id']))
    results=[]
    api_key=settings.OMDB_API_KEY
    missed=0
    bad_response=0
    for imdb_id in search_dat['IMdb_id']:
        if imdb_id == None or imdb_id== 'NaN':
            results.append([])
            missed+=1
        else:
            r=rq.get('http://www.omdbapi.com/?apikey=%s&i=%s'% (api_key, imdb_id))
            if r.status_code== 200:
                m = r.json()
                results.append(m)
            else:
                print('Bad Response for ' + str(imdb_id))
                    
    hit_results=[a for a in results if len(a)>3]
    print('%d IMdb IDs returned no results from the OMdb database' %missed)

    for i,a in enumerate(hit_results):
        a['RT_score']=a['Metacritic_score']=a['IMdb_score']='NaN'
        
        if len(a['Ratings'])==0:
            pass
        
    # Iterate through the Ratings element, stored as a list of dictionaries #        
        for b in a['Ratings']:

            if b['Source'] == 'Internet Movie Database':
                a['IMdb_score']= float(b['Value'][:3])*10
            elif b['Source'] == 'Rotten Tomatoes':
                a['RT_score']= float(b['Value'].split('%')[0])
            elif b['Source'] == 'Metacritic':
                a['Metacritic_score'] = float(b['Value'].split('/')[0])
        
        del a['Ratings']


        ## Actors first, split by commas and store the first two + number of actors ## 
        a['actor_1']=a['actor_2']='NaN'
        a['num_actor']=0
        actor_list=a['Actors'].split(',')
        if actor_list[0]=='N/A':
            pass
        elif len(actor_list)==1:
            a['actor_1']=actor_list[0].strip(' ')
            a['num_actor']=1
        else:
            a['actor_1']=actor_list[0].strip(' ')
            a['actor_2']=actor_list[1].strip(' ')
            a['num_actor']= len(actor_list)
        
        ## Directors next, same task as above ## 
        a['director_1']=a['director_2']='NaN'
        a['num_director']=0
        director_list=a['Director'].split(',')
        if director_list[0]=='N/A':
            pass
        elif len(director_list)==1:
            a['director_1']=director_list[0].strip(' ')
            a['num_director']=1
        else:
            a['director_1']=director_list[0].strip(' ')
            a['director_2']=director_list[1].strip(' ')
            a['num_director']= len(director_list)
    
    with open('./data/OMdb_data.json', 'w') as outfile:
        json.dump(hit_results,outfile)


def collect():

    rss_itunes=collect_rss_movies()
    itunes=get_info_by_id(rss_itunes)
    movie_search_dat=get_search_dat(itunes)

    ## TMdb Run 1 - Query by Keyword + Year  ## 

    movie_dat_TMdb,exact_match_run1,no_match_run1,multi_match_run1=get_TMDB_ids(movie_search_dat)

    ## TMdb Run 2 - Query by Keyword only ## 

    movie_dat_TMdb_run2,exact_match_run2,no_match_run2,multi_match_run2=get_TMDB_ids(no_match_run1,specify_year=False)

    num_exact_matches=len(exact_match_run1['TMdb_id'])+len(exact_match_run2['TMdb_id'])
    pct_match= float(num_exact_matches*100/len(movie_search_dat['TMdb_id']))

    print('%.2f percent of keyword searches on the TMdb database returned exact matches for TMdb IDs' % pct_match)

    ## TMdb Run 3 - Getting IMdb IDs by TMdb IDs ## 

    TMdb_search=combine_search_results([exact_match_run1,exact_match_run2])
    missed_IDs,matched_IDs=get_imdb_id_from_tmdb_id(TMdb_search)

    ## Google for the movies that did not get a hit, or multiple hits on TMdb ## 
    no_hit=combine_search_results([multi_match_run1,multi_match_run2,missed_IDs,no_match_run2])
    google_results=google_for_imdb_id(no_hit)

    ## Combine everything together to pass through the OMdb database ## 

    all_hits=combine_search_results([google_results,matched_IDs])

    with open('./data/OMdb_search_dat.json','w') as outfile:
        json.dump(all_hits,outfile)

    ## Search the OMdb database # 

    OMdb_data= get_data_from_omdb(all_hits)

    print('Data collection complete')

if __name__ == "__main__": 

    collect()




















