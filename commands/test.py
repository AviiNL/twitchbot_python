from command import command

class test(command):
    def execute(self):
        self.c.privmsg(self.channel, "This is a test")