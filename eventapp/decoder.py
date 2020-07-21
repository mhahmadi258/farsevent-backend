def decode_ticket(encoded_string):
    ticketList = []
    splitStr = encoded_string.split("|")
    for stringVal in splitStr:
        splitObject = stringVal.split("&")
        tickInfo = {}
        tickInfo['title'] = splitObject[0]
        tickInfo['description'] = splitObject[1]
        tickInfo['capacity'] = splitObject[2]
        tickInfo['price'] = splitObject[3]
        ticketList.append(tickInfo)

    return ticketList

