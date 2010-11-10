from google.appengine.ext import webapp
import traceback

# I feel like Harry....
from DAO.DAO import DAO
from DAO import StatusCodes
from Common.LogRoutine import *
from Common.configobj import ConfigObj
import random

class GameHandler( webapp.RequestHandler ):
    
  def __init__( self ):
    webapp.RequestHandler.__init__( self )

    self.log = getLogger()
    self.dao = DAO()  
    self.config = ConfigObj("Config/skajserver.cfg")


  def handleCreateGame(self, url):
    """
    Create a game... ..   DUH
    NO SECURITY YET.....
    """
    response = "sorry... operation failed"
    data = "<game>FAILED</game>"

    try:
      self.log.debug("GameHandler:handleCreateGame start")

      name = self.request.get("name")    
      password = self.request.get("password")
      num_players = int( self.request.get("num_players") )
      map_name = self.request.get("map_name", "default")
     
      (stat, game) =  self.dao.createGame( name, password, num_players, map_name )
          
      if stat == StatusCodes.SUCCESSFUL:
        self.log.debug("SUCCESSFULLY CREATED GAME " + name )
        data = "<game name=%s></game>"%( name )

    except:
      self.log.error("GameHandler:handleCreateGame  ex " + traceback.format_exc()  ) 
      
    self.response.out.write( data )

  def handleModifyGameState(self, url):
    """
    Create a game... ..   DUH
    NO SECURITY YET.....
    """
    response = "sorry... operation failed"
    data = "<game>FAILED</game>"

    try:
      self.log.debug("GameHandler:handleModifyGameState start")

      name = self.request.get("name")    
      state = self.request.get("state")
  
      
      (stat, game) =  self.dao.modifyGameState( name, state )
          
      if stat == StatusCodes.SUCCESSFUL:
        self.log.debug("SUCCESSFULLY MODIFIED STATE GAME " + name )
        data = "<game name=%s></game>"%( name )

    except:
      self.log.error("GameHandler:handleModifyGameState  ex " + traceback.format_exc()  ) 
      
    self.response.out.write( data )

  # will eventually go into a proper object for this.
  def populateGame( self, game ):
    """
    Assigns countries to players and does initial populating of armies.
    """

    # get list of countries for map name
    game_name = game.game_name
    (game_status, countries_list) = self.dao.getMasterCountries( game.map_name )

    # randomize list.
    random.shuffle( countries_list )

    # get players.
    (players_status, players_list) = self.dao.getAllPlayersForGame( game.game_name )

    # assign equals num of countries to players
    starting_armies = int( self.config["starting_armies"] )
    starting_countries = int( self.config["starting_countries"] )

    # need to check if enough countries.
    if len( players_list) * starting_countries > countries_list:
      self.log.error("NOT ENOUGH COUNTRIES FOR NUMBER OF PLAYERS")

    else:
      for player in players_list:

        for i in xrange( starting_countries ):
          country_name = countries_list.pop()
          self.dao.createCountryForPlayer( game_name, player.user_name, country_name, starting_armies )
      
  def handleStartGame(self, url):
    """
    Create a game... ..   DUH
    NO SECURITY YET.....
    """
    response = "sorry... operation failed"
    data = "<game>FAILED</game>"

    try:
      self.log.debug("GameHandler:handleStartGame start")

      name = self.request.get("name")    
 
      (stat, game) =  self.dao.modifyGameState( name, "STARTED" )
          
      if stat == StatusCodes.SUCCESSFUL:
        self.log.debug("SUCCESSFULLY MODIFIED STATE GAME " + name )

        # populate game with countries.
        self.populateGame( game )
        
        data = "<game name=%s>%s</game>"%( name, "STARTED" )

    except:
      self.log.error("GameHandler:handleStartGame  ex " + traceback.format_exc()  ) 
      
    self.response.out.write( data )

  def handleJoinGame(self, url):
    """
    Join a game... ..   DUH
    NO SECURITY YET.....

    1) Get username
    2) get token
    3) authenticate
    4) get game
    5) create player for game
    """
    response = "sorry... operation failed"
    data = "<game>FAILED</game>"

    try:
      self.log.debug("GameHandler:handleJoinGame start")

      user_name = self.request.get("username")
      token = self.request.get("token")
      state = self.request.get("state")
      game_name = self.request.get("gamename")
      
      ( stat, user ) =  self.dao.authenticateUser( user_name, token )

      if stat == StatusCodes.SUCCESSFUL:
        (game_status, game) = self.dao.getGame( game_name )

        if game_status == StatusCodes.SUCCESSFUL and game != None:

          # check if user has already joined the game.
          ( stat, player ) = self.dao.getPlayerForGame( user_name, game )
          
          if stat != StatusCodes.PLAYER_NOT_IN_GAME:

            # create the player.
            ( player_status, player) = self.dao.createPlayer( user, game )
            if player_status == StatusCodes.SUCCESSFUL:
              data = "<game>JOINED</game>"

    except:
      self.log.error("GameHandler:handleJoinGame  ex " + traceback.format_exc()  ) 
      
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
    if path == "/1/creategame":
      self.handleCreateGame( url )
    else:
      if path == "/1/modifygamestate":
        self.handleModifyGameState( url )
      else:
        if path == "/1/joingame":
          self.handleJoinGame( url )
        else:
          if path == "/1/startgame":
            self.handleStartGame( url )
          else:
            if path == "/foo":
              self.dao.generateCountryMaster()




