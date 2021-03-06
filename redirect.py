import webapp
import csv

class redirect(webapp.app):
    """
    Use parse of webapp.app
    """
    
    def initDic(self):
         try:
            open('invUrlDic.csv').close
        except FileNotFoundError:
            with open('invUrlDic.csv', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                fieldnames = ['shortUrl', 'url']
                writer.writeheaders()
                write.writerow({'url' : '', 'shortUrl': ''})
        return

    def tryOpen(self, filename):
        try:
            open(filename).close
        except FileNotFoundError:
            open(filename, 'a').close
        return

    def getValue(self, key):
        self.tryOpen('invUrlDic.csv')
        with open('invUrlDic.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if key == row['shortUrl']:
                    return row['url']
        return "Null"

    def process(self, parsedRequest, method, rest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """
        
        self.initDic()    #Por si acaso nada mas iniciar el servidor nos piden una redireccion
        if method == 'GET':
            if self.getValue(rest) == "Null":
                return("404 NOT FOUND", "YOUR SHORT URL: /" + rest + " IS WRONG")
            return("303 See Other", "<html><head><meta http-equiv='refresh' content='0; URL=" + self.getValue(rest) + "' /></head></html>")
        else:
            return("400 BAD REQUEST", "YOU HAVE DONE A BAD REQUEST")
