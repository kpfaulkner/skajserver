#!/usr/bin/env python
#
import wsgiref.handlers
import sys
import traceback
from Common.configobj import ConfigObj
import time
import logging

#from Redirector import Redirector
from Output import HTMLGenerator
import urllib
from Common.LogRoutine import *
from Handlers.MainHandler import MainHandler
from Handlers.RedirectHandler import RedirectHandler
from Handlers.StoreHandler import StoreHandler
from Handlers.PreviewHandler import PreviewHandler
from Handlers.CreatorListHandler import CreatorListHandler
from Handlers.APIHandler import APIHandler
from Handlers.StatsHandler import StatsHandler
from Handlers.TagHandler import TagHandler
from django import http

import os
import re

from google.appengine.ext import webapp

def main():

  host_name = os.environ['HTTP_HOST']
  
  log = getLogger()
  
  log.debug("hostname is " + str( host_name ) )
  
  application = webapp.WSGIApplication( [ ('/', MainHandler),
                                          ('/o/submitter(.*)', StoreHandler),
                                          ('/o/preview(.*)', PreviewHandler),   
                                          ('/(.*)', RedirectHandler) ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
