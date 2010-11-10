import traceback
from Common.configobj import ConfigObj
#from pysqlite2 import dbapi2 as sqlite
import time
from Common.LogRoutine import *
import md5
import urllib
from google.appengine.ext import db
import StatusCodes

class User( db.Model ):
  """
  Represents the user acct. NOT just a user within a particular game.
  For players within a specific game, see Player class.
  """
  name = db.StringProperty( required = True )
  passwd = db.StringProperty( required = True )
  number_wins = db.IntegerProperty( required = False )
  number_losses = db.IntegerProperty( required = False )

  # token the user needs to pass for all requests to prove they're who they say they are.
  # this is just a temporary measure until I figure out what to do for real.
  # empty token means not logged in.
  token = db.StringProperty( required = False )

# very basic... not normalized... but simple.
class GameCountryMaster( db.Model ):

  map_name = db.StringProperty( required = True )
  country_name = db.StringProperty( required = True )
  border_countries = db.StringListProperty( required = True )
  

class Game( db.Model ):

  STATE_NOT_STARTED = "notstarted"
  STATE_STARTED = "started"

  game_name = db.StringProperty( required = True )
  turn = db.StringProperty( required = False )
  state = db.StringProperty( required = False )

  # name of map.
  map_name = db.StringProperty( required = True )

  # number of REAL players, not including a dummy player for the 
  # non-taken land.
  number_players = db.IntegerProperty( required = True )

  # password to join game.
  passwd = db.StringProperty( required = False )



#class Map( db.Model ):

  # many many countries.
  #game = db.ReferenceProperty( Game, required=True )

class Player( db.Model ):

  # unsure how to do queries with using reference values.
  # eg, I'd want to do: SELECT * FROM Player WHERE game='mygame' and user.name="fred"
  # so will include game names and usernames in this entry aswell.
  # dont like it... but will keep this here for the moment.

  # username
  user_name = db.StringProperty( required = True )
  game_name = db.StringProperty( required = True )

  # user associated with this player.
  user = db.ReferenceProperty( User, required = True )

  # associated with a particular map.
  #game_map = db.ReferenceProperty( Map, required = True )

  # associate with a game
  game = db.ReferenceProperty( Game, required=True )

  # bonus's...   not used yet.
  bonus = db.StringProperty( required = False )
  
      
# country for a specific game instance...
class Country( db.Model ):

  player = db.ReferenceProperty( Player, required = True )
  armies = db.IntegerProperty( required = True )

  # name, eg. western australia
  name = db.StringProperty( required = True )