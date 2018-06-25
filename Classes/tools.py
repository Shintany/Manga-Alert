# For database
import csv
import shutil
from tempfile import NamedTemporaryFile

# For mail
import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '

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

    def updateDatabase(self):
        self.database[self.header[0]] = self.header[1]
        filename = self.databasePath
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        with open(filename, 'r', encoding='utf8') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=self.header)
            writer = csv.DictWriter(tempfile, fieldnames=self.header)
            # writer.writeheader()

            for row in reader:
                print(row[self.header[0]] + " : " + row[self.header[1]])
                row[self.header[1]] = self.database.get(row[self.header[0]])
                row = {'manga_name' : row['manga_name'], 'chapter_nb' : row['chapter_nb']}
                writer.writerow(row)
            shutil.move(tempfile.name, filename)
        print("Database updated successfully!")

class Email():
    def __init__(self):
        # enter your gmail bot address and pwd here
        self.sender = "manga.alert.bot@gmail.com"
        self.gmail_password = "YourPassword"
        self.recipients = ["irchadtuankitchil@gmail.com"]

        # Create the enclosing (outer) message
        self.outer = MIMEMultipart()
        self.outer['Subject'] = 'Manga Alert - New releases!'
        self.outer['To'] = COMMASPACE.join(self.recipients)
        self.outer['From'] = self.sender
        self.outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        self.content = ""

        self.attachment = []

    def addContent(self, text_to_add):
        self.content = self.content + text_to_add

    def addAttachments(self, filename):
        self.attachment.append(filename)

    def displayAttachments(self):
        print(self.attachment)

    def displayMailContent(self):
        print(self.content)

    def deleteAttachments(self):
        for file in self.attachment:
            os.remove(file)

    def sendMail(self):

        #writing the content is the .txt file
        for file in self.attachment:
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                self.outer.attach(msg)
            except:
                print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                raise             

        composed = self.outer.as_string()

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(self.sender, self.gmail_password)
                s.sendmail(self.sender, self.recipients, composed)
                s.close()
            print("Email sent!")
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise
