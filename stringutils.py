import uuid
#Yeah I know it does not return four but 10
def randomFour():
    return str(uuid.uuid4())[:11].replace("-", "")

def randomEight():
    return str(uuid.uuid4())[:8]
