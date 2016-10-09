# Gmail to Logitech Media Server bridge

## Dependencies
https://github.com/charlierguo/gmail
https://github.com/jinglemansweep/PyLMS

## Usage
python start.py -u username@gmail.com -s squeezeserver.hostname

## Details
Uses gmail library to poll for new messages.
If a message body includes a supported link to Spotify, that link will be added to the current playlist using PyLMS.
The message will be marked as Read so that it is only queued once.
