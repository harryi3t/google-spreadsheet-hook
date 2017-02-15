import os
import urllib
from datetime import date

import httplib2
from apiclient import discovery
from bs4 import BeautifulSoup
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/credentials.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
SPREADSHEET_ID = '17-2Uv6e2VnDAkWo6rKNlmJwJYAQg735pPBkqQnTJXcg'
WEB_URL = 'http://www.practice.geeksforgeeks.org/user-profile.php?user=harendra%20Singh'
SELECTOR = '#detail1 div.panel-body div div.col-sm-8 table tbody tr:nth-of-type(2) td:nth-of-type(2)'


def get_credentials():
  home_dir = os.path.expanduser('~')
  credential_path = os.path.join(home_dir, '.credentials', 'credentials.json')

  if not os.path.exists(credential_path):
    print 'credentials.json file does not exists. Please create it manually'
    exit(1)
  store = Storage(credential_path)
  credentials = store.get()
  if not credentials:
    print 'Not authorized. Please set the correct credentials'
    exit(1)
  return credentials


def getRank():
  r = urllib.urlopen(WEB_URL).read()
  soup = BeautifulSoup(r, 'lxml')
  tags = soup.select(SELECTOR)
  if len(tags) != 1:
    print "Something has changed in website structure. Rank not found"
    exit(1)
  try:
      rank = int(tags[0].text)
      print 'latest rank is:',rank
      return rank
  except:
      print 'rank not an integer', tags[0]
      exit(1)


def updateRankOnSheet(service, rank):
  rangeName = 'A:B'
  result = service.spreadsheets().values().get(
      spreadsheetId=SPREADSHEET_ID, range=rangeName).execute()
  values = result.get('values', [])
  lastUpdated = str(values[len(values) - 1][0])
  lastRank = str(values[len(values) - 1][1])
  currentDate = date.strftime(date.today(), '%d %b %Y')

  if currentDate == lastUpdated and abs(int(lastRank)) == abs(rank):
    print 'Skipping updation as lastUpdated and lastRank are same', lastUpdated, abs(rank)
    exit(0)

  rowNum = len(values) + 1
  if currentDate == lastUpdated and abs(int(lastRank)) != abs(rank):
    print 'Rank changed within same date so updating'
    print abs(int(lastRank)), ' => ', abs(rank)
    rowNum = len(values)

  rangeName = 'A{}:B{}'.format(rowNum, rowNum)
  dateFormula = date.strftime(date.today(), '=DATE(%Y,%m,%d)')
  body = {"values": [[dateFormula, rank]]}

  result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=rangeName,
    body=body,
    valueInputOption='USER_ENTERED'
  ).execute()
  print result

def setupService():
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
  service = discovery.build('sheets', 'v4', http=http,
                            discoveryServiceUrl=discoveryUrl)
  return service


def main():
  service = setupService()
  rank = getRank()
  updateRankOnSheet(service, -rank)

if __name__ == '__main__':
  main()
