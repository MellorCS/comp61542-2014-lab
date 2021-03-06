from comp61542 import app
from comp61542.database import (database, mock_database)
import sys
import os
from comp61542 import statistics
if len(sys.argv) == 1:
    dataset = "Mock"
    db = mock_database.MockDatabase()
else:
    data_file = sys.argv[1]
    path, dataset = os.path.split(data_file)
    print "Database: path=%s name=%s" % (path, dataset)
    db = database.Database()
    if db.read(data_file) == False:
        sys.exit(1)

app.config['DATASET'] = dataset
app.config['DATABASE'] = db

if "DEBUG" in os.environ:
    app.config['DEBUG'] = True

if "TESTING" in os.environ:
    app.config['TESTING'] = True
header, data = db.get_authors_who_appear_first()

for p in db.authors:
    print p.name
app.run(host='127.0.0.1', port=9292)

