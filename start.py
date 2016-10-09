#!/bin/python

import getopt, getpass, gmail, re, signal, sys, urllib2, time
from pylms.server import Server
from pylms.player import Player

_example = 'start.py -u someuser@gmail.com -s squeezeserver.host'
_refresh_seconds = 60
_services = {
    'bandcamp': ['https://\w+\.bandcamp\.com/track/[\w-]+', 'http:', '"(//\w+\.bandcamp\.com/download/track[^"]+)"'],
    'soundcloud': ['https://soundcloud\.com/\w+/[\w-]+', 'soundcloud://', 'soundcloud:tracks:(\d+)'],
    'spotify': ['https://open\.spotify\.com/track/(\w+)', 'spotify:track:'],
    'youtube': ['https://youtu\.be/(\w+)', 'youtube://www.youtube.com/v/']}
_lms_autoplay = True


def main(argv):
    username = ''
    server = ''
    player = ''
    try:
        opts, args = getopt.getopt(argv, 'hu:s:p:r:', ['help', 'username=', 'server=', 'player=', 'refresh='])
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
        elif opt in ('-r', '--refresh'):
            global _refresh_seconds
            _refresh_seconds = int(arg)
    # Main loop
    print 'Starting Gmail 2 LMS Bridge\nusername[%s] server[%s] player[%s] refresh[%ds]' % (
        username, server, player, _refresh_seconds)

    password = getpass.getpass('Gmail Password:')
    sp = get_squeeze_player(server, player)
    while True:
        print '\n%s' % time.ctime()
        uris = process_unread_emails(username, password)
        add_to_playlist(sp, uris)
        if _lms_autoplay and len(uris) > 0 and sp.get_mode() == 'stop':
            print 'Stopped player detected, advancing to next track and playing'
            sp.next()
            sp.play()
        print 'Will refresh in %s seconds' % _refresh_seconds
        time.sleep(_refresh_seconds)


def get_squeeze_player(server, player):
    print 'Connecting to server[%s] player[%s]' % (server, player)
    sc = Server(hostname=server, port=9090)
    sc.connect()
    return sc.get_player(player)


def process_unread_emails(username, password):
    print 'Checking unread mail for music URIs'
    uris = []
    g = gmail.login(username, password)
    emails = g.inbox().mail(unread=True, prefetch=True)
    for email in emails:
        uri = parse_supported_uri(email.body)
        if uri is not None:
            uris.append(uri)
            print '\nFrom[%s]\nSent at[%s]\nSubject[%s]\nURI[%s]\n' % (
                email.fr, email.sent_at, email.subject, uri)
        email.read()
    g.logout()
    return uris


def parse_supported_uri(text):
    for k, v in _services.items():
        match = re.search(v[0], text)
        if match is not None:
            if k in ('bandcamp', 'soundcloud'):
                print 'Looking up API id for [%s]' % match.group(0)
                html = urllib2.urlopen(match.group(0)).read()
                match = re.search(v[2], html)
                if match is not None:
                    return v[1] + match.group(1)
            else:
                return v[1] + match.group(1)


def add_to_playlist(sp, uris):
    if len(uris) == 0:
        return
    print 'Adding [%d] URIs to current playlist' % len(uris)
    for uri in uris:
        sp.playlist_add(uri)


def signal_handler(signal, frame):
    print 'Shutting down'
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main(sys.argv[1:])
