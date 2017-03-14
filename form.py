import webapp
import urllib.parse
import csv

class form(webapp.app):
    "Use webapp parse"

    def tryOpen(self, filename):
        try:
            open(filename).close
        except FileNotFoundError:
            open(filename, 'a').close
        return

    def getActualDir(self):
        self.tryOpen('shortUrlDic.csv')
        i = 0
        with open('shortUrlDic.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                i = i + 1
        return i

    def findParsed(self, parsedRequest):
        self.tryOpen('shortUrlDic.csv')
        with open('shortUrlDic.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if parsedRequest == row['url']:
                    return True
        return False

    def initDic(self, parameter1, parameter2, filename):
        try:
            open(filename).close
        except FileNotFoundError:
            with open(filename, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                fieldnames = [parameter1, parameter2]
                writer.writeheaders()
                write.writerow({'shortUrl' : '', 'url': ''})
        return

    def addToDic(self, parsedRequest, actualDir):
        with open('shortUrlDic.csv', 'a') as csvfile:
            fieldnames = ['url', 'shortUrl']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if int(actualDir) == 0:
                writer.writeheader()
            writer.writerow({'url': parsedRequest, 'shortUrl': actualDir})
        with open('invUrlDic.csv', 'a') as csvfile:
            fieldnames = ['shortUrl', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if int(actualDir) == 0:
                writer.writeheader()
            writer.writerow({'shortUrl': actualDir, 'url': parsedRequest})
        return

    def getValue(self, key):
        self.tryOpen('shortUrlDic.csv')
        with open('shortUrlDic.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['url'] == key:
                    return row['shortUrl']
        return "ERROR AL OBTENER"

    def printDic(self):
        to_return = "<p> Las url ya acortadas son:</p>"
        self.tryOpen('shortUrlDic.csv')
        self.initDic('url', 'shortUrl', 'shortUrlDic.csv')
        with open('shortUrlDic.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                to_return = "<p>" + to_return + "<a href=" + row['url'] + ">" + row['url'] + "</a>"
                to_return = to_return + " ==> Acortada: <a href=http://localhost:1234/" + row['shortUrl'] + ">" + row['shortUrl'] + "</a></p>"
        return to_return

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""
        method = request.split(' ', 2)[0]
        url = request.splitlines()[-1]
        http = "http://"
        if method == "POST":
            if url.startswith("url="):
                url = url.split('=')[1]
                urllib.parse.unquote(url,'utf-8','replace')
                if (not url.startswith("http://"))  or (not url.startswith("https://")):
                    url = http + url
            else:
                url = ""
                return (method,parsedRequest)
        return (method, url)

    def process(self, parsedRequest, method, rest):
        if method == "POST":
            actualDir = str(self.getActualDir())
            if parsedRequest == "":
                return ("400 BAD REQUEST", "YOUR POST IS WRONG")
            if not self.findParsed(parsedRequest):
                self.addToDic(parsedRequest, actualDir)
                return ("200 OK", "<html><body><h1>Your url is: </h1>" + parsedRequest
                              + "==> Your new url: <a href= localhost:1234/" + actualDir + ">" + actualDir + "</a></body></html>")
            else:
                return ("200 OK", "<html><body><h1>Your url is: </h1>" + parsedRequest
                              + "==> Your new url: <a href= localhost:1234/" + self.getValue(parsedRequest) + ">" + self.getValue(parsedRequest) + "</a></body></html>")

        if method == "GET":
            return ("200 OK", "<html><body><h1>Introduzca URL a acortar: </h1>"
                    + "<form action='/'' method='post'>"
                    + "URL:<br> <input type='text' name = 'url' value='google.es'><br>"
                    + "<input type='submit' value='Submit'>"
                    + "</form></body>" + self.printDic() + "</html>")
