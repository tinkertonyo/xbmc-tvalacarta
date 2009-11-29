# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Utilidades para detectar v�deos de los diferentes conectores
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools

import megavideo
import megaupload
import tutv
import stagevu
import vreel
import movshare
import veoh

xbmc.output("[servertools.py] init")

def findvideos(data):
	xbmc.output("[servertools.py] findvideos")
	encontrados = set()
	devuelve = []

	# Megavideo - V�deos con t�tulo
	xbmc.output("1) Megavideo con titulo...")
	patronvideos  = '<div align="center">([^<]+)<.*?<param name="movie" value="http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = match[0].strip()
		if titulo == "":
			titulo = "[Megavideo]"
		url = match[1]
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Megavideo - V�deos con t�tulo
	xbmc.output("1b) Megavideo con titulo...")
	patronvideos  = '<a href\="http\:\/\/www.megavideo.com/\?v\=([A-Z0-9]{8})".*?>([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = match[1].strip()
		if titulo == "":
			titulo = "[Megavideo]"
		url = match[0]
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	xbmc.output("1c) Megavideo sin titulo...")
	#http://www.megavideo.com/?v=OYGXMZBM
	patronvideos  = 'http\:\/\/www.megavideo.com/\?v\=([A-Z0-9]{8})"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		titulo = ""
		if titulo == "":
			titulo = "[Megavideo]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	xbmc.output("1d) Megavideo sin titulo...")
	#http://www.megavideo.com/?v=OYGXMZBM
	patronvideos  = 'http\:\/\/www.megavideo.com/\?v\=([A-Z0-9]{8})'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		titulo = ""
		if titulo == "":
			titulo = "[Megavideo]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	xbmc.output("1d) Megaupload sin titulo...")
	#http://www.megavideo.com/?v=OYGXMZBM
	patronvideos  = 'http\:\/\/www.megaupload.com/\?d\=([A-Z0-9]{8})'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		titulo = ""
		if titulo == "":
			titulo = "[Megaupload]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megaupload' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Megavideo - V�deos sin t�tulo
	xbmc.output("2) Megavideo sin titulo...")
	patronvideos  = '<param name="movie" value="http://wwwstatic.megavideo.com/mv_player.swf\?v=([^"]+)">'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "[Megavideo]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Vreel - V�deos con t�tulo
	xbmc.output( "3) Vreel con t�tulo...")
	patronvideos  = '<div align="center"><b>([^<]+)</b>.*?<a href\="(http://beta.vreel.net[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = match[0].strip()
		if titulo == "":
			titulo = "[Vreel]"
		url = match[1]
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Vreel' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Vreel - V�deos con t�tulo
	xbmc.output("4) Vreel con titulo...")
	patronvideos  = '<div align="center">([^<]+)<.*?<a href\="(http://beta.vreel.net[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = match[0].strip()
		if titulo == "":
			titulo = "[Vreel]"
		url = match[1]
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Vreel' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	'''
	# WUAPI
	xbmc.output("5) wuapi sin t�tulo")
	patronvideos  = '<a href\="(http://wuapi.com[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin t�tulo ("+match[23:]+")"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Wuapi' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# WUAPI
	xbmc.output("6) wuapi sin t�tulo...")
	patronvideos  = '(http://wuapi.com[^<]+)<'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin t�tulo ("+match[23:]+")"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Wuapi' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)
	'''
	
	# STAGEVU
	xbmc.output("7) Stagevu sin t�tulo...")
	patronvideos  = '"(http://stagevu.com[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "[Stagevu]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Stagevu' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# TU.TV
	xbmc.output("8) Tu.tv sin t�tulo...")
	patronvideos  = '<param name="movie" value="(http://tu.tv[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "[tu.tv]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'tu.tv' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# TU.TV
	xbmc.output("9) Tu.tv sin t�tulo...")
	#<param name="movie" value="http://www.tu.tv/tutvweb.swf?kpt=aHR0cDovL3d3dy50dS50di92aWRlb3Njb2RpL24vYS9uYXppcy11bi1hdmlzby1kZS1sYS1oaXN0b3JpYS0xLTYtbGEtbC5mbHY=&xtp=669149_VIDEO"
	patronvideos  = '<param name="movie" value="(http://www.tu.tv[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "[tu.tv]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'tu.tv' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	xbmc.output("9b) Tu.tv sin t�tulo...")
	#<embed src="http://tu.tv/tutvweb.swf?kpt=aHR0cDovL3d3dy50dS50di92aW
	patronvideos  = '<embed src="(http://tu.tv/[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "[tu.tv]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'tu.tv' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Megavideo - V�deos sin t�tulo
	xbmc.output("10 ) Megavideo sin titulo...")
	patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "[Megavideo]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Megavideo - V�deos sin t�tulo
	xbmc.output("11) Megavideo sin titulo...")
	patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "[Megavideo]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# STAGEVU
	'''
	xbmc.output("12) Stagevu...")
	patronvideos  = '(http://stagevu.com[^<]+)<'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Ver el v�deo en Stagevu"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Stagevu' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)
	'''
		
	# Vreel - V�deos sin t�tulo
	xbmc.output("13) Vreel sin titulo...")
	patronvideos  = '(http://beta.vreel.net[^<]+)<'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "[Vreel]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Vreel' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Megavideo - V�deos con t�tulo
	xbmc.output("14) Megavideo con titulo...")
	patronvideos  = '<a href="http://www.megavideo.com/\?v\=([^"]+)".*?>(.*?)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	
	for match in matches:
		titulo = match[1].strip()
		if titulo == "":
			titulo = "[Megavideo]"
		url = match[0]
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	xbmc.output("0) Stagevu...")
	patronvideos  = '"http://stagevu.com.*?uid\=([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	
	for match in matches:
		titulo = "[Stagevu]"
		url = "http://stagevu.com/video/"+match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Stagevu' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	xbmc.output("0) Megavideo... formato d=XXXXXXX")
	patronvideos  = '"http://www.megavideo.com/.*?\&d\=([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	
	for match in matches:
		titulo = "[Megavideo]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	xbmc.output("0) Megaupload... formato megavideo con d=XXXXXXX")
	patronvideos  = '"http://www.megavideo.com/\?d\=([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "[Megavideo]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'Megaupload' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	xbmc.output("0) Movshare...")
	patronvideos  = '"(http://www.movshare.net/video/[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	
	for match in matches:
		titulo = "[Movshare]"
		url = match
		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'movshare' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	xbmc.output("0) Veoh...")
	patronvideos  = '"http://www.veoh.com/veohplayer.swf.*?permalinkId=([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "[Veoh]"
		if match.count("&")>0:
			primera = match.find("&")
			url = match[:primera]
		else:
			url = match

		if url not in encontrados:
			xbmc.output("  url="+url)
			devuelve.append( [ titulo , url , 'veoh' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	return devuelve

def findurl(code,server):
	mediaurl = "ERROR"
	if server == "Megavideo":
		mediaurl = megavideo.Megavideo(code)
		
	if server == "Megaupload":
		mediaurl = megaupload.getvideo(code)
		
	if server == "Wuapi":
		mediaurl = wuapi.Wuapi(code)
		
	if server == "Vreel":
		mediaurl = vreel.Vreel(code)

	if server == "Stagevu":
		mediaurl = stagevu.Stagevu(code)
	
	if server == "tu.tv":
		mediaurl = tutv.Tutv(code)
	
	if server == "movshare":
		mediaurl = movshare.getvideo(code)
	
	if server == "veoh":
		mediaurl = veoh.getvideo(code)
	
	if server == "Directo":
		mediaurl = code
	return mediaurl

def getmegavideolow(code):
	return megavideo.getlowurl(code)

def getmegavideohigh(code):
	return megavideo.gethighurl(code)

def getmegauploadhigh(code):
	return megaupload.gethighurl(code)

def getmegauploadlow(code):
	return megaupload.getlowurl(code)