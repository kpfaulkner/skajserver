from google.appengine.ext import webapp
import traceback

# I feel like Harry....
from DAO.DAO import DAO
from DAO import StatusCodes
from Common.LogRoutine import *
from Output.HTMLGenerator import HTMLGenerator
from Common.configobj import ConfigObj

class StoreHandler(webapp.RequestHandler):
    
  def __init__( self ):
    webapp.RequestHandler.__init__( self )

    self.log = getLogger()
    self.dao = DAO()  
    self.output_generator = HTMLGenerator()
    self.config = ConfigObj("Config/linkmenow.cfg")

  def validate_short_url( self, url ):
    """
    removes spaces, checks length etc.
    
    Returns the modified URL.
    """
    
    self.log.info("StoreHandler::validate_short_url start")
    
    valid_url = url
    
    try:
    
      if url != None and url != "":
        
        max_length = int( self.config['LinkMeNow']['MaxShortURLLength'] )
        
        url = url.replace(" ", "")
        url = url.lower()
        
        if len(url) > max_length:
        
          # this will force some numerical representation.
          # if the user doesn't like it, they can try again.
          url = None
          
        valid_url = url
        
        #self.log.debug("valid url " + str( valid_url ) )
            
    except:
      self.log.error("StoreHandler::validate_short_url ex " + traceback.format_exc() )
    
    
    return valid_url
    
    
        
  def validate_long_url( self, url ):
    """
    Make sure that url doesn't have any of the banned urls in the config.
    """
    
    self.log.info("StoreHandler::validate_long_url start")
    
    valid_url = True
    
    small_url = url.lower()
        
        
    # yucky hard coded case for own blog.
    if small_url.find("blog.linkmenow.org") == -1:
      
      try:
        banned_urls = self.config['LinkMeNow']['BannedDomains']
        
        self.log.debug("url " + small_url )
         
        for b in banned_urls:
          
          self.log.debug("banned url " + b )
          
          # substring search for banned urls.
          if small_url.find( b ) != -1:
            valid_url = False
            break
      
        self.log.debug("is valid url " + str( valid_url ) )
              
      except:
        self.log.error("StoreHandler::validate_long_url ex " + traceback.format_exc() )
      
    
    return valid_url
    
    
  def __process_data( self, long_url = None, short_url = None , creator = None, tags=None ):
    """
    Some basic rules setup.
    
    1) dont feed them after midnight....
      sorry... wrong movie.
      
    1) If short url isn't supplied, then generate a number as the short URL.
    2) If the short url IS supplied and it already exists, we need to check that the "creator" is the same for the new url as well as the old.
       THE ONLY EXCEPTION TO THIS IS WHEN THE CREATOR IS AUTO, IN THAT CASE WE DO NOT ALLOW REPLACING OF URLS.
       
    """
    response = "Sorry, can't store entry"
    
    try:      
      if self.validate_long_url( long_url ):
         
        short_url = self.validate_short_url( short_url )
        
        # make sure long_url and creator aren't empty.
        if long_url != None and long_url != "" and creator != None and creator != "":
          
          
          # just incase the random number value is already used. (ie, someones actually used that combination of characters).
          # try it again 3 times, else bomb out.
        
          count = 3
          while count > 0:
            count -= 1
            
            if short_url == None or short_url == "":
            
            
              # CODE IS BORKED.... THIS DOESN'T RETURN ANYTHING, BUT CODE LATER ON HANDLES IT. REMOVE THIS!!!!! FIXME FIXME FIXME
              short_url = self.dao.get_next_number()
              
            result_url, status_code = self.dao.replace_entry( short_url, long_url, creator, tags )
            if status_code == StatusCodes.SUCCESSFUL:
              break
      
          if status_code == StatusCodes.SUCCESSFUL:
            
            response = self.output_generator.generate_successful_save( result_url, long_url )
            #response = self.output_generator.generate_message("Success!!", "%s has reduced to <a href=%s >%s</a>"%(long_url, result_url, result_url) )
             
          else:
            
            response = self.output_generator.generate_unsuccessful_save( result_url, long_url, status_code )
            
        else:
          if creator == None or creator == "":
            response = self.output_generator.generate_unsuccessful_save( short_url , long_url, StatusCodes.INVALID_CREATOR  )   
      else:
        
        response = self.output_generator.generate_unsuccessful_save( short_url , long_url, StatusCodes.INVALID_LONG_URL  )    
    except:
      self.log.error("StoreHandler::post ex " + traceback.format_exc()  )
      
      
    return response
        
    
  def post( self, data  ):
    response = "sorry... operation failed"
    
    try:
    
      self.log.debug("StoreHandler post")
      
      long_url = self.request.get("LONG_URL")    
      short_url = self.request.get("SHORT_URL")
      creator = self.request.get("CREATOR")
      tags = self.request.get("TAGS")
    
      self.log.debug("post environ" + str( self.request.environ) )
      
      
      response = self.__process_data( long_url, short_url, creator, tags )
      
    except:
      self.log.error("StoreHandler::post ex " + traceback.format_exc()  )
      
    self.response.out.write( response )      
            
  def get(self, url):
    """
    Main "index.html" routine.
    ie, displays hello etc :)
    
    """
    response = "sorry... operation failed"
    
    try:
      
      self.log.debug("StoreHandler get")
      
      long_url = self.request.get("LONG_URL")    
      short_url = self.request.get("SHORT_URL")
      creator = self.request.get("CREATOR")
      tags = self.request.get("TAGS")
      
      #self.log.debug("short " + str( unicode( short_url ) ) )
      self.log.debug("short url type " + str( type( short_url ) ) )
      
      #self.log.debug("long " + str( long_url ) )
      
      response = self.__process_data( long_url, short_url, creator, tags )
      
    except:
      self.log.error("StoreHandler::get ex " + traceback.format_exc()  ) 
      
    self.response.out.write( response )
