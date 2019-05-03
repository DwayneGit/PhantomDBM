def getType(typeStr):
   
    if not isinstance(typeStr, str):
        return typeStr

    try:
        return int(typeStr)
    except:
        pass

    try:
        return float(typeStr)
    except:
        pass

    if typeStr.lower() == "true":
        return True

    elif typeStr.lower() == "false":
        return False

    elif typeStr == "":
        return None

    elif typeStr == "None":
        return None

    elif typeStr == "\\None":
        return "None"

    else: 
        return typeStr
