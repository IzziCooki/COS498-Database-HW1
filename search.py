from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import BulkIndexError
client = Elasticsearch(
    "https://e39474f0d4954505a97c937a34edebc3.us-central1.gcp.cloud.es.io:443",
    api_key="OU9td0Q1d0JyeVU3RjJLc0N1UHc6WmhYWldqZW9ZUlp0M1BXUkN3Q2dPUQ==",
)

index_name = "testing"

client.indices.delete(index=index_name, ignore=[404])

client.indices.create(
    index=index_name,
    mappings={
        "properties": {
            "text": {"type": "text"}
        }
    }
)

docs = [
    {
        "_index": index_name,
        "_source": {
            "text": "Hello World"
        }
    },
    {
        "_index": index_name,
        "_source": {
            "text": "Testing for COS498"
        }
    },
    {   
        "_index": index_name,
        "_source": {
        "text": "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black."
        }
    },
    {   
        "_index": index_name,
        "_source": {
        "text": "To be... or not to be."
        }
    },
    {   
        "_index": index_name,
        "_source": {
        "text": "Pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989..."
        }
    },
    {   
        "_index": index_name,
        "_source": {
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam id placerat purus. Cras maximus consequat dui, quis varius eros scelerisque ut. Donec a erat quis metus ullamcorper scelerisque. Ut id tincidunt nisi. Suspendisse pretium tortor et nisl iaculis, a fermentum sem dapibus. Phasellus nec lacinia massa, pulvinar aliquet sapien. Aliquam non ullamcorper nisi, in maximus arcu. Pellentesque ut condimentum lectus. Duis lectus nulla, hendrerit quis risus eget, pellentesque gravida nisl. Proin tempus et mi id ultricies. Curabitur sit amet tortor sed tortor euismod dictum venenatis quis urna. Maecenas a fermentum lacus, suscipit tincidunt sem. Quisque euismod felis tincidunt, mollis sem in, congue justo. Vestibulum nunc velit, rutrum dapibus magna a, interdum tempus orci. Maecenas maximus accumsan blandit. Fusce vel tristique quam. Proin ut metus in libero iaculis rhoncus sit amet quis sapien. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nulla a laoreet risus, at interdum eros. Praesent et euismod velit, aliquam porttitor dui. Vivamus sit amet tortor quam. Curabitur tellus odio, interdum a iaculis id, venenatis sed turpis. Suspendisse potenti. Suspendisse posuere massa purus, nec luctus turpis varius nec. Nullam pharetra sapien leo, sed pretium odio efficitur ut. Maecenas eu posuere lorem. Morbi rhoncus erat sed erat pellentesque eleifend posuere in justo. Quisque sodales elementum lorem, id tempor tortor faucibus ac. Aenean in ligula id tellus aliquet facilisis. Pellentesque rhoncus velit sed tortor finibus laoreet. Aenean ultricies gravida ligula, vitae pellentesque nisi laoreet eu. Maecenas mattis elementum ante non mollis. Nulla et felis ut massa sollicitudin pharetra. Duis ac elit et est auctor porta ut ac velit. Proin tincidunt quis sapien quis pharetra. Duis ac enim nec felis volutpat bibendum. Praesent tempor vulputate purus. Sed eu libero posuere, scelerisque odio nec, gravida magna. Nullam maximus faucibus mollis. Quisque vulputate felis metus, eu dapibus massa egestas nec. Cras tristique urna rhoncus fermentum lobortis. Pellentesque pulvinar eu metus in tempor. Fusce pellentesque consequat libero sit amet efficitur. Donec sed porttitor elit, in pharetra quam. Aliquam congue arcu venenatis pretium finibus. Etiam semper turpis quis vulputate interdum. In dapibus leo id erat euismod, eget pellentesque urna tempus. Vestibulum scelerisque massa nisi, sit amet efficitur metus tristique in. Nunc vel ultricies leo. Vestibulum tincidunt, risus a vestibulum vulputate, urna est fermentum ante, vitae congue elit risus non tortor. Proin facilisis ligula non neque porta facilisis. Suspendisse lorem urna, elementum id nibh non, iaculis ultricies ex. Donec congue nec justo vitae placerat. Cras sed diam a lacus placerat cursus. Sed placerat, sapien at ullamcorper commodo, nunc nisi fermentum nunc, non finibus mi justo id ipsum. Curabitur scelerisque dolor ac ipsum pretium, nec rutrum massa facilisis. Morbi interdum blandit ultricies. Mauris vitae auctor mi. Aliquam id nulla nulla. Morbi faucibus eleifend lacus, faucibus hendrerit ipsum ultrices auctor. In tincidunt sit amet orci sit amet venenatis. Suspendisse potenti. Pellentesque convallis eros eu dui gravida, sit amet finibus massa laoreet. Cras ornare ipsum quis turpis efficitur, ut vestibulum mauris semper. Integer aliquet iaculis feugiat. Pellentesque ex purus, consequat vel interdum sit amet, maximus vel odio. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque posuere ultricies posuere. Aliquam facilisis aliquet arcu vitae fringilla. Donec nisl ex, vehicula tincidunt imperdiet eu, sodales vitae arcu. Donec fringilla quam nunc, at varius eros malesuada luctus. Nulla commodo eget lorem et cursus. Aenean condimentum, sapien nec aliquam egestas, enim libero commodo nunc, sit amet euismod ante dui lacinia nibh. Sed in lorem ut urna tempus euismod sit amet ac mi. Integer congue sem in felis porta, at luctus ligula tempor. Donec quis porta odio, in porttitor diam. Nunc ut auctor urna. Mauris nec nulla eget mi lobortis dapibus. Ut condimentum enim sed enim placerat, eu cursus dolor sodales. Curabitur sagittis maximus lorem sed vestibulum. Fusce ut justo a nulla eleifend hendrerit id facilisis felis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nullam eu mauris facilisis, rutrum purus tempor, pretium lectus. Nulla elementum nunc sed felis tempus auctor. Sed metus felis, facilisis at mollis vel, ullamcorper at lacus. Cras viverra, orci sit amet efficitur vestibulum, metus velit mattis ex, eget gravida nibh ante a sem. Proin mi erat, condimentum vel orci a, auctor consectetur leo. Phasellus laoreet nisl quis suscipit finibus. Nam vitae lacinia elit. Quisque orci metus, pretium id aliquet vitae, finibus suscipit quam. Vivamus at consectetur lectus, sed elementum ipsum. Nullam commodo vulputate mi tincidunt vehicula. Nulla lacinia, nisl eu blandit venenatis, elit magna dignissim eros, non finibus dolor felis vitae nisl. Cras dignissim mi mi, in tempor est egestas id. Morbi semper nisl ipsum. Suspendisse feugiat sollicitudin metus condimentum condimentum. Pellentesque a molestie sapien, id mollis leo. Quisque pulvinar, libero ac accumsan aliquet, felis turpis ullamcorper odio, eget aliquet magna metus eget eros. Fusce at lobortis tellus. Nam lobortis sit amet nisl vel porttitor. Etiam magna diam, feugiat vel volutpat nec, tincidunt ac ex. Maecenas ut ipsum tortor. Vivamus sed vestibulum tellus. Vestibulum dapibus gravida ultrices. Etiam et consequat nisl, a blandit sem. Vivamus sed aliquet sem. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vel elit id tortor aliquam tempor vel in urna. Vivamus tristique nunc at nunc venenatis auctor. Ut eget metus vitae mauris fringilla pharetra vitae sed mi. Phasellus convallis ante ac eros ornare, nec pharetra arcu dignissim. Morbi gravida sagittis ullamcorper. Vestibulum aliquet, metus in interdum finibus, libero mauris eleifend lectus, id pretium nibh ligula vulputate erat. Aenean elementum elit nec nibh iaculis, ac porttitor sapien mattis. Sed orci est, cursus et mauris quis, sagittis sagittis massa. Proin leo orci, efficitur nec accumsan eget, tempus in diam. Nulla ornare turpis quis diam posuere, nec fringilla turpis varius. Praesent sodales luctus semper. Proin congue dui malesuada, dignissim dui id, porttitor elit. Pellentesque eu urna non neque faucibus convallis. Nunc sem justo, consectetur nec mi accumsan, auctor tristique mi. Etiam eu tortor vitae dolor posuere placerat eu vitae orci. Cras et feugiat sem."
        }
    }
]
# Timeout to allow machine learning model loading and semantic ingestion to complete
ingestion_timeout=300
try:
    bulk_response = helpers.bulk(
        client.options(request_timeout=ingestion_timeout),
        docs,
    )
    print("Bulk response:", bulk_response)

except BulkIndexError as e:
    print("Bulk indexing failed. Detailed errors:\n")
    for err in e.errors:
        print(err)
print(bulk_response)