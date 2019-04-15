# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 18:47:13 2019

@author: caios
"""

import requests
from bs4 import BeautifulSoup
import re, os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


music_name_download = []
download_link = []
search_result = []
music_name = []
my_list = []
music_list = []
page = requests.get("http://www.deutsche-dj-playlist.de/DDP-Charts-Top100/")
print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

datalist = soup.find_all('div', class_='cover dummy')


for data in datalist:
    str(data)
    my_list.append(data)
    m = re.search('title=".*([A-Z])\w+(.*)', str(data))
    music_list.append(m)
#print(music_list)
    
for music in music_list:
    n = re.sub('(<_sre.SRE_Match object; span=).\d*..\d*., (match=.)|(title=.)|&amp;|>|\\| -|None|<|div','', str(music))
    music_name.append(n)    
   

for y in range(len(music_name)):

    url = "https://pecah.ndas.se/download-mp3/?q=" + music_name[y+1] + "&type=Search"
    payload = {'q':music_name[y+1]}
    r = requests.post(url, payload)
    #print(r.content)
    
    soup2 = BeautifulSoup(r.content, 'html.parser')
    
    try:
        searching = soup2.find('ul').find('a')

        m = re.sub('(<a href=")|("><img alt=").*','', str(searching))
        #print(searching)
        
        name = re.sub('((<a href=")|.*(<img alt=")|(" height="200px).*)','',str(searching))
        get_name = re.sub('(&amp;)','&', str(name))
            
        music_name_download.append(get_name)
           
        comparison_value = fuzz.partial_ratio(music_name[y+1],get_name)
        if(comparison_value > 30):
            print('Musica buscada: ' + music_name[y+1])
           # print(get_name)
            print('Acurácia da busca: ' + str(comparison_value) + '%')
                    
        
            url2 = "https://pecah.ndas.se" + m
            r2 = requests.post(url2)
        
            soup3 = BeautifulSoup(r2.content, 'html.parser')
            get_download_button = soup3.find('center', { 'id': 'download'})
        
            downgex = re.sub('((<center id="download"><a href=")|" (rel="nofollow").*)','',str(get_download_button))
            
            url3 = downgex
            download_link.append(url3)
           # print(r2.content)
                      
            try:
                path = "C:/Users/caios/Desktop/teste_musica/"
                os.mkdir(path, 777)     #
            except FileExistsError:
                pass
            
            for x in download_link: 
                        with open(path + str(get_name) + '.mp3', 'wb') as f:
                                download = requests.get(x)  
                                donwload_info = requests.head(x)
                               # print(donwload_info.headers)
                                f.write(download.content)
                                f.close()
                        print('...')
            print('Download de ' + str(get_name) + ' realizado com sucesso!')                 
                 
    except:
         print('OPS! Música não encontrada')

       
