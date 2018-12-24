# Includes
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen
import csv
import itertools
import os
import pprint as pp
import re

# Retrieve Website for new Threads
def RetrieveData(urllist):
    postsnames = ""
    for url in urllist:
        try:
            html = urlopen(url)
        except HTTPError as e:
            print("The server returned an HTTP error")
        except URLError as e:
            print("The server could not be found!")
        else:
            bs = BeautifulSoup(html, "html.parser")
            raw = bs.findAll('span', {'class': 'subject_new'})
            postsnames += str(raw)
            postsnames += ", "

    # Parse Threads
    postsnames = postsnames.strip()[:-1]

    regex = r"(<span class=\" subject_new\" id=\"tid_[0-9]+\"><a href=\"showthread.php\?tid=)|(</a></span>)|(\[)|(\])"
    result1 = re.sub(regex, "", postsnames , 0)
    result2 = re.sub("(\">)", ", ", result1, 0)
    resulttolist = result2.split(",")

    return resulttolist

# Parse CSV
def getCSVdata(cdir):
    with open(cdir,"r") as file:
        csvdata = file.read()
        csvdata = csvdata.split("\n")

        cleancsvdata = []
        for value in csvdata:
            try:
                cleancsvdata.append(int(value))
            except ValueError:
                # Forgive me lord because I have sinned
                pass 
    return cleancsvdata

# Print new data to CSV and screen
def PrintData(resulttolist,pages):
    # Data.csv directory
    cdir = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/data.csv"
    cleancsvdata = getCSVdata(cdir)
        
    # Parsed data to sorted list
    parseddata = resulttolist[0::2]
    for i in range(len(parseddata)):
        parseddata[i] = int(parseddata[i])
    
    resultlist = sorted(cleancsvdata + list(set(parseddata) - set(cleancsvdata)))

    # Show quantity of entities added
    print("""
    _  _ ____ _ _ _      ___  ____ ___ ____ 
    |\ | |___ | | |      |  \ |__|  |  |__| 
    | \| |___ |_|_|      |__/ |  |  |  |  |    
    %d NEW ITEMS FROM %s PAGES ADDED
    """ % (len(resultlist)-len(cleancsvdata), pages))

    # Data to CSV
    with open(cdir, 'w') as outfile: 
        w = csv.writer(outfile, delimiter='\n', lineterminator="\n")  
        for elem in resultlist:
            w.writerow([elem])

    # Preview Data if wanted
    ans= input("\tDONE! Want to preview data saved? (y/n)")
    if (ans == "y"):
        print("""
         _  _  __     ___ __       _  _ ___ _ 
        |_)|_)|_  \ /  | |_ | |   | \|_| | |_|
        |  | \|__  V  _|_|__|^|   |_/| | | | |:
        --------------------------------------
        """)
        pp.pprint(resulttolist)
    else:
        print("Cy@!")

def downloadThread(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print("The server returned an HTTP error")
    except URLError as e:
        print("The server could not be found!")
    else:
        bs = BeautifulSoup(html, "html.parser")
        raw = bs.find('div', {'class': 'post_body scaleimages'})

    regex = r"(<br>)|(\[/url])|(\<span style=\"[a-zA-Z\-\:\;\ \"]+>)|([^a-zA-Z\d\s:])"
    result = re.sub(regex, "", str(raw) , 0)
    
    return result


def main():
    # Introduce parametres to scrape
    urlroot ="https://greysec.net/"
    urlid = "forumdisplay.php?fid=11"
    pages = 2
    
    urllist = []
    for x in range(pages):
        urllist.append(urlroot+urlid+"&page="+str(x+1))


    print("""
    ::::::::  :::::::::  :::         ::::::::  ::::::::::: 
    :+:    :+: :+:    :+: :+:        :+:    :+:     :+:     
    +:+        +:+    +:+ +:+        +:+    +:+     +:+     
    +#++:++#++ +#++:++#+  +#+        +#+    +:+     +#+     
           +#+ +#+        +#+        +#+    +#+     +#+     
    #+#    #+# #+#        #+#        #+#    #+#     #+#     
    ########   ###        ##########  ########      ###   
         - Memorias de un informático 2018 - 
                memoriasit.github.io
    """)

    ans=True
    while ans:
        print ("""
        1. Check new threads
        2. Get threads from data in CSV
        3. Check and D/L threads
        """)
        ans= input("What would you like to do? ") 
        if ans=="1": 
            ans = False
            print("\n\tWait, Batman is working on it...\n")
            
            # Get data and print
            data = RetrieveData(urllist)
            PrintData(data, pages)

        elif ans=="2":
            ans = False
            print("\n\tYou let chippy do all the work, huh?\n") 

            # Data from CSV to parse
            cdir = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/data.csv"
            cleancsvdata = getCSVdata(cdir)

            # for each element in cleancsvdata download (parsed) html to file
            filedir = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/data/"
            lenght = len(cleancsvdata)
            cont = 0
            print(" STARTING PARSE TO FILES: ")
            for thread in cleancsvdata:
                url = urlroot+'showthread.php?tid='+str(thread)
                content = downloadThread(url)
                
                print("("+str(cont)+"/"+str(lenght-1)+") - Threads completed")
                cont +=1

                with open(filedir+str(thread), 'w') as file:
                    file.write(str(content))

        elif ans=="3":
            ans = False
            print("\n\tYou might want to go get a coffe while this loads...") 
            
            # D/L new data
            data = RetrieveData(urllist)
            PrintData(data, pages)

            # Parse data from urls

        elif ans !="":
            print("\n Not Valid Choice Try again")



if __name__== "__main__":
  main()