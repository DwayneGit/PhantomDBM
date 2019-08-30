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

def getKeys(jsonData, start=0):
    key = regex.search("[^\[\]{}\s:\"]+", jsonData[start:])
    if not key: return
    data, index = getObject(jsonData, key.group(0))
    print( data)
    
    if start < len(jsonData):
        getKeys(jsonData, index)

def getObject(jsonData, *keydata):
    index = 0
    for val in keydata:
        index = jsonData.find(val, index)
    index = jsonData.find("{", index)
    return __bracketParse(jsonData, index)
    
def __bracketParse(strg, start):
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

# print(getObject(test, "json")[0])
getKeys(getObject(test, "json")[0])

