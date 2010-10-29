from google.appengine.ext import webapp
import traceback
from Common.LogRoutine import *


class MainHandler(webapp.RequestHandler):
    
  def __init__( self ):
    webapp.RequestHandler.__init__( self )

    self.log = getLogger()
        
  def get(self):
    """
    Main "index.html" routine.
    ie, displays hello etc :)
    
    """
    
    try:
      

      
      data = "hello"
      #data = open( "index.html").read()
      self.log.debug("data " + data )
      
      self.response.out.write( data )
      
    except:
      print "MainHandler ex " + traceback.format_exc() 
