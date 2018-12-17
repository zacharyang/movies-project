# Choose the countries that you want to get the iTunes movies from using the ISO-3166 Country Codes ## 

COUNTRIES=['us','sg','my','id','au','ph','th','vn','nz']

# There are typically two genres available through the iTunes API, action/adventures and documentaries ##

GENRES=['action-and-adventure']

# You will need two API keys, one for the TMdb database, one for the OMdb database # 

TMDB_API_KEY=""

OMDB_API_KEY=""

try:
	from private import *
except Exception:
	pass
