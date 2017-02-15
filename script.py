from bs4 import BeautifulSoup
import urllib

r = urllib.urlopen('http://www.practice.geeksforgeeks.org/user-profile.php?user=harendra%20Singh').read()
soup = BeautifulSoup(r)
tags = soup.select('#detail1 div.panel-body div div.col-sm-8 table tbody tr:nth-of-type(2) td:nth-of-type(2)')
if len(tags) != 1:
  print "Something has changed in website structure. Rank not found"
  exit(1)
  
rank = tags[0]
print 'Latest rank is', str(rank.string)

