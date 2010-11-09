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

class Game( db.Model ):

  STATE_NOT_STARTED = "notstarted"
  STATE_STARTED = "started"

  game_name = db.StringProperty( required = True )
  turn = db.StringProperty( required = False )
  state = db.StringProperty( required = False )

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

  
class DAO( object ):

  def __init__(self):
    self.log = getLogger(  )
    self.log.info("XXXXXXX")

    self.config = ConfigObj("Config/skajserver.cfg")


  def authenticateUser( self, username, token ):
    """
    Confirm that username and token match what the server thinks.
    """

    user = None
    status = StatusCodes.FAILED

    try:

      (stat, user) = self.getUser( username )

      # check passwd.
      if stat == StatusCodes.SUCCESSFUL:
        if user.token == token:
          status = StatusCodes.SUCCESSFUL
        else:
          status = StatusCodes.USER_NOT_LOGGED_IN

    except:
      self.log.error("DAO:getUserWithPassword ex " + traceback.format_exc() )


    return ( status, user )

  def storeUser( self, user ):
    """
    Just store the user.
    """

    db.put( user )

  def getUserWithPassword( self, username, password ):
    """
    Get user based on username and verify the passwd is correct
    This is for external consumption
    Dont like the idea of returning None, but hey....
    """

    self.log.info("DAO:getUserWithPassword start")

    user = None
    status = StatusCodes.FAILED

    try:

      ( stat, user ) = self.getUser( username )

      # check passwd.
      if stat == StatusCodes.SUCCESSFUL:
        if user.passwd == password:
          status = StatusCodes.SUCCESSFUL
        else:
          status = StatusCodes.USER_PASSWORD_INCORRECT

    except:
      self.log.error("DAO:getUserWithPassword ex " + traceback.format_exc() )

    return ( status, user)

  def getUser( self, username  ):
    """
    Get user based on username.
    Dont like the idea of returning None, but hey....
    """

    self.log.info("DAO:getUser start")

    user = None
    status = StatusCodes.USER_DOES_NOT_EXIST

    try:
      self.log.debug("Trying to get  %s"%(username) )
      
      user_list = db.GqlQuery("SELECT * FROM User WHERE name = :1 ", username )
      
      
      if user_list.count() > 0:
    
        user = user_list.get()
        status = StatusCodes.SUCCESSFUL

    except:
      self.log.error("DAO:getUser ex " + traceback.format_exc() )

    return ( status, user)

  def createUser( self, username, password ):
    self.log.info("DAO:createUser start")

    status = StatusCodes.SUCCESSFUL
    user = None

    try:
       
      (stat, user) = self.getUser( username )
      
      self.log.debug("status is " + str( stat) )
      if stat == StatusCodes.USER_DOES_NOT_EXIST:
        user = User( name = username, passwd = password)
        db.put( user )
      else:
        self.log.warning("DAO:createUser user already exists " + username  )
        status = StatusCodes.USER_ALREADY_EXISTS
  
    except:
      self.log.error("DAO:createUser ex " + traceback.format_exc() )

    return ( status, user )

 
 #########################################

 # GAME

  def createGame( self, name, password, num_players ):
    self.log.info("DAO:createGame start")

    status = StatusCodes.SUCCESSFUL
    game = None

    try:
       
      game = Game( game_name = name, passwd = password, number_players = num_players)

      db.put( game )

    except:
      self.log.error("DAO:createUser ex " + traceback.format_exc() )

    return ( status, game )
  
  def getGame( self, name ):
    """
    Get game based on name.
    Dont like the idea of returning None, but hey....
    """

    self.log.info("DAO:getGame start")

    game = None
    status = StatusCodes.GAME_DOES_NOT_EXIST

    try:
      self.log.debug("Trying to get  %s"%(username) )
      
      game_list = db.GqlQuery("SELECT * FROM Game WHERE game_name = :1 ", name )
      
      
      if game_list.count() > 0:
    
        game = game_list.get()
        status = StatusCodes.SUCCESSFUL

    except:
      self.log.error("DAO:getGame ex " + traceback.format_exc() )

    return ( status, game)
    
  def modifyGameState( self, name, state ):
    
    self.log.info("DAO:modifyGameState start")

    game = None
    status = StatusCodes.GAME_DOES_NOT_EXIST

    try:
      self.log.debug("Trying to get  %s"%(name) )
      
      game_list = db.GqlQuery("SELECT * FROM Game WHERE game_name = :1 ", name )
      
      if game_list.count() > 0:
    
        game = game_list.get()
        game.state = state
        db.put( game )

        status = StatusCodes.SUCCESSFUL

    except:
      self.log.error("DAO:getGame ex " + traceback.format_exc() )

    return ( status, game)   

    ##############################3
    # PLAYER

  def getPlayerForGame( self, user_name, game_name ):
    """
    Get Player for particular user and game combo.
    Dont like the idea of returning None, but hey....
    """

    self.log.info("DAO:getPlayerForGame start")

    player = None
    status = StatusCodes.PLAYER_NOT_IN_GAME

    try:
      
      
      player_list = db.GqlQuery("SELECT * FROM Player WHERE user_name = :1 and game_name = :2", user_name, game_name )
      
      
      if player_list.count() > 0:
    
        player = player_list.get()
        status = StatusCodes.SUCCESSFUL

    except:
      self.log.error("DAO:getPlayerForGame ex " + traceback.format_exc() )

    return ( status, player)

  def createPlayer( self, user, game ):
    self.log.info("DAO:createPlayer start")

    status = StatusCodes.SUCCESSFUL
    player = None

    try:
      
      # hate the fact I'm using names and objects... 
      player = Player( user_name = user.name, game_name = game.name, user = user, game = game )

      db.put( player )

    except:
      self.log.error("DAO:createPlayer ex " + traceback.format_exc() )
      status = StatusCodes.FAILED

    return ( status, player )

      
########################################

  def createCountryForPlayer( self, player_name, country_name, num_armies, game_name ):
    self.log.info("DAO:createCountry start")

    status = StatusCodes.SUCCESSFUL
    country = None

    try:
      
      ( player_stat, player ) = self.getPlayerForGame( player_name, game_name )

      if player_stat == StatusCodes.SUCCESSFUL:
        # hate the fact I'm using names and objects... 
        country = Country( player = player, armies = num_armies, name = country_name )
        db.put( country )

    except:
      self.log.error("DAO:createCountryForPlayer ex " + traceback.format_exc() )
      status = StatusCodes.FAILED

    return ( status, country )


