# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para putlocker
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[putlocker.py] test_video_exists(page_url='%s')" % page_url)

    location = scrapertools.get_header_from_response( url = page_url , header_to_get = "location")
    if location=="":
        return True,""
    elif "&404" in location:
        return False,"El archivo no existe<br/>en putlocker o ha sido borrado."
    else:
        return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[putlocker.py] url="+page_url)
    data = scrapertools.cache_page(page_url)

    patron  = '<form method="post">[^<]+'
    patron += '<input type="hidden" value="([0-9a-f]+?)" name="([^"]+)">[^<]+'
    patron += '<input name="confirm" type="submit" value="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0: return []

    post = matches[0][1]+"="+matches[0][0]+"&confirm="+(matches[0][2].replace(" ","+"))
    headers = []
    headers.append( ['User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:10.0.2) Gecko/20100101 Firefox/10.0.2'] )
    headers.append( [ "Accept" , "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ])
    headers.append( ['Referer',page_url] )

    data = scrapertools.cache_page( page_url , post=post, headers=headers )
    #logger.info("data="+data)
    # extrae 
    patron = "playlist: '(.+?)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    video_urls = []
    if len(matches)>0:
        xmlurl = urlparse.urljoin(page_url,matches[0])
        logger.info("[putlocker.py] Playlis="+xmlurl)
    
        logger.info("xmlurl="+xmlurl)
        data = scrapertools.downloadpageWithoutCookies(xmlurl)
        # Extrae la URL
        patron = '</link><media\:content url="(.+?)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        
        if len(matches)>0:
            video_urls.append( ["."+matches[0].rsplit('.',1)[1][0:3]+" [putlocker]",matches[0]])

    else:
        logger.info("[putlocker.py] No encuentra Playlist")
        #url: 'http://s3.putlocker.ch:86/2015.mp4?key=2daad71cdc34f5a2e10665cf0efe1356'
        videourl = scrapertools.get_match(data,"url\: '([^']+)'")
        video_urls.append( ["[putlocker]",videourl] )
    

    for video_url in video_urls:
        logger.info("[putlocker.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra v�deos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.peliculasaudiolatino.com/show/putlocker.php?url=CEE0B3A7DDFED758
    patronvideos  = 'putlocker.php\?url=([A-Z0-9]+)'
    logger.info("[putlocker.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[putlocker]"
        url = "http://www.putlocker.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'putlocker' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    # http://www.putlocker.com/embed/CEE0B3A7DDFED758 | http://www.putlocker.com/file/CEE0B3A7DDFED758
    patronvideos  = 'http://www.putlocker.com/(?:file|embed)/([A-Z0-9]+)'
    logger.info("[putlocker.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[putlocker]"
        url = "http://www.putlocker.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'putlocker' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #//www.cinezer.com/putlocker/CD6003D971725774
    patronvideos  = '/putlocker/([A-Z0-9]+)'
    logger.info("[putlocker.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[putlocker]"
        url = "http://www.putlocker.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'putlocker' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.putlocker.ch/file/0e6f1eeb473e0d87b390a71cd50c24a2/
    patronvideos  = '(putlocker.ch/file/[a-z0-9]+)'
    logger.info("[putlocker.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[putlocker]"
        url = "http://www."+match+"/"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'putlocker' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.player3k.info/putlocker/?id=92FA671A11CA7A05
    patronvideos  = '/putlocker/\?id\=([A-Z0-9]+)'
    logger.info("[putlocker.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[putlocker]"
        url = "http://www.putlocker.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'putlocker' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    
    return devuelve
