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
  number_wins = db.IntegerProperty( required = True )
  number_losses = db.IntegerProperty( required = True )
  

class Game( db.Model ):

  players = db.ListProperty(  User )
  turn = db.StringProperty( required = True )
  state = db.StringProperty( required = True )
  map = db.
  
  
class Entry( db.Model ):
  long_url  = db.StringProperty( required = True )
  short_url = db.StringProperty( required = False )
  creator   = db.StringProperty( required = True )
 
  times_retrieved = db.IntegerProperty( required = False )

# cant be stuffed with tag-->id lookup table.
# will adjust it if size ever becomes an issue.
class URLTag( db.Model ):
  short_url = db.StringProperty( required = True )
  tag = db.StringProperty( required = True )
     
class Unique_Number( db.Model ):
 
  short_url = db.StringProperty( required = True )
  creator   = db.StringProperty( required = True )
  
class DAO( object ):
  
  def __init__(self):
    self.log = getLogger(  )
    
    self.config = ConfigObj("Config/linkmenow.cfg")


  def entry_to_dict( self, entry ):
    """
    Converts an "Entry" instance to a dict.
    """
    pass
    
  def urltag_to_dict( self, tag ):
    """
    Converts URLTag instance to dict.
    """
    pass
    
    
  def get_stats( self, short_url, creator ):
    self.log.info("DAO::get_stats start")
    
    stats = {}
    
    try:
    
      self.log.debug("Trying to get  %s:%s"%(short_url, creator) )
      
      long_url_list = db.GqlQuery("SELECT * FROM Entry WHERE short_url = :1 and creator = :2", short_url, creator )
      
      
      if long_url_list.count() > 0:
        entry = long_url_list.get()
        if entry.long_url != None:
          long_url = entry.long_url
          
          stats['VALID'] = True
          
          # yucky magic!!!!
          if entry.times_retrieved == None:
            stats['RECALL'] = 0
          else:
            stats['RECALL'] = int( entry.times_retrieved )
      else:
        stats['RECALL'] = 0
        stats['VALID'] = False
          
    except:
      self.log.error("DAO::get_stats ex " + traceback.format_exc() )
      
      
    return stats
        
  def get_long_url( self, short_url ):
    self.log.info("DAO::get_long_url start")
    
    long_url = None
    
    try:
    
      
      if not isinstance( short_url, unicode):
        short_url = unicode( short_url , "UTF-8") 
      
      #self.log.debug("Trying to get " + str( short_url ) )
      
      long_url_list = db.GqlQuery("SELECT * FROM Entry WHERE short_url = :1", short_url )

      
      if long_url_list != None and long_url_list.count() > 0:
        entry = long_url_list.get()
        if entry.long_url != None:
          long_url = entry.long_url
          
          if entry.times_retrieved == None:
            entry.times_retrieved = 0
            
          entry.times_retrieved += 1
          db.put( entry )
          
      self.log.debug("long url is " + str( long_url ) )
        
    except:
      self.log.error("DAO::get_long_url ex " + traceback.format_exc() )
      
      
    return long_url

    
  def get_short_url( self, long_url ):
    self.log.info("DAO::get_short_url start")
    
    short_url = None
    
    try:
    
      short_url_list = db.GqlQuery("SELECT short_url FROM Entry WHERE long_url = :1", long_url )

      if len( short_url_list ) > 0:
        short_url = short_url_list[ 0 ]
        
    except:
      self.log.error("DAO::get_short_url ex " + traceback.format_exc() )
      
      
    return short_url


  def insert_entry( self, s_url, l_url, user ):
    self.log.info("DAO::insert_entry start")
    
    try:
    
      entry = Entry( short_url = s_url, long_url = l_url, creator = user,times_retrieved = 0  )
      
      db.put( entry )
      
    except:
      self.log.error("DAO::insert_entry ex " + traceback.format_exc() )



  def get_all_entries_for_creator( self, creator ):
    self.log.info("DAO::get_all_entries_for_creator start")
    
    entry_list = []
    
    
    try:
    
      l = db.GqlQuery("SELECT * FROM Entry WHERE creator = :1", creator )

      if l.count() > 0:
        entry_list = l
        
    except:
      self.log.error("DAO::get_all_entries_for_creator ex " + traceback.format_exc() )
      
      
    return entry_list

  def get_all_entries_for_tag( self, tag ):
    self.log.info("DAO::get_all_entries_for_tag start")
    
    entry_list = []
    
    
    try:
    
      l = db.GqlQuery("SELECT * FROM URLTag WHERE tag = :1", tag )

      if l.count() > 0:
        entry_list = l
        
    except:
      self.log.error("DAO::get_all_entries_for_tag ex " + traceback.format_exc() )
      
      
    return entry_list
    

  def get_entry( self, short_url, creator ):
    self.log.info("DAO::get_entry start")
    
    entry = None
    
    try:
    
      entry_list = db.GqlQuery("SELECT * FROM Entry WHERE short_url = :1 and creator = :2", short_url, creator )

      if len( entry_list ) > 0:
        entry = entry_list[ 0 ]
        
    except:
      self.log.error("DAO::get_entry ex " + traceback.format_exc() )
      
      
    return entry

  def get_entry_from_short_url( self, short_url ):
    self.log.info("DAO::get_entry_from_short_url start")
    
    entry = None
    
    try:
    
      entry_list = db.GqlQuery("SELECT * FROM Entry WHERE short_url = :1  ", short_url  )

      if entry_list.count() > 0:
        entry = entry_list.get()
        
    except:
      self.log.error("DAO::get_entry_from_short_url ex " + traceback.format_exc() )
      
      
    return entry
        
  def replace_entry( self, s_url, l_url, user, tags ):
    """
    Tries to replace... otherwise, inserts
    """
    self.log.info("DAO::replace_entry start")
    
    result_url = None
    
    status = StatusCodes.FAILED
    
    try:
    
      self.log.debug("db " + str( dir( db ) ) )
      
      entry = None
      
      if s_url != None:
      
        # make sure we're dealing with lowercase only!
        s_url = s_url.lower()
        
        entry = self.get_entry_from_short_url( s_url )
      
        if entry != None:
          self.log.debug("entry long is " + str( entry.long_url ) )
          self.log.debug("entry short is " + str( entry.short_url ) )
        
      self.log.debug("tags" + str( tags ) )
      
      # get list of special users where replacing of their URLs are NOT allowed.
      # This is a nasty special case for the "AUTO" user.
      dont_replace_content_users = self.config['LinkMeNow']['SpecialUsernames']
      
      # same user replacing their entry.
      if s_url != None and entry != None and entry.creator == user and entry.creator not in dont_replace_content_users:
        
        db.delete( entry )
        
        entry.long_url = l_url
        
        db.put( entry )
        status = StatusCodes.SUCCESSFUL
                
      else:

        # short_url exists, but wrong user.
        if entry != None and entry.creator != user:
          status = StatusCodes.INVALID_CREATOR
          
        else:
          if entry != None and user in dont_replace_content_users:
            status = StatusCodes.SHORT_URL_TAKEN
          
          else:
            
            # create a new one?
            if entry == None:
              entry = Entry( short_url = s_url, long_url = l_url, creator = user, times_retrieved = 0  )
    
              db.put( entry )
    
              # if s_url is empty, then replace the short_url with the id.
              if s_url == None or s_url == "":
                iid = entry.key().id()
                
                encoded_short_url = base36encode( iid )
                
                self.log.debug("ENCODED " + str( encoded_short_url ).lower()  )
                
                s_url = str( encoded_short_url ).lower()
                entry.short_url = s_url
                self.log.debug("about to store")
                
                db.put( entry )
              
                self.log.debug("setting to success")
                
              status = StatusCodes.SUCCESSFUL
      
      self.log.debug("current status %d"%( status ) )
      
      if status == StatusCodes.SUCCESSFUL:
        # now add tags for the URL.

        self.log.debug("tags type " + str( type( tags ) ) )
        
        if tags != None and tags != "":
          tag_list = tags.split(",") 
        else:
          tag_list = []
          
        status = self.set_tags_for_short_url( s_url, tag_list )
                    
      #result_url = self.generate_short_url( entry )
        
    except:
      self.log.error("DAO::replace_entry ex " + traceback.format_exc() )

    return entry.short_url , status

  def set_tags_for_short_url( self, s_url, tag_list ):
    """
    Tries to replace... otherwise, inserts
    """
    self.log.info("DAO::set_tags_for_short_url start")
    
    result_url = None
    
    status = StatusCodes.FAILED
    
    try:
    
      self.log.debug("db " + str( dir( db ) ) )

      # delete existing tags for the short_url      
      url_tag_list = db.GqlQuery("SELECT * FROM URLTag WHERE short_url = :1  ", s_url  )

      if url_tag_list.count() > 0:
        db.delete( url_tag_list )
        
     
      s = set()
      for t in tag_list:
        t = t.strip()
        t = t.lower()
        
        s.add( t )
        
      for t in s:
        tag = URLTag( short_url = s_url, tag = t  )
        db.put( tag )
        
      status = StatusCodes.SUCCESSFUL
        
    except:
      self.log.error("DAO::set_tags_for_short_url ex " + traceback.format_exc() )

    return status

  def get_tags_for_short_url( self, s_url ):
    """
    Gets tags for short url.
    """
    self.log.info("DAO::get_tags_for_short_url start")
    
    result_url = None
    
    status = StatusCodes.FAILED
    
    tag_list = []
    
    try:
    
      self.log.debug("db " + str( dir( db ) ) )

      # delete existing tags for the short_url      
      url_tag_list = db.GqlQuery("SELECT * FROM URLTag WHERE short_url = :1  ", s_url  )
      if url_tag_list.count() > 0:
      
        res = url_tag_list.fetch( 1000 )
        
        for i in res:
          tag_list.append( i.tag )
          
        
      status = StatusCodes.SUCCESSFUL
        
    except:
      self.log.error("DAO::set_tags_for_short_url ex " + traceback.format_exc() )

    return tag_list, status
    
      
    
  def generate_short_url( self, entry):
    """
    Generate short URL.
    """
    
    self.log.info("DAO::generate_short_url start")
    
    res = ""
    
    try:
    
      
      
      if entry != None and entry.short_url != None:
        res = self.config['LinkMeNow']['ShortLinkBase'] + entry.short_url
        
        #"http://linkmenow/r/"+entry.short_url
      else:
        res = "unable to create short URL"
    except:
      self.log.error("DAO::generate_short_url ex " + traceback.format_exc() )
          
    return res
    
    
  def get_next_number( self ):

    val = None
    
    try:

      command = "insert into counter (val) values( null )"
      #self.counterCur.execute( command )
      #self.counterCon.commit()
      
      command = "select last_insert_rowid()"
      #self.counterCur.execute( command )
      #res = self.counterCur.fetchone()
      
    except:
      self.log.error("DAO::getNextNumber ex " + traceback.format_exc() )
      
    return val


