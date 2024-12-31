import uuid

def randomTen():
    # return str(uuid.uuid4())[:11].replace("-", "")
    return str(uuid.uuid4()).replace("-", "")

def randomEight():
    return str(uuid.uuid4())[:8]
