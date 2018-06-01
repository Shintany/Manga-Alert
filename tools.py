import csv

# This class purpose is to put into an array the list of manga from the .csv file
class Database():
    def __init__(self, filePath):
        self.database = {}
        self.databasePath = filePath

        self.fillDatabase()
    
    def fillDatabase(self):
        with open(self.databasePath, mode = 'r') as infile:
            dbReader = csv.reader(infile)
            self.database = {row[0]:row[1] for row in dbReader}
    
    def displayDatabase(self):
        for keys in self.database:
            print(keys, ' : ', self.database.get(keys))
