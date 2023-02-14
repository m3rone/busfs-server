import uuid

def randomFour():
    return str(uuid.uuid4())[:4]

def randomEight():
    return str(uuid.uuid4())[:8]