#!/bin/python

import getopt, getpass, gmail, re, signal, sys, time
from pylms.server import Server
from pylms.player import Player

_example = 'start.py -u someuser@gmail.com -s squeezeserver.host'
_regex = 'https://open.spotify.com/track/(\w+)'

def main(argv):
  username = ''
  server = ''
  player = ''
  try:
    opts, args = getopt.getopt(argv,'hu:s:p:',['help','username=','server=','player='])
  except getopt.GetoptError:
    print _example
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      print _example
      sys.exit()
    elif opt in ('-u', '--username'):
      username = arg
    elif opt in ('-s', '--server'):
      server = arg
    elif opt in ('-p', '--player'):
      player = arg
  print 'Starting Gmail 2 LMS Bridge username: ' + username + ' server: '+ server
  password = getpass.getpass()
  sp = getSqueezePlayer(server, player)
  while True:
    uris = findUnreadMusicURIs(username, password)
    addToPlaylist(sp, uris)
    print 'Sleeping 60 seconds'
    time.sleep(60)

def getSqueezePlayer(server, player):
  print 'Connecting to server[%s] player[%s]' % (server, player)
  sc = Server(hostname=server, port=9090)
  sc.connect()
  return sc.get_player(player)

def findUnreadMusicURIs(username, password):
  print 'Checking unread mail for music URIs'
  uris = []
  g = gmail.login(username, password)
  emails = g.inbox().mail(unread=True, prefetch=True)
  for email in emails:
    match = re.search(_regex, email.body)
    if (match != None):
      uris.append("spotify:track:" + match.group(1))
      print 'Found URI [%s] From[%s] Subject[%s]' % (match.group(0), email.fr, email.subject)
    email.read()
  g.logout()
  return uris

def addToPlaylist(sp, uris):
  print 'Adding uris to current playlist'
  if (len(uris) == 0):
    return
  for uri in uris:
    print uri
    sp.playlist_add(uri)

def signal_handler(signal, frame):
  print 'Shutting down'
  sys.exit(0)

if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal_handler)
  main(sys.argv[1:])
