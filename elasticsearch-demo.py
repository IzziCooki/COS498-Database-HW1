# SETUP

# import elasticsearch module
from elasticsearch import Elasticsearch,helpers
# import csv and re (regular expression module) to help parse data
import csv,re

# first create a variable to represent the elasticsearch client you wish to connect to
# first arg is the elasticsearch endpoint, second arg is the api key, both can be found in the Kibana dashboard for your cluster
client = Elasticsearch("https://b99be8fe54f8461cba15e2b7ed9aec33.us-central1.gcp.cloud.es.io:443",api_key="SVh1dEQ1d0JXTl8zSzRJdTZuYXE6bldCSWRONzl6N09iTjBUbmNIMjJpQQ==")

# elasticsearch throws an error if an existing document is added to an index, so this is just here so this program can be ran multiple times while still allowing the added data to remain visible after program execution is complete
client.indices.delete(index="index-movies")


# CREATE

# elasticsearch stores documents (which are essentially objects with various named fields and values for those fields) in bins called indices
# in a sense, documents are like instances of a class and the index is the class blueprint itself

# mappings dictate the names and types of fields that documents in an index have, and follow json formatting generally
# all fields are stored in the "properties" json object, and each field is listed in the format "<field name>":{"type":"<desired elasticsearch field type>"}
# available field types are listed at https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/field-data-types

# mapping so the documents in the index we'll create conform to our dataset (movie information)
mov_map = {
    "properties": {
        "Wikipedia ID":{"type":"integer"},
        "Freebase ID":{"type":"text"},
        "Title":{"type":"text"},
        "Release date":{"type":"date"},
        "Revenue":{"type":"integer"},
        "Runtime (min)":{"type":"float"},
        "Languages":{"type":"text"},
        "Countries":{"type":"text"},
        "Genres":{"type":"text"}
    }
}
# with our mapping established, we can create an index to store our documents
client.indices.create(index="index-movies",mappings=mov_map)

# to add an individual document, use the .index() function
client.index(index="index-movies",id="/m/03/vyhn",document={
    "Wikipedia ID":975900,
    "Freebase ID":"/m/03/vyhn",
    "Title":"Ghosts of Mars",
    "Release date":"2001-08-24",
    "Revenue":14010832,
    "Runtime (min)":98,
    "Languages":"English Language",
    "Countries":"United States of America",
    "Genres":["Thriller","Science Fiction","Horror","Adventure","Supernatural","Action","Space western"]
    }
)

# to add documents en masse, provide a generator function (normal Python code using the yield keyword instead of return) that will generate all your documents to Elasticsearch's bulk add helper function, helpers.bulk(client,generator)
# below is the generator function, which extracts the first 500 rows of data from movie.metadata.tsv and yields a properly-formatted document for each row, since the bulk add seems capable of handling no more than 500 docs at once
# this could easily be modified to extract from custom rows or from a custom file
def doc_generator():
    # this is the regex pattern used to extract the actual languages/countries/genres from movie.metadata.tsv, where they are listed alongside IDs for each that we don't need
    messy_split=re.compile(r''': "[^"]*"[,}]''') # they are extracted with identifying characters still attached, which we will remove later
    # normal file reading stuff
    with open("D:/UMaine/2sophs/COS498/movie.metadata.tsv",newline='') as file:
        tsv_reader = csv.reader(file,delimiter='\t')
        tsv_reader.__next__() # skip the first row since it's already been added manually with .index()
        row_count = 1
        for row in tsv_reader:
            # first, handling of messy data and null values must be done
            # we'll start with the messy data bc it's more complicated
            languages=[]
            countries=[]
            genres=[]
            # cleaning up languages...
            for lang in messy_split.finditer(row[6]):
                lang=lang.group()
                if len(lang)<=5:
                    languages.append("")
                else:
                    languages.append(lang[3:-2])
            # and countries...
            for cnt in messy_split.finditer(row[7]):
                cnt=cnt.group()
                if len(cnt)<=5:
                    countries.append("")
                else:
                    countries.append(cnt[3:-2])
            # and, finally, genres
            for g in messy_split.finditer(row[8]):
                g=g.group()
                if len(g)<=5:
                    genres.append("")
                else:
                    genres.append(g[3:-2])
            
            # with messy data put in a readable form, next we'll make sure anything we want to cast to an int (wiki ID, revenue, etc.) has a value, if not we'll just put in -1 to symbolize that it was blank
            for i in (0,4,5):
                if row[i]=="":
                    row[i]=-1
            # a similar thing must be done with the date column as well. elasticsearch can read dates either as formatted strings or as a number representing the ms since the epoch, so 0 is an acceptable null value
            if row[3]=="":
                row[3]=0
            
            row_count+=1
            
            # at this point, row is an array containing all the elements of one row
            # all that must be done is plugging in its values in the correct format into the mapping, and then yielding the resulting document
            # note that fields like _id and _index are metadata fields specifying the document's id and index, which are necessary to include for use with the bulk helper function
            yield {
                "_id":row[1],
                "_index":"index-movies",
                "Wikipedia ID":int(row[0]),
                "Freebase ID":row[1],
                "Title":row[2],
                "Release date":row[3], # elasticsearch autoconverts from str if it's formatted right which for this dataset it alr is
                "Revenue":int(float(row[4])),
                "Runtime (min)":int(float(row[5])),
                "Languages":languages,
                "Countries":countries,
                "Genres":genres
            }

            #print(f"Created doc for row {row_count}")
            if row_count>=500:
                break

helpers.bulk(client,doc_generator())

client.indices.refresh(index="index-movies") # after performing the bulk add, refreshing the index is necessary so the python client is made aware of the new additions
# refreshing is done automatically after manual adds


# READ

# to get a specific document as a json string, simply pass its index and id into your client object's .get() function
first_doc = client.get(index="index-movies",id="/m/03/vyhn")
# the elements of the doc can then be accessed using normal python dict notation, with metadata (ex. '_id') stores normally and all actual data stored in the '_source' subdict
print(f"The title of the first movie is {first_doc['_source']['Title']}") # note that for some reason specifying the keys with double quotes doesn't work

# elasticsearch, unsurprisingly, also has very robust searching capabilities through the use of the .search() method
# this method takes the index (or indices) to be searched, an optional size argument containing a string of the max number of results to return (default="10"), and a "query" JSON object that uses Query DSL syntax (https://www.elastic.co/docs/explore-analyze/query-filter/languages/querydsl)
# this consists of independent leaf clauses, the most basic of which is "match":{"<field_name>":<desired_value>}, and these leaf clauses can be optionally joined using compound clauses
# likely the most generally useful compound clause is "bool", which consists of a JSON object containing occurrence types, which themselves are arrays of leaf clauses, with the specific occurrence type used dictating how the listed leaf clauses will be related
# "must" relates them through a logical AND, returning only docs that match all the provided leaf clauses, "should" relates them through a logical OR, and "filter" is a logical AND like "must" but doesn't calculate a relevance score and therefor operates faster
# "minimum_should_match" is an optional property of "bool" specifying how many or what percentage of clauses within "should" must be matched for the doc in question to be returned as a hit
results = client.search(index="index-movies",size="500",query={
    "bool":{
        "filter":[
            {"match":{"Countries":"America"}},
            {"match":{"Languages":"English"}}
        ],
        "should":[
            {"match":{"Genres":"Thriller"}},
            {"match":{"Genres":"Horror"}},
            {"match":{"Title":"monster"}}
        ],
        "minimum_should_match":1
        }
    }
)

# the above code searches index-movies for up to 500 results, first filtering down to only results that contain the word "America" in their "Countries" field and "English" in their "Languages" field
# from this narrowed down list, only results that contain at least one of "Thriller" or "Horror" in their "Genres" field or "monster" in their "Title" field are returned
# the results are returned in descending order of score, so items with more matches are first in the list
# for fields of type "text", the query need only be present somewhere within the field, so for example, searching for "Thriller" also returns movies that have the genre "Erotic thriller"
# the "keyword" field type can be used instead for fields where exact matching is desired

# client.search() returns a rather complicated JSON object containing both information related to how the search went and all of the individual hits
# more detailed knowledge of its structure can be gained by simply printing out the results of a small test search and seeing how the result is composed
# for general purposes, know that the number of hits is at results['hits']['total']['value'] and the array of documents that match the search criteria is at results['hits']['hits']

print(f"Found {results['hits']['total']['value']} results")
item_num=1
for result in results['hits']['hits']:
    print(f"{item_num}.\n{result['_source']['Title']}\n{result['_source']['Genres']}")
    item_num+=1


# UPDATE

# to update an existing doc, use the .update() function and specify the index and id of the document you wish to update and a JSON object of how your new object should look
# for example, the below code updates the first movie we added to remove "Horror" and "Thriller" from its list of genres
client.update(index="index-movies",id="/m/03/vyhn",doc={
    "Wikipedia ID":975900,
    "Freebase ID":"/m/03/vyhn",
    "Title":"Ghosts of Mars",
    "Release date":"2001-08-24",
    "Revenue":14010832,
    "Runtime (min)":98,
    "Languages":"English Language",
    "Countries":"United States of America",
    "Genres":["Science Fiction","Adventure","Supernatural","Action","Space western"]
    })

print(client.get(index="index-movies",id="/m/03/vyhn")['_source']['Genres'])

# DELETE

# to delete a doc, use the .delete() function and specify the index and id
client.delete(index="index-movies",id="/m/03/vyhn")

# to delete an entire index, use .indices.delete(), as is done at the top of this program so it can be ran multiple times without elasticsearch throwing an error because the documents being added already exist
client.indices.delete(index="index-movies") # to test this code this should probably be commented out bc otherwise you won't be able to see any of the data that was added