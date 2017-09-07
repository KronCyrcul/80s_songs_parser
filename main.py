from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import re

def search_exact_song(pattern,d):
    #find artist in dictionary
    sought_artist = d[pattern[0]]
    #find url for a song
    for i in range(len(sought_artist)):
        if re.search(r'%s' %pattern[1],sought_artist[i][0]) is not None:
            song_page = main_site+sought_artist[i][1]
    song_request = requests.get(song_page)
    song_soup = BeautifulSoup(song_request.text,"html5lib")
    song_sought = song_soup.find("div",{"class":"lcontent"})
    print(song_sought.get_text())
    main(d)

def search_similar_songs(pattern,d):
    #split pattern in two parts: for an artist and a song
    pattern_split = pattern.split(" ")
    list_similar = defaultdict(list)
    i=0
    #search through dictionary
    for artist in d.keys():
        for word in pattern_split:
            for n in range(len(d[artist])):
                #if key or value(artist or song) in dictionary match pattern
                if re.search(r'%s' %word,artist) is not None or re.search(r'%s' %word,d[artist][n][0]) is not None:
                    list_similar[i]=artist+" - "+d[artist][n][0]
                    print("[%s]: %s - %s" %(i+1,artist,d[artist][n][0]))
                    i+=1
    inpt = input("Write a number or a song\n")
    #if number - find exact song,else restart searching
    try:
        choosen_song = list_similar[int(inpt)-1].split(" - ")
        search_exact_song(choosen_song,d)
    except ValueError:
        search_similar_songs(inpt,d)
        
def main(dict):
    inpt = input("What song are you searching for\n")
    search_similar_songs(inpt,dict)

if __name__=="__main__":
    #get an artist and a song from main page 
    request = requests.get('http://www.lyricsondemand.com/tophits/80s.html')
    main_site = 'http://www.lyricsondemand.com/'
    soup = BeautifulSoup(request.text,'html.parser')
    div = soup.find('div',{'class':'infotxt'})
    span = div.find_all('span')
    songs=defaultdict(list)
    for n in range(0,len(span)-1,2):
        artist = span[n].findChild('a')
        title = span[n+1].findChild('a')
        songs[artist.text].append([title.text,title.get('href')[2:]])
    #run search
    main(songs)