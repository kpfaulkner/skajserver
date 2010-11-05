from google.appengine.ext import webapp
import traceback

# I feel like Harry....
from DAO.DAO import DAO
from DAO import StatusCodes
from Common.LogRoutine import *
from Common.configobj import ConfigObj

class PlayerHandler( webapp.RequestHandler ):
    
  def __init__( self ):
    webapp.RequestHandler.__init__( self )

    self.log = getLogger()
    self.dao = DAO()  
    self.config = ConfigObj("Config/skajserver.cfg")

  def createPlayerHandler(self, url):
    """
    create player based on user that is logged in. 
    """
    response = "sorry... operation failed"
    data = "<user>FAILED</user>"

    try:
      
      self.log.debug("UserHandler:handleLogin")

      user_name = self.request.get("user_name")    
      token = self.request.get("token")    
      
      # need to know which game we're joining.
      game = self.request.get("game_name")

      if self.dao.authenticateUser( user_name, token ):

        # check if user has already joined the game.
        ( stat, player ) = self.dao.getPlayerForGame( user_name, game )
        
        if stat != StatusCodes.PLAYER_NOT_IN_GAME:

          # create the player.
          #player = Player( )
        # store.

      self.log.debug("user URL is " + user_name )

      (stat, user ) = self.dao.getUserWithPassword( user_name, password )

      print "stat is "+str(stat)

      #print "fooooooooooooo"

      if stat == StatusCodes.SUCCESSFUL:
        self.log.debug("SUCCESSFULLY RETRIEVED USER " + user_name )

        # get token.
        new_token = str( random.randrange(0,1000000000) )
        user.token = new_token
        
        # store it 
        self.dao.storeUser( user)

        data = "<user id=%s token=%s></user>"%( user_name, new_token )

    except:
      self.log.error("UserHandler:handleLogin ex " + traceback.format_exc()  ) 
      
    self.response.out.write( data )

  def setPlayerHandler(self, url):

  def getPlayerHandler( self, url):


    """
    Retrieve User.
    NO SECURITY YET.....
    MARKS the user as logged in (on the server?)
    """
    response = "sorry... operation failed"
    data = "<user>FAILED</user>"

    try:
      
      self.log.debug("UserHandler:handleGetUser")

      user_name = self.request.get("user_name")    
      password = self.request.get("password")    

      self.log.debug("user URL is " + user_name )

      (stat, user ) = self.dao.getUserWithPassword( user_name, password )

      print "stat is "+str(stat)

      #print "fooooooooooooo"

      if stat == StatusCodes.SUCCESSFUL:
        self.log.debug("SUCCESSFULLY RETRIEVED USER " + user_name )


        data = "<user id=%s token=%s></user>"%( user_name, user.token )

    except:
      self.log.error("UserHandler:handleGetUser ex " + traceback.format_exc()  ) 
      
    self.response.out.write( data ) 
            
  def handleCreateUser(self, url):
    """
    Create a user... ..   DUH
    NO SECURITY YET.....
    """
    response = "sorry... operation failed"
    data = "<user>FAILED</user>"

    try:
      
      d = str(dir(self.request ))
      self.log.debug("D " + d )
      self.log.debug("path "+self.request.path)
      self.log.debug("path_url " + self.request.path_url)
      self.log.debug("UserHandler:handleCreateUser")
      data = "success2"
      user_name = self.request.get("user_name")    
      password = self.request.get("password")    
      data = "success3"
      self.log.debug("user URL is " + user_name )

      (status, user ) = self.dao.createUser( user_name, password )
      data = "success4"
      
      #print "fooooooooooooo"

      if status == StatusCodes.SUCCESSFUL:
        self.log.debug("SUCCESSFULLY CREATED USER " + user_name )
        data = "<user name=%s></user>"%(user_name)

    except:
      self.log.error("UserHandler:handleCreateUser ex " + traceback.format_exc()  ) 
      
    self.response.out.write( data )

  def get(self, url):
    """
    handle various User based gets
    """

    self.log.debug("URL is " + url)
    
    path = self.request.path
    self.log.debug("path is " + path)

    # dict string --> method.
    # FIXME
    if path == "/1/createuser":
      self.handleCreateUser( url )
    else:
      if path == "/1/login":
        self.handleLogin( url )
      else:
        if path == "/1/getuser":
          self.handleGetUser( url )



