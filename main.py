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
from Handlers.CreateUserHandler import CreateUserHandler

from django import http

import os
import re

from google.appengine.ext import webapp

def main():

  host_name = os.environ['HTTP_HOST']
  
  log = getLogger()
  
  log.debug("hostname is " + str( host_name ) )
  
  application = webapp.WSGIApplication( [ ('/', MainHandler),
                                          ('/1/createuser(.*)', CreateUserHandler)
                                           ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
