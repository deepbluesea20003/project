from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess, FilePasswordDB
from twisted.internet import reactor

reactor.listenTCP(21, FTPFactory(Portal(FTPRealm('./'), [AllowAnonymousAccess()])))
reactor.run()