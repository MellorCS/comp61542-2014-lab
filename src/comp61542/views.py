from comp61542 import app
from database import database
from flask import (render_template, request)

def format_data(data):
    fmt = "%.2f"
    result = []
    for item in data:
        if type(item) is list:
            result.append(", ".join([ (fmt % i).rstrip('0').rstrip('.') for i in item ]))
        else:
            result.append((fmt % item).rstrip('0').rstrip('.'))
    return result

@app.route("/averages")
def showAverages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"averages"}
    args['title'] = "Averaged Data"
    tables = []
    headers = ["Average", "Conference Paper", "Journal", "Book", "Book Chapter", "All Publications"]
    averages = [ database.Stat.MEAN, database.Stat.MEDIAN, database.Stat.MODE ]
    tables.append({
        "id":1,
        "title":"Average Authors per Publication",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_per_publication(i)[1])
                for i in averages ] })
    tables.append({
        "id":2,
        "title":"Average Publications per Author",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_per_author(i)[1])
                for i in averages ] })
    tables.append({
        "id":3,
        "title":"Average Publications in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_in_a_year(i)[1])
                for i in averages ] })
    tables.append({
        "id":4,
        "title":"Average Authors in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_in_a_year(i)[1])
                for i in averages ] })

    args['tables'] = tables
    return render_template("averages.html", args=args)

@app.route("/coauthors")
def showCoAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset":dataset, "id":"coauthors"}
    args["title"] = "Co-Authors"

    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_coauthor_data(start_year, end_year, pub_type)
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]
    return render_template("coauthors.html", args=args)

@app.route("/first_last_sole")
def show_first_last_sole_pub_type():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset":dataset, "id":"first_last_sole"}
    args["title"] = "First, Last and sole authors"
    pub_type=0
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_first_last_sole(pub_type)
    args["pub_str"] = PUB_TYPES[pub_type]
    args["pub_type"] = pub_type

    return render_template("first_last_sole.html", args=args)

@app.route("/")
def showStatisticsMenu():
    dataset = app.config['DATASET']
    args = {"dataset":dataset}
    return render_template('statistics.html', args=args)

@app.route("/statisticsdetails/<status>")
def showPublicationSummary(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":status}

    if (status == "publication_summary"):
        args["title"] = "Publication Summary"
        args["data"] = db.get_publication_summary()

    if (status == "publication_author"):
        args["title"] = "Author Publication"
        args["data"] = db.get_publications_and_first_last()
        #args["data"] = db.get_publications_by_author()

    if (status == "publication_year"):
        args["title"] = "Publication by Year"
        args["data"] = db.get_publications_by_year()

    if (status == "author_year"):
        args["title"] = "Author by Year"
        args["data"] = db.get_author_totals_by_year()
    if (status == "first_author"):
        args["title"] = "Authors that appear first by publication type"
        args["data"] = db.get_authors_who_appear_first()
    if (status == "last_author"):
        args["title"] = "Authors that appear last by publication type"
        args["data"] = db.get_authors_who_appear_last()
    return render_template('statistics_details.html', args=args)

@app.route("/search")
def showSearch():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset}
    args['title'] = "Author's Statistics"
    tables = []
    percentage=[]
    temp1=[]
    temp2=[]
    temp3=[]
    author_name=""

    if("author_name" in request.args):
        author_name=request.args.get("author_name")

    data=db.get_results_of_search_author(author_name)

    if (isinstance(data, basestring)):
        return showAuthorStatistics(data)
    elif(len(data)>1):

        if(author_name!=""):
            import difflib
            for item in data:
             percentage.append(difflib.SequenceMatcher(None,item,author_name).ratio())

            #sortList=[x for (y,x) in sorted(zip(percentage,data))]

            #sortList=[x for (y,x) in sorted(zip(percentage,data))]
            sortList = zip(percentage, data)
            sortList.sort()

            for i in range(len(sortList)):
                flag=0
                str=sortList[i][1].lower().split()
                count=0
                for item in str:
                    count=count+1
                    if(item.startswith(author_name.lower())):
                         flag=flag+count
                if (flag==0):
                    temp3.append(sortList[i][1])
                elif(flag==1):
                    temp1.append(sortList[i][1])
                else:
                    temp2.append(sortList[i][1])

            print data
            print temp1.reverse()
            print temp2.reverse()

            temp=[]
            for i in temp1:
                temp.append(i)
            for i in temp2:
                temp.append(i)
            for i in temp3:
                temp.append(i)

            tables.append({
            "id":1,
            "title": "Data",
            "header":"Author",
            "rows": temp })

        else:
            data.sort()
            tables.append({
            "id":1,
            "title": "Data",
            "header":"Author",
            "rows": data })

        args['tables'] = tables
        return render_template("search.html", args=args)
    else:
        tables.append({
            "id":1,
            "title": "No author found",
            "header":"Author",
            "rows": data })

        args['tables'] = tables
        return render_template("search.html", args=args)



@app.route("/authorStatistics/<authorname>")
def showAuthorStatistics(authorname):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"authorname"}
    args['title'] = "Statistics of " + authorname
    tables = []
    headers=['Conference Paper', 'Journal', 'Book', 'Book Chapter', 'Overall']

    data=db.get_author_statistics(authorname)

    table1=data.get("publications")
    table2=data.get("appear_first")
    table3=data.get("appear_last")
    table4=data.get("appear_solo")
    table5=[data.get("coauthor")]

    tables.append({
        "id":1,
        "title":"Number	of publications",
        "header":headers,
        "rows": table1[1:len(table1)]})
    tables.append({
        "id":2,
        "title":"Number	of times first author",
        "header":headers,
        "rows":table2[1:len(table2)]})
    tables.append({
        "id":3,
        "title":"Number	of times last author",
        "header":headers,
        "rows": table3[1:len(table3)]})
    tables.append({
        "id":4,
        "title":"Number	of times sole author",
        "header":headers,
        "rows": table4[1:len(table4)]})
    tables.append({
        "id":5,
        "title":"Number of co-authors",
        "header":" ",
        "rows": table5})

    args['tables'] = tables
    return render_template("author_statistics.html", args=args)
