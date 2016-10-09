#!/bin/python

import getpass, gmail, signal, sys, getopt


def main(argv):
  example = 'start.py -u someuser@gmail.com -s squeezeserver.host'
  username = ''
  server = ''
  try:
    opts, args = getopt.getopt(argv,'hu:s:',['help','username=','server='])
  except getopt.GetoptError:
    print example
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      print example
      sys.exit()
    elif opt in ('-u', '--username'):
      username = arg
    elif opt in ('-s', '--server'):
      server = arg
  print 'Starting Gmail 2 LMS Bridge username: ' + username + ' server: '+ server
  password = getpass.getpass()
#checkUnread(u, p)

def checkUnread(username, password):
  print('Checking mail')
  g = gmail.login(username, password)
  emails = g.inbox().mail(unread=True, prefetch=True)
  for email in emails:
    print email.subject
    g.logout()


if __name__ == '__main__':
  main(sys.argv[1:])
