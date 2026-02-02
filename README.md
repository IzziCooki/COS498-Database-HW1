# Elastic Search 


## 1: Install dependencies 
- You will need Python 3 installed for this documentation, ideally running in a virtual environment
- Create a folder on your computer and create a Python file.  
- Run the command `pip install elasticsearch`


## 1: Create a project 

-   Go to <a href="https://cloud.elastic.co/registration" target="_blank" rel="noopener">Elastic</a>
to register for a new account if you don't have one already. Alternatively, <a href="https://cloud.elastic.co/login" target="_blank" rel="noopener">Login.</a>

-   Once registered or logged in, go to the cloud dashboard <a href="https://cloud.elastic.co/home" target="_blank" rel="noopener">here</a>.

-   Next, in the dashboard, click the button `Create serverless project`. Then select `next` on ElasticSearch
- Choose your project name and cloud provider. We used Google Cloud in this documentation. 
- Create the project and wait for the server to start up.

## 2: Create api key
- Once the database and dashboard are set up, you can create an API key by clicking `API keys` and naming it what you want. 
- The server endpoint should also be next to the API key button. Hold onto both for use in the next section.


## 2: Connect to database and create index
#### An index is a collection of documents uniquely identified by a name or an alias.

#### To connect to the database and create the index:
-  In the Python file you created, add the following code:
- - Add your own `api_key` and server endpoint information gathered from the step above.
- - You can also change the `index_name`

```     
from elasticsearch import Elasticsearch, helpers
client = Elasticsearch(
    "server_enpoint_here",          # Ex: https://328-dsa-dsad.es.us-central1.gcp.elastic.cloud:443
    api_key="your_api_key_here"     
)

# Name of index
index_name = "testing" 

client.indices.delete(index=index_name, ignore=[404])

# Create the index 
index_creation = client.indices.create(
    index=index_name,
    mappings={
        "properties": {
            "text": {"type": "text"}
        }
    }
)

print(index_creation)
```

##### Sample Output:
`{'acknowledged': True, 'shards_acknowledged': True, 'index': 'testing'}`

- Once the connection to the index is verified, this is how you can add example text to the database...

```

docs = [
    {
        "text": "Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site."
    },
    {
        "text": "Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."
    },
    {
        "text": "Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site."
    }
]
bulk_response = helpers.bulk(client, docs, index=index_name)
print(bulk_response)
```

##### Sample Output:
- Since we created 3 string documents, the function returns:

`(3, [])`

- Check your dashboard to confirm the data was added.
<a href="https://ibb.co/bMLcKjBj"><img src="https://i.ibb.co/Pv4q6shs/Screenshot-from-2026-01-28-14-00-43.png" alt="Screenshot-from-2026-01-28-14-00-43" border="0"></a>

- Success! You have created and stored string data in ElasticSearch! The next step is to search and query the data.

## 3: Searching for data
- There is no point in storing data in the database if you don't access or read the data. The following code is an example to search the index for the word `Yosemite`.

```
text_search = client.search(index=index_name, query={
    "match": {
        "text": "Yosemite"
    }
})
    
print(text_search)
```
##### Sample Output:
`{'took': 2, 'timed_out': False, '_shards': {'total': 6, 'successful': 6, 'skipped': 0, 'failed': 0}, 'hits': {'total': {'value': 1, 'relation': 'eq'}, 'max_score': 0.9530773, 'hits': [{'_index': 'testing', '_id': 'LD3IH5wBl5qpz3CbiUR3', '_score': 0.9530773, '_source': {'text': 'Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face.'}}]}}`

- The response was all the documents that match with "Yosemite". 
- It also returns the accuracy of the search query along with some other data.

       


[Source Documentation](https://www.elastic.co/docs/solutions/search/get-started/keyword-search-python)
