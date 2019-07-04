import regex
test = """
{
	__testToo : {
		__schema: {
			Name : String,
			Age : Number
		},
		__options: {
			collection: "testToo"
		}
	},
	__children: {
		Owner : {
            __schema{
			    Job : String
            }
		},
		Janitor : {
            __schema{
			    Family_count : Number
            }
		}
	}
}
"""

def get_keys(json_data, start=0):
    key = regex.search("[^\[\]{}\s:\"]+", json_data[start:])
    if not key: return
    data, index = get_object(json_data, key.group(0))
    print( data)
    
    if start < len(json_data):
        get_keys(json_data, index)

def get_object(json_data, *keydata):
    index = 0
    for val in keydata:
        index = json_data.find(val, index)
    index = json_data.find("{", index)
    return __bracket_parse(json_data, index)
    
def __bracket_parse(strg, start):
    out = ""
    bracket = 0
    i = 0
    for i in range(start, len(strg)):
        if strg[i] == "{":
            bracket+=1
        elif strg[i] == "}":
            bracket-=1
        elif bracket<=0:
            break
        out+=strg[i]

    return out, i

# print(get_object(test, "json")[0])
get_keys(get_object(test, "json")[0])

