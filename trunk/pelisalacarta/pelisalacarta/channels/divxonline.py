# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para divxonline
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
from core import anotador
import base64
import datetime
import time

from servers import servertools
from core import scrapertools
from core import config
from core import logger
from core.item import Item

#from pelisalacarta import buscador

__channel__ = "divxonline"
__category__ = "F"
__type__ = "generic"
__title__ = "Divx Online"
__language__ = "ES"

DEBUG = config.get_setting("debug")

Generate = False # poner a true para generar listas de peliculas
Notas = False # indica si hay que a�adir la nota a las pel�culas
LoadThumbs = True # indica si deben cargarse los carteles de las pel�culas; en MacOSX cuelga a veces el XBMC

def isGeneric():
    return True

def mainlist(item):
    logger.info("[divxonline.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas"   , title="Pel�culas - Novedades",url="http://www.divxonline.info/"))
    #itemlist.append( Item(channel=__channel__, action="categorias" , title="Pel�culas - Categor�as",url="http://www.divxonline.info/"))
    #itemlist.append( Item(channel=__channel__, action="peliculas"  , title="Pel�culas - Estrenos",url="http://www.divxonline.info/peliculas-estreno/1.html"))
    itemlist.append( Item(channel=__channel__, action="alfabetico"  , title="Pel�culas - A-Z"))
    #itemlist.append( Item(channel=__channel__, action="pelisporanio"  , title="Pel�culas - Por a�o de estreno"))
    itemlist.append( Item(channel=__channel__, action="search"        , title="Buscar"))
    return itemlist

# Al llamarse "search" la funci�n, el launcher pide un texto a buscar y lo a�ade como par�metro
def search(item,texto):
    logger.info("[divxonline.py] search")
    itemlist = []
    
    if item.url=="":
        item.url = "http://www.divxonline.info/"

    # Lanza la b�squeda
    data=scrapertools.cachePagePost("http://www.divxonline.info/buscador.html","buscar="+texto+"&categoria=0&tipo=1&boton=")

    #logger.info(data)
    data=scrapertools.get_match(data,'<div class="caja margen-inf1">[^<]+<h3>Resultados de la palabra(.*?)</div>')
    
    #<li><a href="/pelicula/306/100-chicas-2000/">100 chicas (2000)</a></li>
    patronvideos  = '<li><a href="(.+?)"><font[^<]+<b>([^<]+)<'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for url,title in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedtitle = title

        itemlist.append( Item(channel=__channel__, title = scrapedtitle, fulltitle=scrapedtitle, url=scrapedurl, action="findvideos", plot=scrapedplot, thumbnail=scrapedthumbnail ) )
    
    return itemlist

def peliculas(item):
    logger.info("[divxonline.py] peliculas")
    itemlist=[]
    
    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas
    patron  = '<div class="ficha margen-inf1">[^<]+'
    patron += '<h2><a href="([^"]+)">([^<]+)</a></h2>[^<]+'
    patron += '<div class="foto-link">[^<]+'
    patron += '<img src="([^"]+)".*?'
    patron += '<li><span class="color_azul-ficha">Sinopsis:</span>(.*?)</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,title,thumbnail,plot in matches:
        # Titulo
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = scrapertools.htmlclean(plot).strip()
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    '''
    <div class="ficha margen-inf1">
    <h2>Daens (1993)</h2>
    <div class="foto-link">
    <img src="http://imagenes.divxonline.info/divxonline.info_daens.jpg" width="150" height="200" style="border: 1px solid #FF9900" alt="Daens (1993)" title="Daens (1993)" />
    <a href="/pelicula-divx/6963/Daens-1993/" class="boton-informacion">Ver online</a>
    <a href="/descarga-directa/6963/Daens-1993/" class="boton-descargar">Descargar</a>
    </div>
    <ul>
    <li>
    <div class="tituloPeliculaVotar">
    <span class="color_azul-ficha">Valoraci&oacute;n:</span>
    </div>
    <div class="formPeliculaVotar">
    <form id="ratings6963" class="ratings" action="/votar.php" method="post">
    <input type="radio" name="rate" value="1:6963" title="P&eacute;sima" id="rate16963" /> <label for="rate16963">P&eacute;sima</label><br />
    <input type="radio" name="rate" value="2:6963" title="Mala" id="rate26963" /> <label for="rate26963">Mala</label><br />
    <input type="radio" name="rate" value="3:6963" title="Regular" id="rate36963" /> <label for="rate36963">Regular</label><br />
    <input type="radio" name="rate" value="4:6963" title="Buena" id="rate46963" checked="checked"/> <label for="rate46963">Buena</label><br />
    <input type="radio" name="rate" value="5:6963" title="Excelente" id="rate56963" /> <label for="rate56963">Excelente</label><br />
    <input type="submit" value="Votar" />
    </form>
    <p id="respvotar6963"></p>
    </div>
    <div class="fix"></div>
    </li>
    <li><span class="color_azul-ficha">G&eacute;nero:</span> <a href="/peliculas/13/dramas/">Dramas</a></li>
    <li><span class="color_azul-ficha">Director(es):</span> </li>
    <li><span class="color_azul-ficha">Actor(es):</span> </li>
    <li><span class="color_azul-ficha">Autorizada:</span> <a href="/peliculas/No-recomendada-a-menores-de-7-anos/1/">No recomendada a menores de 7 a�os</a></b></li>
    <li><span class="color_azul-ficha">Vista:</span> 25080 veces<br /></li>
    <li><span class="color_azul-ficha">Sinopsis:</span> La pel�cula relata la vida del Padre Daens en B�lgica a finales del siglo XIX. La acci�n trancurre en la localidad belga de Aalst durante los primeros a�os de este siglo. En este pueblo se inicia una revuelta para protestar por las duras condiciones de los obreros de las f�bricas. Cuando el religioso Adolf Daens escribr un art�culo denunciando e...  <a href="/pelicula/6963/Daens-1993/">(leer m&aacute;s)</a></li>
    
    </ul>
    </div>
    '''
    patron  = '<div class="ficha margen-inf1">[^<]+'
    patron += '<h2>([^<]+)</h2>[^<]+'
    patron += '<div class="foto-link">[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '<a href="([^"]+)".*?'
    patron += '<li><span class="color_azul-ficha">Sinopsis:</span>(.*?)</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for title,thumbnail,url,plot in matches:
        # Titulo
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url.replace("/pelicula-divx/","/pelicula/").replace("/descarga-directa/","/pelicula/"))
        scrapedthumbnail = thumbnail
        scrapedplot = scrapertools.htmlclean(plot).strip()
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    #<a href='/peliculas-online-divx-2.html'>&gt;&gt;</a> 
    patron = "<a href='([^']+)'>\&gt\;\&gt\;</a>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        itemlist.append( Item(channel=__channel__, action="peliculas", title="!P�gina siguiente" , url=urlparse.urljoin(item.url,matches[0]) , folder=True) )

    return itemlist

def alfabetico(item):
    logger.info("[divxonline.py] alfabetico")
    itemlist = []

    letras = "9ABCDEFGHIJKLMN�OPQRSTUVWXYZ" # el 9 antes era 1, que curiosamente est� mal en la web divxonline (no funciona en el navegador)
    for letra in letras:
        itemlist.append( Item(channel=__channel__, action="peliculas", title=str(letra), url = "http://www.divxonline.info/verpeliculas/"+str(letra)+"_pagina_1.html"))

    return itemlist

def categorias(item):
    logger.info("[divxonline.py] categorias")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    patron = '<a href="(/peliculas.*?-megavideo/)">([^<]+)</a><br>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=__channel__, action="movielist", title=match[1], url = urlparse.urljoin(item.url,match[0])))

    return itemlist

def pelisporanio(item):
    logger.info("[divxonline.py] pelisporanio")
    itemlist = []

    #for anio in range(2009,1915,-1):
    for anio in range(datetime.datetime.today().year,1915,-1):
        itemlist.append( Item(channel=__channel__, action="peliculasc", title=str(anio), url = "http://www.divxonline.info/peliculas-anho/"+str(anio)+"/1.html"))

    return itemlist

def movielist(item): # pelis sin ficha (en listados por g�nero)
    logger.info("[divxonline.py] movielist")
    itemlist=[]

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    data = stepinto(item.url,data,'Ver p�gina:(.*?)</p>')

    # Extrae las entradas (carpetas)
    patronvideos  = '<li><h2><a href="([^"]+?)">(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)

    if (Generate):
        f = open(config.DATA_PATH+'/films.tab', 'w') # fichero para obtener las notas

    for match in matches:
        # Titulo
        scrapedtitle = remove_html_tags(match[1])
        if (not Generate and Notas):
            score = anotador.getscore(remove_html_tags(match[1]))
            if (score != ""):
                scrapedtitle += " " + score

        # URL
        scrapedurl = urlparse.urljoin(item.url,match[0]) # url de la ficha divxonline
        scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la p�gina de reproducci�n

        # Thumbnail
        #scrapedthumbnail = urlparse.urljoin(url,match[1])
        scrapedthumbnail = ""

        # procesa el resto
        scrapedplot = ""

        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        if (Generate):
            sanio = re.search('(.*?)\((.*?)\)',scrapedtitle)
            if (sanio): # si hay anio
                fareg = sanio.group(1) + "\t" + sanio.group(2) + "\t" + scrapedtitle
            else:
                fareg = scrapedtitle + "\t\t" + scrapedtitle
            f.write(fareg+"\n")

        # A�ade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    if (Generate):
        f.close()

    return itemlist

def findvideos(item):
    logger.info("[divxonline.py] findvideos(%s)" % item.tostring())
    itemlist = []
    
    # Descarga la p�gina
    data = scrapertools.cachePage(item.url.replace("pelicula","pelicula-divx"))
    patron = '<table class="parrillaDescargas">(.*?)</table>'
    data = scrapertools.get_match(data,patron)
    
    '''
    <td class="numMirror"><img src="http://webs.ono.com/divx/img/filmes1.png" align="middle" alt="Ver online" title="Ver online" /> <a target="_blank" href="/video/40-putlocker/82381-007-Al-servicio-secreto-de-su-Majestad-1969.html"> <b>1</ b> <img src="http://webs.ono.com/divx/img/flecha.png" align="middle" /></a></td>
    <td class="hostParrilla"><a target="_blank" href="/video/40-putlocker/82381-007-Al-servicio-secreto-de-su-Majestad-1969.html"><img src="http://imagenes.divxonline.info/logos_servers/40.jpg" height="23" alt="Host" title="Host" /></a></td>
    <td class="idiomaParrilla"><a target="_blank" href="/video/40-putlocker/82381-007-Al-servicio-secreto-de-su-Majestad-1969.html"><img src="http://imagenes.divxonline.info/idiomas/1.png" alt="Audio" title="Audio" /></a></td>
    <td class="partesParrilla"><a target="_blank" href="/video/40-putlocker/82381-007-Al-servicio-secreto-de-su-Majestad-1969.html">1</a></td>
    <td class="uploaderParrilla"><a target="_blank" href="/video/40-putlocker/82381-007-Al-servicio-secreto-de-su-Majestad-1969.html">anonimo</a></td>
    '''
    patron  = '<td class="numMirror">.*?</td>[^<]+'
    patron += '<td class="hostParrilla"><a target="_blank" href="([^"]+)"><img src="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,thumbnail in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedtitle = url
        try:
            scrapedtitle = scrapedtitle.split("/")[2]
        except:
            pass
        
        scrapedtitle = "Ver online "+scrapedtitle
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , fulltitle=item.title , url=scrapedurl , thumbnail=thumbnail , plot=item.plot , folder=False) )

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url.replace("pelicula","descarga-directa"))
    patron = '<table class="parrillaDescargas">(.*?)</table>'
    data = scrapertools.get_match(data,patron)
    
    patron  = '<td class="numMirror">.*?</td>[^<]+'
    patron += '<td class="hostParrilla"><a target="_blank" href="([^"]+)"><img src="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,thumbnail in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedtitle = url
        try:
            scrapedtitle = scrapedtitle.split("/")[2]
        except:
            pass
        
        scrapedtitle = "Descarga directa "+scrapedtitle
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , fulltitle=item.title , url=scrapedurl , thumbnail=thumbnail , plot=item.plot , folder=False) )

    return itemlist

def play(item):
    logger.info("[divxonline.py] play")
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)

    logger.info("***********************************************************************************************************************")
    patron  = "decodeBase64\('(.+?)'\)"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        cadena = matches[0]
        validchars = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!#$%&'()-@[]^_`{}~.<>"
        cadena = ''.join(c for c in cadena if c in validchars)
        logger.info(  cadena  )

    data=decryptinks(data);
    logger.info("***********************************************************************************************************************")
    logger.info(data)
    logger.info("***********************************************************************************************************************")
    logger.info("***********************************************************************************************************************")
    logger.info("***********************************************************************************************************************")
    logger.info("***********************************************************************************************************************")
    itemlist = servertools.find_video_items(data=data)
    i=1
    for videoitem in itemlist:
        videoitem.title = "Mirror %d%s" % (i,videoitem.title)
        videoitem.fulltitle = item.fulltitle
        videoitem.channel=channel=__channel__
        i=i+1

    return itemlist

def decryptinks(text):
    patronvideos  = "decodeBase64\('(.+?)'\)"
    matches = re.compile(patronvideos,re.DOTALL).findall(text)
    #string='yFA/B6/fgVeTFPS4NIqijSVtVUemN39H+e6EuYNxcNiHnCsZeU3W0iY29Fbye4GjyIrqXD9RTiVAU/gI7Pq7Qi1vnoRkLooganMExe36ySUofSME6cF5zgQPoQvnsRNQbp0owGrUZ0fx0EuMWghIg8PeCbyzW46jM/czf0neyBePLXvg6u0tYdvCHF7JdLLGpH20CWO6mX8bc2rDAz+bUNshJS/eHNhLCblzvrKbJcddzQRfOkyriWOTusBm3wDZ1kZMs2fEckZRMBvUIiQljZ0L1IV3wDkVQ9cbdDqEIHlWi/xmHtVsb4G+SAMpsBNpXJzfzle4IZaHWdt+GOsI+y1DiHdRJ9mizN0+mEUsIhGqgJMiIMzeFeSmRQ21PxDVXP0yLKcsX3IPfPlcIOGcAGXcpXLgchisgZoyej4aEk0MTsRFGto4kvGzHBAyFrsf+UfKZf4ZqYQmx1pFMl8A0CQbhAoOgKioUFNOASCSTpvNqwiL1aRJuYQo/MzOLjhTcwrTua5Cg50513LwRkC7BJcIsHKCuWvU3CyKKV5Iz1M4qB5C4dBISifGiaisjwmprQk4VWeLVmyba+lzpfDa7PjGs3Hh54cE6BoN4aJVqaUpLvbxJfd2A4ODlTrOQZmFa32dfZYEIpB5EejTqY6TU4AW3p9G+Kd4TNAjTE2KVfUIW5bhXSvEE5Gs8JCp1xxgPcwrSTVdqe+VsjhqKjihnMouWiXn5pQzv2DlsGzDB1jShTmdWvo9gv4kya16ZzBUalTPTXVVPlapL4OMIJgwXzGPkO+2mwjgdjF8jzaUjn3bowuDdMaix5xpfJmI5IlHAJYKL4T0oVBE+gMFJsUa09IuBMi48ARSa8hXDmGf9nCpcAJ8jCrBdtj0Apm3CgaNWwdhxJhGb5RCLenTvOwB81N7sbyuWI2XzlKdRuUddJgD+3YDFxh1/gkTFgPWyq4xMuEoiZGcVKvfXpIeIZR6JN7cX3kL1HYfJYyZUs6IsYqQOaOy+gjVVw6GgE25oBD9geh8cS5mx94XxIXmi/1KUcYztxx/+zPSihLJ404sVnaxQ2LfpM7QtUUFZnyz4olTEfdQXxaQPUzIbuceyGqJig1djjiGw5qAHYcQQ45gJC3Gs+bzo4xiIJQHSTvi1SP7b9Ge9bV9SjOJ5kt1Z4CZoehu9VYKc+PcUFwWVeWN2Xf+Xp8xf5txn6upEc0tiUbSsQCRkZmJVVJntibWDnq4MjeczapU/sBgsULj5h7+llwmaKgdTCAfOLqWWX69z7ncwXbg+Aws/t6W75nHeAMVbK+Xt+3zNgCQE8M='
    #logger.info(matches);
    result=base64.b64decode(matches[0])
    return(Procesa('cryptkey', result));

def Procesa (key, pt):
    j=0;
    i=0
    ct=''

    s = [255] * 257

    for i in range(0, 256):
            s[i] = i;
    for i in range(0, 256):
            j= ( j + s[i] + ord(key[i%len(key)]))%256;
            x = s[i];
            s[i] = s[j];
            s[j] = x;

    i=0
    j=0
    for y in range(0, len(pt)):
            i = (i + 1) % 256;
            j = (j + s[i]) % 256;
            x = s[i];
            s[i] = s[j];
            s[j] = x;
            ct += chr(ord(pt[y]) ^ s[(s[i] + s[j]) % 256]);
    return ct


# Verificaci�n autom�tica de canales: Esta funci�n debe devolver "True" si todo est� ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Da por bueno el canal si alguno de los v�deos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos(pelicula_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien