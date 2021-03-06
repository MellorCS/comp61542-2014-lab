from comp61542.statistics import average
import itertools
import numpy as np
from xml.sax import handler, make_parser, SAXException
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]

class Publication:
    CONFERENCE_PAPER = 0
    JOURNAL = 1
    BOOK = 2
    BOOK_CHAPTER = 3

    def __init__(self, pub_type, title, year, authors):
        self.pub_type = pub_type
        self.title = title
        if year:
            self.year = int(year)
        else:
            self.year = -1
        self.authors = authors

class Author:
    def __init__(self, name):
        self.name = name

class Stat:
    STR = ["Mean", "Median", "Mode"]
    FUNC = [average.mean, average.median, average.mode]
    MEAN = 0
    MEDIAN = 1
    MODE = 2

class Database:
    def read(self, filename):
        self.publications = []
        self.authors = []
        self.author_idx = {}
        self.min_year = None
        self.max_year = None

        handler = DocumentHandler(self)
        parser = make_parser()
        parser.setContentHandler(handler)
        infile = open(filename, "r")
        valid = True
        try:
            parser.parse(infile)
        except SAXException as e:
            valid = False
            print "Error reading file (" + e.getMessage() + ")"
        infile.close()

        for p in self.publications:
            if self.min_year == None or p.year < self.min_year:
                self.min_year = p.year
            if self.max_year == None or p.year > self.max_year:
                self.max_year = p.year

        return valid

    def get_all_authors(self):
        return self.author_idx.keys()

    def get_results_of_search_name_author(self, author_name):

        authors=[]
        for key in self.author_idx.keys():
            if author_name.lower() in key.lower():
                authors.append(key)

        if len(authors)==0:
            return []


        if len(authors)==1:
            return authors[0]

        return(authors)

    def get_results_of_search_author(self,author_name,data):

        listResults=[]
        startsWithSurname=[]
        startsWithName=[]
        startsNever=[]

        import difflib
        for item in data:
            fullName=item.split()
            lastName=fullName[0].lower()
            firstName=fullName[1].lower()

            percentageLast=difflib.SequenceMatcher(None,author_name.lower(),lastName).ratio()
            percentageFirst=difflib.SequenceMatcher(None,author_name.lower(),firstName).ratio()

            if (lastName.startswith(author_name.lower())):
                startsWithSurname.append([item,percentageLast,percentageFirst])
            elif (firstName.startswith(author_name.lower())):
                startsWithName.append([item,percentageLast,percentageFirst])
            else:
                startsNever.append([item,percentageLast,percentageFirst])

        startsWithSurname.sort(key=lambda x: (-x[1], x[0]), reverse=False)
        startsWithName.sort(key=lambda x: (-x[2], x[0]), reverse=False)
        startsNever.sort(key=lambda x: (-x[1], x[0]), reverse=False)

        for i in startsWithSurname:
            listResults.append(i[0])
        for i in startsWithName:
            listResults.append(i[0])
        for i in startsNever:
            listResults.append(i[0])

        return (listResults)

    def get_first_last_sole(self,pub_type):
        header = ("Author","First Author","Last Author","Sole Author")
        astats = [[0,0,0] for _ in range(len(self.authors))]

        for p in self.publications:
            if(p.pub_type==pub_type or pub_type==4):
                #count sole authors and add them to the array
                if(len(p.authors)==1):
                    astats[p.authors[0]][2]+=1
                else:
                    astats[p.authors[0]][0]+=1
                    astats[p.authors[-1]][1]+=1

        data = [[self.authors[i].name] + astats[i]
            for i in range(len(astats)) ]
        return (header,data)

    def get_coauthor_data(self, start_year, end_year, pub_type):
        coauthors = {}
        for p in self.publications:
            if ((start_year == None or p.year >= start_year) and
                (end_year == None or p.year <= end_year) and
                (pub_type == 4 or pub_type == p.pub_type)):
                for a in p.authors:
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])
        def display(db, coauthors, author_id):
            return "%s (%d)" % (db.authors[author_id].name, len(coauthors[author_id]))

        header = ("Author", "Co-Authors")
        data = []
        for a in coauthors:
            data.append([ display(self, coauthors, a),
                ", ".join([
                    display(self, coauthors, ca) for ca in coauthors[a] ]) ])

        return (header, data)

    def get_average_authors_per_publication(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ func(auth_per_pub[i]) for i in np.arange(4) ] + [ func(list(itertools.chain(*auth_per_pub))) ]
        return (header, data)

    def get_average_publications_per_author(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))

        for p in self.publications:
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(pub_per_auth[:, i]) for i in np.arange(4) ] + [ func(pub_per_auth.sum(axis=1)) ]
        return (header, data)

    def get_average_publications_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        ystats = np.zeros((int(self.max_year) - int(self.min_year) + 1, 4))

        for p in self.publications:
            ystats[p.year - self.min_year][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(4) ] + [ func(ystats.sum(axis=1)) ]
        return (header, data)

    def get_average_authors_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        yauth = [ [set(), set(), set(), set(), set()] for _ in range(int(self.min_year), int(self.max_year) + 1) ]

        for p in self.publications:
            for a in p.authors:
                yauth[p.year - self.min_year][p.pub_type].add(a)
                yauth[p.year - self.min_year][4].add(a)

        ystats = np.array([ [ len(S) for S in y ] for y in yauth ])

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(5) ]
        return (header, data)

    def get_publication_summary_average(self, av):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))
        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        name = Stat.STR[av]
        func = Stat.FUNC[av]

        data = [
            [name + " authors per publication"]
                + [ func(auth_per_pub[i]) for i in np.arange(4) ]
                + [ func(list(itertools.chain(*auth_per_pub))) ],
            [name + " publications per author"]
                + [ func(pub_per_auth[:, i]) for i in np.arange(4) ]
                + [ func(pub_per_auth.sum(axis=1)) ] ]
        return (header, data)

    def get_publication_summary(self):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "Total")

        plist = [0, 0, 0, 0]
        alist = [set(), set(), set(), set()]

        for p in self.publications:
            plist[p.pub_type] += 1
            for a in p.authors:
                alist[p.pub_type].add(a)
        # create union of all authors
        ua = alist[0] | alist[1] | alist[2] | alist[3]

        data = [
            ["Number of publications"] + plist + [sum(plist)],
            ["Number of authors"] + [ len(a) for a in alist ] + [len(ua)] ]
        return (header, data)

    def get_average_authors_per_publication_by_author(self, av):
        header = ("Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "All publications")

        astats = [ [[], [], [], []] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [self.authors[i].name]
            + [ func(L) for L in astats[i] ]
            + [ func(list(itertools.chain(*astats[i]))) ]
            for i in range(len(astats)) ]
        return (header, data)

    def get_publications_by_author(self):
        header = ("Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapters", "Total")

        astats = [ [0, 0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type] += 1

        data = [ [self.authors[i].name] + astats[i] + [sum(astats[i])]
            for i in range(len(astats)) ]
        return (header, data)

    def get_publications_and_first_last(self):
        header = ("Author","Number of conference papers",
                  "Number of journals","Number of books","Number of book chapters","First","Last",
                  "Co-authors","Total")
        #count publications
        astats = [[0,0,0,0,0,0,0] for _ in range(len(self.authors))]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type]+=1
        #count first and last publications
        for p in self.publications:
            astats[p.authors[0]][4] +=1
            astats[p.authors[-1]][5] +=1

        #count co-authors
        coauthors = {}
        for p in self.publications:
            for a in p.authors:
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])
        astats[a][6] = len(coauthors[a])



        data = [ [self.authors[i].name] + astats[i] + [0]
            for i in range(len(astats)) ]
        #sum up the total publications
        for d in data:
            d[-1] = sum(d[1:5])

        return (header,data)

    def get_authors_who_appear_first(self):
        header = ("Author","Conference Paper","Journal","Book","Book Chapter","Overall")
        astats = [[0,0,0,0] for _ in range(len(self.authors))]


        for p in self.publications:
            if(len(p.authors)!=1):
                astats[p.authors[0]][p.pub_type] +=1

        data = [[self.authors[i].name] + astats[i] + [sum(astats[i])]
            for i in range(len(astats)) ]

        return (header,data)

    def get_authors_who_appear_last(self):
        header = ("Author","Conference Paper","Journal","Book","Book Chapter","Overall")
        astats = [[0,0,0,0] for _ in range(len(self.authors))]

        for p in self.publications:
            if(len(p.authors)!=1):
                astats[p.authors[len(p.authors)-1]][p.pub_type] +=1

        data = [[self.authors[i].name] + astats[i] + [sum(astats[i])]
            for i in range(len(astats)) ]
        return (header,data)

    def get_average_authors_per_publication_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type].append(len(p.authors))
            except KeyError:
                ystats[p.year] = [[], [], [], []]
                ystats[p.year][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(L) for L in ystats[y] ]
            + [ func(list(itertools.chain(*ystats[y]))) ]
            for y in ystats ]
        return (header, data)

    def get_publications_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type] += 1
            except KeyError:
                ystats[p.year] = [0, 0, 0, 0]
                ystats[p.year][p.pub_type] += 1

        data = [ [y] + ystats[y] + [sum(ystats[y])] for y in ystats ]
        return (header, data)

    def get_average_publications_per_author_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year]
            except KeyError:
                s = np.zeros((len(self.authors), 4))
                ystats[p.year] = s
            for a in p.authors:
                s[a][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(ystats[y][:, i]) for i in np.arange(4) ]
            + [ func(ystats[y].sum(axis=1)) ]
            for y in ystats ]
        return (header, data)

    def get_author_totals_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year][p.pub_type]
            except KeyError:
                ystats[p.year] = [set(), set(), set(), set()]
                s = ystats[p.year][p.pub_type]
            for a in p.authors:
                s.add(a)
        data = [ [y] + [len(s) for s in ystats[y]] + [len(ystats[y][0] | ystats[y][1] | ystats[y][2] | ystats[y][3])]
            for y in ystats ]
        return (header, data)

    def add_publication(self, pub_type, title, year, authors):
        if year == None or len(authors) == 0:
            print "Warning: excluding publication due to missing information"
            print "    Publication type:", PublicationType[pub_type]
            print "    Title:", title
            print "    Year:", year
            print "    Authors:", ",".join(authors)
            return
        if title == None:
            print "Warning: adding publication with missing title [ %s %s (%s) ]" % (PublicationType[pub_type], year, ",".join(authors))
        idlist = []
        for a in authors:
            try:
                idlist.append(self.author_idx[a])
            except KeyError:
                a_id = len(self.authors)
                self.author_idx[a] = a_id
                idlist.append(a_id)
                self.authors.append(Author(a))
        self.publications.append(
            Publication(pub_type, title, year, idlist))
        if (len(self.publications) % 100000) == 0:
            print "Adding publication number %d (number of authors is %d)" % (len(self.publications), len(self.authors))

        if self.min_year == None or year < self.min_year:
            self.min_year = year
        if self.max_year == None or year > self.max_year:
            self.max_year = year

    def _get_collaborations(self, author_id, include_self):
        data = {}
        for p in self.publications:
            if author_id in p.authors:
                for a in p.authors:
                    try:
                        data[a] += 1
                    except KeyError:
                        data[a] = 1
        if not include_self:
            del data[author_id]
        return data

    def get_coauthor_details(self, name):
        author_id = self.author_idx[name]
        data = self._get_collaborations(author_id, True)
        return [ (self.authors[key].name, data[key])
            for key in data ]

    def get_network_data(self):
        na = len(self.authors)

        nodes = [ [self.authors[i].name, -1] for i in range(na) ]
        links = set()
        for a in range(na):
            collab = self._get_collaborations(a, False)
            nodes[a][1] = len(collab)
            for a2 in collab:
                if a < a2:
                    links.add((a, a2))
        return (nodes, links)

    def get_author_statistics(self,author_name):
        author_dict = {}
        #author_stats = ()
        publications = self.get_publications_by_author()
        for ap in publications.__getitem__(1):
            if author_name == ap[0]:
                author_dict["publications"] = ap

        appear_first = self.get_authors_who_appear_first()
        for af in appear_first.__getitem__(1):
            if author_name == af[0]:
                author_dict["appear_first"] = af

        appear_last = self.get_authors_who_appear_last()
        for al in appear_last.__getitem__(1):
            if author_name == al[0]:
                author_dict["appear_last"] = al

        appear_solo = self.get_authors_who_appear_sole()
        for solo in appear_solo.__getitem__(1):
            if author_name == solo[0]:
                author_dict["appear_solo"] = solo

        coauthor = self.get_publications_and_first_last()
        for c in coauthor.__getitem__(1):
            if author_name == c[0]:
                author_dict["coauthor"] = c[7]
        return author_dict

    def coauthorsFigure(self,author_name):

        author_id = self.author_idx[author_name]
        data = self._get_collaborations(author_id,False)
        vertices = [author_name]
        for item in data:
            vertices.append(self.authors[item].name)
        print len(vertices)-1
        coAuthorGraph = nx.Graph()
        coAuthorGraph.add_star(vertices)
        pos = nx.spring_layout(coAuthorGraph)
        nx.draw(coAuthorGraph,pos)

        plt.savefig('figure.png')
        plt.close()
        plt.show()


        return len(vertices)-1

    def get_authors_who_appear_sole(self):
        header = ("Author","Conference Paper","Journal","Book","Book Chapter","Overall")
        astats = [[0,0,0,0] for _ in range(len(self.authors))]

        for p in self.publications:
            if(len(p.authors)==1):
                    astats[p.authors[0]][p.pub_type] +=1

        data = [[self.authors[i].name] + astats[i] + [sum(astats[i])]
            for i in range(len(astats)) ]
        return (header,data)

    def detect_whether_the_author_exists(self,author_name):
        a=0
        for i in range(len(self.authors)):
            if self.authors[i].name==author_name:
                a=1
        return a

    def get_degree_of_separation_between_two_authors(self, author1, author2):
        auth1Idx = 0
        auth2Idx = 0
        dos = None
        G = nx.Graph()

        try:
            authName_totalCollab, authIdx_authConn = self.get_network_data()
            auth1Idx = self.author_idx.__getitem__(author1)
            auth2Idx = self.author_idx.__getitem__(author2)
            G.add_edges_from(authIdx_authConn)
            try:
                dos = nx.shortest_path_length(G, auth1Idx, auth2Idx) - 1
            except:
                dos = "X"
        except TypeError:
            print TypeError.message



        return dos


class DocumentHandler(handler.ContentHandler):
    TITLE_TAGS = [ "sub", "sup", "i", "tt", "ref" ]
    PUB_TYPE = {
        "inproceedings":Publication.CONFERENCE_PAPER,
        "article":Publication.JOURNAL,
        "book":Publication.BOOK,
        "incollection":Publication.BOOK_CHAPTER }

    def __init__(self, db):
        self.tag = None
        self.chrs = ""
        self.clearData()
        self.db = db

    def clearData(self):
        self.pub_type = None
        self.authors = []
        self.year = None
        self.title = None

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        if name in self.TITLE_TAGS:
            return
        if name in DocumentHandler.PUB_TYPE.keys():
            self.pub_type = DocumentHandler.PUB_TYPE[name]
        self.tag = name
        self.chrs = ""

    def endElement(self, name):
        if self.pub_type == None:
            return
        if name in self.TITLE_TAGS:
            return
        d = self.chrs.strip()
        if self.tag == "author":

            str=d.split()
            temp=[]
            temp.append(str[-1])

            for item in str:
                if(item!=str[-1]):
                    temp.append(item)

            z=' '.join(temp)

            self.authors.append(z)
        elif self.tag == "title":
            self.title = d
        elif self.tag == "year":
            self.year = int(d)
        elif name in DocumentHandler.PUB_TYPE.keys():
            self.db.add_publication(
                self.pub_type,
                self.title,
                self.year,
                self.authors)
            self.clearData()
        self.tag = None
        self.chrs = ""

    def characters(self, chrs):
        if self.pub_type != None:
            self.chrs += chrs

