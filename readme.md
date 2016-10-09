# Gmail to Logitech Media Server bridge

## Dependencies
https://github.com/charlierguo/gmail
https://github.com/jinglemansweep/PyLMS

## Usage
`python start.py -u username@gmail.com -s squeezeserver.hostname -p squeezeplayername`

optional refresh time (-r, --refresh), defaults to 60 seconds

## Details
Uses gmail python library to poll for new messages.

If a message body includes a supported link to a supported service, that link will be added to the current playlist using PyLMS. The message will be marked as Read so that it is only queued once.

Don't forget to install corresponding LMS plugins for each protocol!

## Supported services
- Bandcamp
- Soundcloud
- Spotify
- YouTube
