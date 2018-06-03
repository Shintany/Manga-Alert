import smtplib
import csv
from tempfile import NamedTemporaryFile

# This class purpose is to put into an array the list of manga from the .csv file
class Database():
    def __init__(self, filePath):
        self.database = {}
        self.databasePath = filePath
        self.header = ["manga_name", "chapter_nb"]
        self.fillDatabase()
    
    def fillDatabase(self):
        with open(self.databasePath, mode = 'r') as infile:
            dbReader = csv.reader(infile)
            self.database = {row[0]:row[1] for row in dbReader}
        del self.database[self.header[0]]
    
    def displayDatabase(self):
        for keys in self.database:
            print(keys, ' : ', self.database.get(keys))

    def updateDatabse(self):
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        with open(self.databasePath, 'r', encoding='utf8') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=self.header)
            writer = csv.DictWriter(tempfile, fieldnames=self.header)

class Email():
    def __init__(self):
        # enter your gmail bot address and pwd here
        self.sender_email = "manga.alert.bot@gmail.com"
        self.sender_passwd = "YourPassword"

        # put your own email address here
        self.to_email = "irchadtuankitchil@gmail.com"
        # Custom the subject notification
        self.subject = "Manga Alert - New releases!"
        self.content = ""

    def addContent(self, text_to_add):
        self.content = self.content + text_to_add

    def displayMailContent(self):
        print(self.content)

    def sendMail(self):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(self.sender_email, self.sender_passwd)

        BODY = '\r\n'.join(['To: %s' % self.to_email,
                    'From: %s' % self.sender_email,
                    'Subject: %s' % self.subject,
                    '', self.content])

        try:
            server.sendmail(self.sender_email, [self.to_email], BODY)
            print("Email sent successfully!")
        except:
            print("Error sending mail!")

        server.quit()

        