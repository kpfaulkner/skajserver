#!/usr/bin/env python
#
import wsgiref.handlers
import sys
import traceback
from Common.configobj import ConfigObj
import time
import logging

#from Redirector import Redirector
import urllib
from Common.LogRoutine import *
from Handlers.MainHandler import MainHandler
from Handlers.UserHandler import UserHandler
from Handlers.GameHandler import GameHandler
from Handlers.PlayerHandler import PlayerHandler
#from Handlers.ActionHander import ActionHandler

from django import http

import os
import re

from google.appengine.ext import webapp

def main():

  host_name = os.environ['HTTP_HOST']
  
  log = getLogger()
  
  log.debug("hostname is " + str( host_name ) )
  
  application = webapp.WSGIApplication( [ ('/', MainHandler),
                                          ('/1/createuser(.*)', UserHandler),
                                          ('/1/login(.*)', UserHandler),
                                          ('/1/getuser(.*)', UserHandler),
                                          ('/1/creategame(.*)', GameHandler),
                                          ('/1/modifygamestate(.*)', GameHandler),
                                          ('/1/joingame(.*)', GameHandler),
                                          ('/1/createplayer(.*)', PlayerHandler),
                                          ('/1/startgame(.*)', GameHandler),
                                          ('/foo(.*)', GameHandler),


                                          
                                           ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
