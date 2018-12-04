# pip install irc
# pip install lru_cache (might be optional, not sure)
# pip install functools32

import sys
import irc.bot
import requests
from commands.test import test

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel):
        self.token = token
        self.channel = '#' + channel

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print 'Connecting to ' + server + ' on port ' + str(port) + '...'
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, token)], username, username)
        
    def on_welcome(self, c, e):
        print 'Joining ' + self.channel

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):

        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print 'Received command: ' + cmd
            self.do_command(e, cmd)
        return

    def do_command(self, e, cmd):
        module = __import__("commands")
        if hasattr(module, cmd):
            class_ = getattr(module, cmd)
            rawr = getattr(class_, cmd)
            instance = rawr(self.connection, self.channel)

            instance.execute()

def main():
    username  = ""
    token     = "" # get it from - https://twitchapps.com/tmi/
    channel   = ""

    bot = TwitchBot(username, token, channel)
    bot.start()

if __name__ == "__main__":
    main()