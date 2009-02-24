#!/usr/bin/python
#
# Copyright (C) 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'api.laurabeth@gmail.com (Laura Beth Lincoln)'


try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import getopt
import sys
import string


class SimpleCRUD:

  def __init__(self, email, password):
    self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'Spreadsheets GData Sample'
    self.gd_client.ProgrammaticLogin()
    self.curr_key = 'ppLr8BAF-3ST9UCUc-d7tUw' #gnome-dates
    self.curr_wksht_id = 'od6'
    self.list_feed = None    
        
  def _ListGetAction(self):
    # Get the list feed
    self.list_feed = self.gd_client.GetListFeed(self.curr_key, self.curr_wksht_id)
    self._PrintFeed(self.list_feed)
  
  def _StringToDictionary(self, row_data):
    dict = {}
    for param in row_data.split():
      temp = param.split('=')
      dict[temp[0]] = temp[1]
    return dict
  
  def _PrintFeed(self, feed):
        start_list = []
        title_list = []
        for i, entry in enumerate(feed.entry):
            if isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
                for key in entry.custom:  
                    if key == 'start':
                        start_list.append(entry.custom[key].text)
                    if key == 'title':
                        title_list.append(entry.custom[key].text)
        self.fix_dates(start_list)
        print start_list     

  def fix_dates(self, date_list):
      """ change dates from '01/03/2004' to datetime.date(2004,03,01)"""
      import datetime
      new_list = []
      for date in date_list:
          print date
          new_list.append(datetime.date(date))
      print new_list
        
  def _InvalidCommandError(self, input):
    print 'Invalid input: %s\n' % (input)
    
  def Run(self):
    self._ListGetAction()

def main():
  # parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["user=", "pw="])
  except getopt.error, msg:
    print 'python spreadsheetExample.py --user [username] --pw [password] '
    sys.exit(2)
  
  user = ''
  pw = ''
  key = ''
  # Process options
  for o, a in opts:
    if o == "--user":
      user = a
    elif o == "--pw":
      pw = a

  if user == '' or pw == '':
    print 'python query_spreadsheet.py --user [username] --pw [password] '
    sys.exit(2)
        
  sample = SimpleCRUD(user, pw)
  sample.Run()


if __name__ == '__main__':
  main()
