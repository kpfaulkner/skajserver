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
  name = db.StringProperty( required = True )
  passwd = db.StringProperty( required = True )
  number_wins = db.IntegerProperty( required = False )
  number_losses = db.IntegerProperty( required = False )

class Game( db.Model ):

  turn = db.StringProperty( required = True )
  state = db.StringProperty( required = True )

  # number of REAL players, not including a dummy player for the 
  # non-taken land.
  number_players = db.IntegerProperty( required = True )


class Map( db.Model ):

  # many many countries.
  game = db.ReferenceProperty( Game, required=True )

class Player( db.Model ):

  # user associated with this player.
  user = db.ReferenceProperty( User, required = True )

  # associated with a particular map.
  game_map = db.ReferenceProperty( Map, required = True )

  # bonus's...   not used yet.
  bonus = db.StringProperty( required = False )
  
      
# country for a specific game instance...
class Country( db.Model ):

  player = db.ReferenceProperty( Player, required = True )
  armies = db.IntegerProperty( required = True )


class DAO( object ):

  def __init__(self):
    self.log = getLogger(  )
    
    self.config = ConfigObj("Config/skajserver.cfg")


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

 
    
