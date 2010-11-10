import traceback
from Common.configobj import ConfigObj
#from pysqlite2 import dbapi2 as sqlite
import time
from Common.LogRoutine import *
import md5
import urllib
from google.appengine.ext import db
import StatusCodes
from DAOModels import *

  
# *Obj classes are wrapper classes to the DAO instances.

##################3 NOT USED YET
class GameObj( object ):
  """
  Game object...
  """

  # game model.
  game = None

  # PlayerObj list.
  players = []

class PlayerObj( object ):
  """
  player.....
  """

  player = None

class CountryObj( object ):
  """
  Country....
  """

  country = None

################# NOT USED YET

class DAO( object ):

  def __init__(self):
    self.log = getLogger(  )

    self.config = ConfigObj("Config/skajserver.cfg")


  def generateCountryMaster( self ):
    """
    Dummy...
    """
    entry1 = GameCountryMaster( map_name = "default", country_name="A", border_countries=["B","C","D"])
    db.put( entry1 )

    entry2 = GameCountryMaster( map_name = "default", country_name="B", border_countries=["A","C"])
    db.put( entry2 )
    
    entry3 = GameCountryMaster( map_name = "default", country_name="C", border_countries=["A","B","E"])
    db.put( entry3 )
    
    entry4 = GameCountryMaster( map_name = "default", country_name="D", border_countries=["A"])
    db.put( entry4 )
    
    entry5 = GameCountryMaster( map_name = "default", country_name="E", border_countries=["C"])
    db.put( entry5 )


  def getMasterCountries( self, map_name ):
    """
    Get a list of countries for a particular map.
    """


    self.log.info("DAO:getMasterCountries start")

    country_list = []
    status = StatusCodes.FAILED

    try:
      self.log.debug("Trying to get  %s"%(map_name) )
      
      country_list2 = db.GqlQuery("SELECT * FROM GameCountryMaster WHERE map_name = :1 ", map_name )
      
      if country_list2.count() > 0:
    
        # ugly... but want to check something
        for i in country_list2:
          country_list.append( i )

        status = StatusCodes.SUCCESSFUL

    except:
      self.log.error("DAO:getMasterCountries ex " + traceback.format_exc() )

    return ( status, country_list )
 
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

  def createGame( self, name, password, num_players, map_name ):
    self.log.info("DAO:createGame start")

    status = StatusCodes.SUCCESSFUL
    game = None

    try:
       
      game = Game( game_name = name, passwd = password, number_players = num_players, map_name=map_name)

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
      self.log.debug("Trying to get  %s"%(name) )
      
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
      self.log.debug("Trying to get %s"%(name) )
      
      game_list = db.GqlQuery("SELECT * FROM Game WHERE game_name = :1 ", name )
      
      self.log.debug("game count is " + str( game_list.count() ) )
      if game_list.count() > 0:
    
        self.log.debug("dir " + str( dir( game_list )))
        self.log.debug("list " + str( game_list ))

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

  def getAllPlayersForGame( self, game_name ):
    """
    Get all players for a game
    """

    self.log.info("DAO:getAllPlayersForGame start")

    player_list = []
    status = StatusCodes.PLAYER_NOT_IN_GAME

    try:
      
      
      player_list2 = db.GqlQuery("SELECT * FROM Player WHERE user_name = :1 and game_name = :2", user_name, game_name )
      
      
      if player_list2.count() > 0:
        for i in player_list2:
          player_list.append( i )

        status = StatusCodes.SUCCESSFUL

    except:
      self.log.error("DAO:getAllPlayersForGame ex " + traceback.format_exc() )

    return ( status, player_list)

  def createPlayer( self, user, game ):
    self.log.info("DAO:createPlayer start")

    status = StatusCodes.SUCCESSFUL
    player = None

    try:
      
      # hate the fact I'm using names and objects... 
      player = Player( user_name = user.name, game_name = game.game_name, user = user, game = game )

      db.put( player )

    except:
      self.log.error("DAO:createPlayer ex " + traceback.format_exc() )
      status = StatusCodes.FAILED

    return ( status, player )

      
########################################

  def createCountryForPlayer( self, game_name, player_name, country_name, num_armies ):
    self.log.info("DAO:createCountryForPlayer start")

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

  def getCountryForPlayer( self, game_name, player_name, country_name ): 
    """
    Get country for specific player/game combo.
    """
    self.log.info("DAO:getCountryForPlayer start")

    status = StatusCodes.SUCCESSFUL
    country = None

    try:

      country_list = db.GqlQuery("SELECT * FROM Country WHERE player = :1 and name = :2", player_name, game_name )
      
      
      if player_list.count() > 0:
    
        player = player_list.get()
        status = StatusCodes.SUCCESSFUL
      ( player_stat, player ) = self.getPlayerForGame( player_name, game_name )

      if player_stat == StatusCodes.SUCCESSFUL:
        # hate the fact I'm using names and objects... 
        country = Country( player = player, armies = num_armies, name = country_name )
        db.put( country )

    except:
      self.log.error("DAO:getCountryForPlayer ex " + traceback.format_exc() )
      status = StatusCodes.FAILED

    return ( status, country )

