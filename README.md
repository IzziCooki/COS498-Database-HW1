# Elastic Search 

## 1: Create a project 

-   Go to <a href="https://cloud.elastic.co/registration" target="_blank" rel="noopener">Elastic</a>
to register for a new account if you don't have one already. Alternatively, <a href="https://cloud.elastic.co/login" target="_blank" rel="noopener">Login.</a>

-   Once registered or logged in, go to the cloud dashboard <a href="https://cloud.elastic.co/home" target="_blank" rel="noopener">here</a>.

-   Next, in the dashboard, click the button `Create serverless project`. Then select `next` on ElasticSearch
- Choose your project name and cloud provider. We used Google Cloud in this documentation. 
- Create the project and wait for the server the start up.

## 2: Create an index
#### An index is a collection of documents uniquely identified by a name or an alias. 
- Once the project is created, select it in the the dashboard.

- In the project dashboard, there is a search menu in the top right, search for `Index Management` and select the option.
- Select `Create index`, name the index what you want, and move on to the next page.
- Select the `Workflow guide`, we used keyword search.
- Follow the instructions and code given in python to connect to the database.
## 2: Connect to database and add data

#### To connect to the database and verify the connection:
```     
        from elasticsearch import Elasticsearch
        client = Elasticsearch(
            "https://yourproject.es.us-central1.gcp.elastic.cloud:443",
            api_key="your api key here"
        )
        index_name = "keyword-search" #name of index you created
        mappings = {
            "properties": {
                "text": {
                    "type": "text"
                }
            }
        }
        mapping_response = client.indices.put_mapping(index=index_name, body=mappings)
        print(mapping_response)
```

##### Sample Output:
`{'acknowledged': True}`

- Once the connection is verified, this is an example to add some sample data to the database...

```
from elasticsearch import Elasticsearch, helpers
client = Elasticsearch(
    "https://yourproject.es.us-central1.gcp.elastic.cloud:443",
    api_key="your api key here"
)
index_name = "keyword-search"
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
`(3, [])`

- Once the code has ran, check your dashboard to see if the data was added to it.
<a href="https://ibb.co/bMLcKjBj"><img src="https://i.ibb.co/Pv4q6shs/Screenshot-from-2026-01-28-14-00-43.png" alt="Screenshot-from-2026-01-28-14-00-43" border="0"></a>



       


[Source Documentation](https://www.elastic.co/docs/solutions/search/get-started/keyword-search-python)






















