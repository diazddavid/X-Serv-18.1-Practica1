#!/usr/bin/python3

"""
webApp class
 Root for hierarchy of classes implementing web applications

 Copyright Jesus M. Gonzalez-Barahona and Gregorio Robles (2009-2015)
 jgb @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - March 2017
"""

import socket

class app:
    """Root of a hierarchy of classes implementing web applications

    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return (request.split(' ', 2)[0], request)

    def process(self, parsedRequest, method, rest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("404 Not Found", "<html><body><h1>WRONG PETITION</h1>" + parsedRequest + "</body></html>")

import form
import redirect

class webApp:

    def select(self, request):

        """Selects the application (in the app hierarchy) to run.
        Having into account the prefix of the resource obtained
        in the request, return the class in the app hierarchy to be
        invoked. If prefix is not found, return app class
        """

        resource = request.split(' ', 2)[1]
        if resource == "/":
            print("Running app for Root")
            return (self.apps['root'], "")
        resource = resource.split('/')[1]
        if resource.isdigit():
            print("Running app for DIGIT")
            return (self.apps['redirect'], resource)
        print("Running default app")
        return (self.myApp, resource)

    def __init__(self, hostname, port, apps):
        """Initialize the web application."""

        self.apps = apps
        self.myApp = app()

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        while True:
            print('Waiting for connections')
            (recvSocket, address) = mySocket.accept()
            print('HTTP request received (going to parse and process):')
            request = recvSocket.recv(2048).decode('utf-8')
            print(request)
            (theApp, rest) = self.select(request)
            (method, parsedRequest) = theApp.parse(request)
            (returnCode, htmlAnswer) = theApp.process(parsedRequest, method, rest)
            print('Answering back...')
            recvSocket.send(bytes("HTTP/1.1 " + returnCode + " \r\n\r\n"
                            + htmlAnswer + "\r\n", 'utf-8'))
            recvSocket.close()

if __name__ == "__main__":
    form = form.form()
    redirect = redirect.redirect()
    testWebApp = webApp("localhost", 1234, {'root': form,
                                            'redirect': redirect})
