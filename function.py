import urllib.request, urllib.parse, re,random, os, csv
from linebot.models import TextSendMessage, ImageSendMessage

learn_data = []

def calc(query):
    url = urllib.parse.quote_plus(query)
    result = urllib.request.urlopen('http://api.mathjs.org/v4/?expr='+url).read(1000)
    return TextSendMessage(text=str(result)[2:-1])

def stalk(username):
    url = 'https://www.instagram.com/'+username
    try :
        match = re.findall(r'"display_url":"(.*?)"', str(urllib.request.urlopen(url).read(100000)))
        if len(match) == 0:
            result = TextSendMessage(text = "Photo doesn't exist. Perhaps this user account private or don't have any photos yet") 
        else :
            random_img = match[random.randint(0,len(match)-1)]
            result = ImageSendMessage(original_content_url=random_img, preview_image_url=random_img)
    except:   # Ketika username yang dicari tidak ada
        result = TextSendMessage(text = "Username doesn't exist")
    return result

def learn(query, answer):
    learn_data.append([query,answer])
    opened_files = open("data.csv","w", newline = "")
    files = csv.writer(opened_files)
    for data in learn_data:
        files.writerow(data)
    opened_files.close()
    return TextSendMessage(text = "Words '{}' has learned".format(query))

def generate():
    opened_files = open("data.csv","r")
    files = csv.reader(opened_files)
    files = list(files)
    for file in files:
        learn_data.append(file)
    opened_files.close()

def helps(query):
    if query == "list":
        result = "List of all available command :\n1. calc\n2. stalk\n3. learn\nTo see further information input /helps <command>."
    elif query == "calc":
        result = "To calculate math operation by sending the query into MathJs API.\nUsage :\n/calc <operation>\nExample :\n/calc 1+1"
    elif query == "stalk":
        result = "To see random photo in someone's instagram account.\nFor information :\nIt cannot see photo from private account.\nUsage :\n/stalk <username>\nExample :\n/stalk wijaya.adrian"
    elif query == "learn":
        result = "To learn new input words from user and give back the feedback in desired output.\nUsage :\n/learn <question>|<answer>\nExample :\n/learn halo|halo juga\nWarning : Ferguso is dumb. He only remember your new words in a few hours."
    else :
        result = "Command is not available"
    return TextSendMessage(text = result)
