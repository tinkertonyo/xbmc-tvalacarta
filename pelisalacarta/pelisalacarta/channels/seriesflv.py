# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesflv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "seriesflv"
__channel__ = "seriesflv"
__language__ = "ES"
__creationdate__ = "20140615"

DEFAULT_HEADERS = []
DEFAULT_HEADERS.append( ["User-Agent","Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12"] )

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.seriesflv mainlist")

    itemlist = []

    itemlist.append( Item(channel=__channel__, action="menuepisodios" , title="Últimos episodios..." , url="" ))
    itemlist.append( Item(channel=__channel__, action="series"        , title="Todas las series"     , url="http://www.seriesflv.net/ajax/lista.php", extra="grupo_no=0&type=series&order=titulo" ))
    itemlist.append( Item(channel=__channel__, action="series"        , title="Series más vistas"    , url="http://www.seriesflv.net/ajax/lista.php", extra="grupo_no=0&type=series&order=hits" ))
    itemlist.append( Item(channel=__channel__, action="series"        , title="Telenovelas"          , url="http://www.seriesflv.net/ajax/lista.php", extra="grupo_no=0&type=generos&order=novelas" ))
    itemlist.append( Item(channel=__channel__, action="search"        , title="Buscar..."            , url="http://www.seriesflv.net/api/search/?q=" ))
       
    return itemlist

def menuepisodios(item):
    logger.info("pelisalacarta.channels.seriesflv menuepisodios")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="ultimos_episodios"  , title="Subtitulados" , url="sub" ))
    itemlist.append( Item(channel=__channel__, action="ultimos_episodios"  , title="Español"      , url="es" ))
    itemlist.append( Item(channel=__channel__, action="ultimos_episodios"  , title="Latino"       , url="la" ))
    itemlist.append( Item(channel=__channel__, action="ultimos_episodios"  , title="Original"     , url="en" ))
    return itemlist

def ultimos_episodios(item):
    logger.info("pelisalacarta.channels.seriesflv ultimos_episodios")
    itemlist = []

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    data = scrapertools.cache_page("http://www.seriesflv.net/",headers=headers)
    #logger.info("data="+data)

    # Extrae los episodios
    '''
    <a href="http://www.seriesflv.net/ver/ciega-a-citas-1x72.html" class="item-one" lang="es" title="Ciega a citas 1x72 Online Sub Español Gratis">
    <div class="box-tc">1x72</div>
    <div class="box-info">
    <div class="i-title">Ciega a citas</div>
    <div class="i-time">Hace 10 minutos</div>
    </div>
    </a>
    '''
    idioma = item.url
    patron  = '<a href="([^"]+)" class="item-one" lang="'+idioma+'"[^<]+'
    patron += '<div class="box-tc">([^<]+)</div[^<]+'
    patron += '<div class="box-info"[^<]+'
    patron += '<div class="i-title">([^<]+)</div[^<]+'
    patron += '<div class="i-time">([^<]+)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl,episodio,serie,hace in matches:
        title = serie+" "+episodio+" ("+hace+")"
        thumbnail = ""
        plot = ""
        url = scrapedurl
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title))

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    return itemlist


def search(item,texto):
    logger.info("pelisalacarta.channels.seriesflv search")

    texto = texto.replace(" ","%20")

    if item.url=="":
        item.url="http://www.seriesflv.net/api/search/?q="

    item.url = item.url+texto

    try:
        return buscar(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def buscar(item):
    logger.info("pelisalacarta.channels.seriesflv buscar")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    headers.append(["Referer","http://www.seriesflv.net/series/"])
    headers.append(["X-Requested-With","XMLHttpRequest"])

    post = item.extra

    data = scrapertools.cache_page(item.url , headers=headers , post=post)
    logger.info("data="+data)

    # Extrae las entradas (carpetas)
    '''
    <ul><div class="bg7 header color7">Resultados de <b>equipo a</b></div>      
    <li><a class="on over" href="http://www.seriesflv.net/serie/el-equipo-a.html">
    <div class="left">
    <img src="http://http-s.ws/ysk/img/data/b5de7e0470eae36f8196d8fcbf897c17-size-90x120-a.jpg" />
    </div><div class="op">
    <span class="color1 bold tit">El equipo A</span>
    <span class="color8 font2">6 temporadas</span><span><div class="star_rating over">
    <ul style="float:none; left:auto;" class="star">
    <li style="width: 100%;" class="curr"></li>
    </ul>
    </div></span></div></a></li>
    </ul>
    '''
    patron  = '<li><a class="on over" href="([^"]+)"[^<]+'
    patron += '<div class="left"[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '</div><div class="op"[^<]+'
    patron += '<span class="[^"]+">([^<]+)</span[^<]+'
    patron += '<span class="[^"]+">([^<]+)</span>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedthumbnail,scrapedtitle,numtemporadas in matches:

        title = scrapertools.htmlclean(scrapedtitle).strip()+" ("+numtemporadas+")"
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""

        url = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title))
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    return itemlist

def series(item):
    logger.info("pelisalacarta.channels.seriesflv series")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    headers.append(["Referer","http://www.seriesflv.net/series/"])
    headers.append(["X-Requested-With","XMLHttpRequest"])

    post = item.extra

    data = scrapertools.cache_page(item.url , headers=headers , post=post)
    logger.info("data="+data)

    # Extrae las entradas (carpetas)
    '''
    <ul><li>
    <a href="http://www.seriesflv.net/serie/game-of-thrones.html" class="on over">
    <div class="left">
    <img src="http://http-s.ws/ysk/img/data/11a1a46bca5c4cca2cac0d0711225feb-size-90x120-a.jpg" width="50" height="60" />
    Game of Thrones (Juego de tronos)</div>
    <div class="rigth over">

    <div class="left op">
    <span>4</span>
    <p>Temporadas</p>
    </div>
    '''
    patron  = '<a.*?href="([^"]+)"[^<]+'
    patron += '<div class="left"[^<]+'
    patron += '<img.*?src="([^"]+)"[^>]*>([^<]+)</div[^<]+'
    patron += '<div class="rigth over"[^<]+'
    patron += '<div class="left op"[^<]+'
    patron += '<span>([^<]+)</span'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedthumbnail,scrapedtitle,numtemporadas in matches:

        title = scrapertools.htmlclean(scrapedtitle).strip()+" ("+numtemporadas+" temporadas)"
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""

        url = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=title))
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    #grupo_no=0&type=series&order=titulo
    old_offset = scrapertools.find_single_match(item.extra,"grupo_no\=(\d+)")
    new_offset = str(int(old_offset)+1)
    newextra = item.extra.replace("grupo_no="+old_offset,"grupo_no="+new_offset)
    itemlist.append( Item(channel=__channel__, action="series" , title=">> Página siguiente" , extra=newextra, url=item.url))

    return itemlist

def get_nombre_idioma(idioma):

    if idioma=="es":
        return "Español"
    elif idioma=="en":
        return "Inglés"
    elif idioma=="la":
        return "Latino"
    elif idioma=="sub":
        return "VOS"
    else:
        return idioma

def episodios(item):
    logger.info("pelisalacarta.channels.seriesflv episodios")
    itemlist = []

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    data = scrapertools.cache_page(item.url,headers=headers)
    #logger.info("data="+data)

    # Extrae los episodios
    '''
    <tr>
    <td class="sape"><i class="glyphicon glyphicon-film"></i> <a href="http://www.seriesflv.net/ver/game-of-thrones-1x9.html" class="color4">Game of Thrones (Juego de tronos) 1x09</a></td>
    <td>
    <a href="javascript:void(0);" class="loginSF" title="Marcar Visto"><span class="no visto"></span></a>
    </td>
    <td><div class="star_rating">
    <ul class="star">
    <li class="curr" style="width: 99.6%;"></li>
    </ul>
    </div></td>
    <td>
    <img src="http://www.seriesflv.net/images/lang/es.png" width="20" />
    <img src="http://www.seriesflv.net/images/lang/la.png" width="20" />
    <img src="http://www.seriesflv.net/images/lang/sub.png" width="20" />
    </td>
    <td>40,583</td>
    </tr>
    '''
    patron  = '<tr[^<]+<td class="sape"><i class="glyphicon glyphicon-film"></i[^<]+'
    patron += '<a href="([^"]+)"[^>]+>([^<]+)</a>.*?<img(.*?)</td'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl,scrapedtitle,bloqueidiomas in matches:
        title = scrapedtitle+" ("

        patronidiomas="lang/([a-z]+).png"
        matchesidiomas = re.compile(patronidiomas,re.DOTALL).findall(bloqueidiomas)
        for idioma in matchesidiomas:
            title=title+get_nombre_idioma(idioma)+", "

        title=title[:-2]+")"

        thumbnail = ""
        plot = ""
        url = scrapedurl
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, fulltitle=title))

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.seriesflv findvideos")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    data = scrapertools.cache_page(item.url,headers=headers)
    data = scrapertools.find_single_match(data,'<div id="enlaces">(.*?)<div id="comentarios">')
    #logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    '''
    <tr>
    <td width="45"><img width="20" src="http://www.seriesflv.net/images/lang/es.png"></td>
    <td width="86">2014-04-03</td>
    <td width="134" style="text-align:left;"><img width="16" src="http://www.google.com/s2/favicons?domain=gamovideo.com"> gamovideo</td>
    <td width="84"><a href="http://www.seriesflv.net/reproductor/?go=3Se67975zSF73F2SbnvpMlOoJWfQHQEQP7hCqqNzOqNTSUBt90wx9Lj0DUVi2vGcV32wTiKeNId%2FtnFDVGdUPQ%3D%3D" data-uri="http://gamovideo.com/i9445na28nrm" rel="nofollow" target="_blank" title="Reproducir..." class="btn btn-primary btn-xs bg2"><i class="glyphicon glyphicon-play"></i> Reproducir</a></td>
    <td width="96" class="usuario"><a href="http://www.seriesflv.net/usuario/natzuflv/" rel="nofollow" class="color1">Natzuflv</a></td>
    <td width="200">Hace 3 meses | HD 720p</td>
    <td width="92">
    <div class="report off">
    <a href="#" class="btn btn-danger btn-xs loginSF"><i class="glyphicon glyphicon-warning-sign"></i></a>
    </div>
    <div class="views on">2,595</div>
    </td>
    </tr>
    '''
    '''
    <tr>
    <td width="45"><img width="20" src="http://www.seriesflv.net/images/lang/sub.png"></td>
    <td width="86">2014-08-10</td>
    <td width="134" style="text-align:left;"><img width="16" src="http://www.google.com/s2/favicons?domain=tumi.tv"> tumi</td>
    <td width="84"><a href="http://www.seriesflv.net/goto/" data-key="qXFa+2QrDcOkQxTBiRWMDvjw9twofrTPwY6R3IV1tEU=" rel="nofollow" target="_blank" title="Reproducir..." class="btn btn-primary btn-xs bg2 enlace_link"><i class="glyphicon glyphicon-play"></i> Reproducir</a></td>
    <td width="96" class="usuario"><a href="http://www.seriesflv.net/usuario/natzuflv/" rel="nofollow" class="color1">Natzuflv</a></td>
    <td width="200">Hace 3 horas | </td>

    <td width="45"><img width="20" src="http://www.seriesflv.net/images/lang/sub.png"></td>
    <td width="86">2014-03-22</td>
    <td width="134" style="text-align:left;"><img width="16" src="http://www.google.com/s2/favicons?domain=nowdownload.ch"> nowdownload</td>
    <td width="84"><a href="http://www.seriesflv.net/goto/" rel="nofollow" target="_blank" title="Descargar...!" data-key="eZMOyiO7JKrg7YI9FegHR97/raBhS4x3qa1gc9S0yVQ=" class="btn btn-primary btn-xs bg2 enlace_link"><i class="glyphicon glyphicon-cloud-download"></i> Descargar</a></td>
    <td width="96" class="usuario"><a href="http://www.seriesflv.net/usuario/mayaflv/" rel="nofollow" class="color1">MayaFLV</a></td>
    <td width="200">Hace 7 meses | </td>

    '''

    patron  = '<tr[^<]+'
    patron += '<td[^<]+<img width="\d+" src="([^"]+)"></td[^<]+'
    patron += '<td[^<]+</td[^<]+'
    patron += '<td[^<]+<img[^>]+>([^<]+)</td[^<]+'
    patron += '<td[^<]+<a href="([^"]+)".*?data-key="([^"]+)"[^<]+<i[^<]+</i[^<]+</a></td[^<]+'
    patron += '<td[^<]+<a[^<]+</a></td[^<]+'
    patron += '<td[^>]+>([^<]+)</td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for url_idioma,nombre_servidor,target_url,key_url,comentario in matches:
        codigo_idioma = scrapertools.find_single_match(url_idioma,'lang/([a-z]+).png')
        idioma = get_nombre_idioma(codigo_idioma)

        title = "Ver en "+nombre_servidor.strip()+" ("+idioma+") ("+comentario.strip()+")"
        url = target_url
        extra = key_url
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, extra=extra, thumbnail=thumbnail, plot=plot, folder=False))

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.seriesflv play url="+item.url)

    # Hace la llamada
    if item.extra!="":
        '''
        Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
        Accept-Encoding:gzip,deflate,sdch
        Accept-Language:es-ES,es;q=0.8,en;q=0.6
        Cache-Control:max-age=0
        Connection:keep-alive
        Content-Length:178
        Content-Type:multipart/form-data; boundary=----WebKitFormBoundaryzyvJgsMftSHwzZNf
        Cookie:perseguidor-limit=COOKIE1407744675853; __utma=253162379.911083080.1407744679.1407744679.1407744679.1; __utmb=253162379.1.10.1407744679; __utmc=253162379; __utmz=253162379.1407744679.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)
        Host:www.seriesflv.net
        Origin:http://www.seriesflv.net
        Referer:http://www.seriesflv.net/ver/satisfaction--1x03.html
        User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36
        Request Payload
        ------WebKitFormBoundaryzyvJgsMftSHwzZNf
        Content-Disposition: form-data; name="url"

        qXFa+2QrDcOkQxTBiRWMDvjw9twofrTPwY6R3IV1tEU=
        ------WebKitFormBoundaryzyvJgsMftSHwzZNf--
        Response Headersview source
        '''
        body  = '------WebKitFormBoundaryzyvJgsMftSHwzZNf\n'
        body += 'Content-Disposition: form-data; name="url"\n'
        body += '\n'
        body += item.extra+'\n'
        body += '------WebKitFormBoundaryzyvJgsMftSHwzZNf--\n'

        headers = []
        headers.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"])
        headers.append(["Accept-Encoding","gzip,deflate,sdch"])
        headers.append(["Accept-Language","es-ES,es;q=0.8,en;q=0.6"])
        headers.append(["Cache-Control","max-age=0"])
        headers.append(["Connection","keep-alive"])
        headers.append(["Content-Length",str(len(body))])
        headers.append(["Content-Type","multipart/form-data; boundary=----WebKitFormBoundaryzyvJgsMftSHwzZNf"])
        headers.append(["Origin","http://www.seriesflv.net"])
        headers.append(["Referer","http://www.seriesflv.net/ver/satisfaction--1x03.html"])
        headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"])
        data = scrapertools.cache_page(item.url,headers=headers,post=body)
        logger.info("data="+data)
    else:
        data = item.url
    
    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist    