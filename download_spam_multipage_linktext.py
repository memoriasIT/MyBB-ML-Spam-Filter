# Includes
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen
from collections import OrderedDict
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

def PrintData(resulttolist,pages):

    #Print Data to terminal beautiful
    resultdict = {}
    resultdict = dict(itertools.zip_longest(*[iter(resulttolist)] * 2, fillvalue=""))

    resultdict = OrderedDict(sorted((int(key), value) for key, value in resultdict.items()))
 
    


    print("""
    _  _ ____ _ _ _      ___  ____ ___ ____ 
    |\ | |___ | | |      |  \ |__|  |  |__| 
    | \| |___ |_|_|      |__/ |  |  |  |  |    
    %d NEW ITEMS FROM %s PAGES ADDED
    """ % (len(resulttolist)/2, pages))

    # Data to CSV
    cdir = os.path.join(os.getcwd(), os.path.dirname(__file__))+"/data.csv"
    with open(cdir, 'w') as outfile: 
        w = csv.writer(outfile, delimiter='\n')        
        w.writerows([resultdict])

    ans= input("\tDONE! Want to preview data saved? (y/n)")
    if (ans == "y"):
        pp.pprint(resultdict)
    else:
        print("Cy@!")


def main():
    # Introduce parametres to scrape
    urlroot ="https://greysec.net/forumdisplay.php?fid="
    urlid = "11"
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
        1. D/L new data
        2. Parse data in CSV
        3. D/L and Parse
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
            print("\n\tYou let chippy do all the work, huh?") 

            # Open CSV

            # Data from CSV to parse

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