# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# XBMC Tools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# 2010/02/13 A�adida funcionalidad de Biblioteca - JUR
#------------------------------------------------------------

import urllib
import xbmc
import xbmcgui
import xbmcplugin
import sys
import servertools
import downloadtools
import os
import favoritos
import library
import descargadoslist

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

#IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' ) )
DEBUG = True
 
def get_system_platform():
	""" fonction: pour recuperer la platform que xbmc tourne """
	platform = "unknown"
	if xbmc.getCondVisibility( "system.platform.linux" ):
		platform = "linux"
	elif xbmc.getCondVisibility( "system.platform.xbox" ):
		platform = "xbox"
	elif xbmc.getCondVisibility( "system.platform.windows" ):
		platform = "windows"
	elif xbmc.getCondVisibility( "system.platform.osx" ):
		platform = "osx"
	return platform

def addnewfolder( canal , accion , category , title , url , thumbnail , plot , Serie="",totalItems=0):
	addnewfolderextra( canal , accion , category , title , url , thumbnail , plot , "" ,Serie,totalItems)

def addnewfolderextra( canal , accion , category , title , url , thumbnail , plot , extradata ,Serie="",totalItems=0):
	#xbmc.output("pluginhandle=%d" % pluginhandle)
	try:
		xbmc.output('[xbmctools.py] addnewfolder( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")" , "'+Serie+'")"')
	except:
		xbmc.output('[xbmctools.py] addnewfolder(<unicode>)')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot, "Studio" : canal } )
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&extradata=%s&Serie=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( extradata ) , Serie)
	#xbmc.output("[xbmctools.py] itemurl=%s" % itemurl)
	if totalItems == 0:
		xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)
	else:
		xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True, totalItems=totalItems)

def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ,Serie=""):
	try:
		xbmc.output('[xbmctools.py] addnewvideo( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+server+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")" , "'+Serie+'")"')
	except:
		xbmc.output('[xbmctools.py] addnewvideo(<unicode>)')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot, "Studio" : canal } )
	#listitem.setProperty('fanart_image',os.path.join(IMAGES_PATH, "cinetube.png"))
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s&Serie=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server , Serie)
	#xbmc.output("[xbmctools.py] itemurl=%s" % itemurl)
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def addthumbnailfolder( canal , scrapedtitle , scrapedurl , scrapedthumbnail , accion ):
	xbmc.output('[xbmctools.py] addthumbnailfolder( "'+scrapedtitle+'" , "' + scrapedurl + '" , "'+scrapedthumbnail+'" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
	itemurl = '%s?channel=%s&action=%s&category=%s&url=%s&title=%s&thumbnail=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedurl ) , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedthumbnail ) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addfolder( canal , nombre , url , accion ):
	xbmc.output('[xbmctools.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
	itemurl = '%s?channel=%s&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus(nombre) , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addvideo( canal , nombre , url , category , server , Serie=""):
	xbmc.output('[xbmctools.py] addvideo( "'+nombre+'" , "' + url + '" , "'+server+ '" , "'+Serie+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : nombre } )
	itemurl = '%s?channel=%s&action=play&category=%s&url=%s&server=%s&title=%s&Serie=%s' % ( sys.argv[ 0 ] , canal , category , urllib.quote_plus(url) , server , urllib.quote_plus( nombre ) , Serie)
	xbmcplugin.addDirectoryItem( handle=pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def playvideo(canal,server,url,category,title,thumbnail,plot,strmfile=False,Serie=""):
	playvideoEx(canal,server,url,category,title,thumbnail,plot,False,False,strmfile,Serie)

def playvideo2(canal,server,url,category,title,thumbnail,plot):
	playvideoEx(canal,server,url,category,title,thumbnail,plot,True,False)

def playvideo3(canal,server,url,category,title,thumbnail,plot):
	playvideoEx(canal,server,url,category,title,thumbnail,plot,False,True)

def playvideoEx(canal,server,url,category,title,thumbnail,plot,desdefavoritos,desdedescargados,strmfile=False,Serie=""):
	
	xbmc.output("[xbmctools.py] playvideo")
	xbmc.output("[xbmctools.py] playvideo canal="+canal)
	xbmc.output("[xbmctools.py] playvideo server="+server)
	xbmc.output("[xbmctools.py] playvideo url="+url)
	xbmc.output("[xbmctools.py] playvideo category="+category)
	xbmc.output("[xbmctools.py] playvideo serie="+Serie)
	
	# Abre el di�logo de selecci�n
	opciones = []

	# Los v�deos de Megav�deo s�lo se pueden ver en calidad alta con cuenta premium
	# Los v�deos de Megaupload s�lo se pueden ver con cuenta premium, en otro caso pide captcha
	if (server=="Megavideo" or server=="Megaupload") and xbmcplugin.getSetting("megavideopremium")=="true":
		opciones.append("Ver en calidad alta ["+server+"]")
		# Si la accion por defecto es "Ver en calidad alta", la seleccion se hace ya
		if xbmcplugin.getSetting("default_action")=="2":
			seleccion = len(opciones)-1

	# Los v�deos de Megav�deo o Megaupload se pueden ver en calidad baja sin cuenta premium, aunque con el l�mite
	if (server=="Megavideo" or server=="Megaupload"):
		opciones.append("Ver en calidad baja [Megavideo]")
		# Si la accion por defecto es "Ver en calidad baja", la seleccion se hace ya
		if xbmcplugin.getSetting("default_action")=="1":
			seleccion = len(opciones)-1
	else:
		opciones.append("Ver ["+server+"]")
		# Si la accion por defecto es "Ver en calidad baja", la seleccion se hace ya
		if xbmcplugin.getSetting("default_action")=="1":
			seleccion = len(opciones)-1

	opciones.append("Descargar")

	if desdefavoritos: 
		opciones.append("Quitar de favoritos")
	else:
		opciones.append("A�adir a favoritos")

	if desdedescargados:
		opciones.append("Quitar de lista de descargas")
	else:
		opciones.append("A�adir a lista de descargas")

	if not strmfile: #JUR: Temp-Modo desarrollo. Abierto a todos los canales
		opciones.append("A�adir a Biblioteca")

	# Busqueda de trailers en youtube	
	if not canal in ["Trailer","ecarteleratrailers"]:
		opciones.append("Buscar Trailer")

	# Si la accion por defecto es "Preguntar", pregunta
	if xbmcplugin.getSetting("default_action")=="0":
		dia = xbmcgui.Dialog()
		seleccion = dia.select("Elige una opci�n", opciones)
		#dia.close()
	xbmc.output("seleccion=%d" % seleccion)
	xbmc.output("seleccion=%s" % opciones[seleccion])

	# No ha elegido nada, lo m�s probable porque haya dado al ESC 
	if seleccion==-1:
		if strmfile:  #Para evitar el error "Uno o m�s elementos fallaron" al cancelar la selecci�n desde fichero strm
			listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail, path="")    # JUR Modified
			xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),False,listitem)    # JUR Added
		return
	# Ver en calidad alta
	if opciones[seleccion].startswith("Ver en calidad alta"):
		if server=="Megaupload":
			mediaurl = servertools.getmegauploadhigh(url)
		else:
			mediaurl = servertools.getmegavideohigh(url)
	# Ver (calidad baja megavideo o resto servidores)
	elif opciones[seleccion].startswith("Ver"):
		if server=="Megaupload":
			mediaurl = servertools.getmegauploadlow(url)
		elif server=="Megavideo":
			if xbmcplugin.getSetting("megavideopremium")=="false":
				advertencia = xbmcgui.Dialog()
				resultado = advertencia.ok('Megavideo tiene un l�mite de reproducci�n de 72 minutos' , 'Para evitar que los v�deos se corten pasado ese tiempo' , 'necesitas una cuenta Premium')			
			mediaurl = servertools.getmegavideolow(url)
		else:
			mediaurl = servertools.findurl(url,server)

	# Descargar
	elif opciones[seleccion]=="Descargar":
		if server=="Megaupload":
			if xbmcplugin.getSetting("megavideopremium")=="false":
				mediaurl = servertools.getmegauploadlow(url)
			else:
				mediaurl = servertools.getmegauploadhigh(url)
		elif server=="Megavideo":
			if xbmcplugin.getSetting("megavideopremium")=="false":
				mediaurl = servertools.getmegavideolow(url)
			else:
				mediaurl = servertools.getmegavideohigh(url)
		else:
			mediaurl = servertools.findurl(url,server)

		keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			title = keyboard.getText()
			downloadtools.downloadtitle(mediaurl,title)
		return

	elif opciones[seleccion]=="Quitar de favoritos":
		# La categor�a es el nombre del fichero en favoritos
		os.remove(urllib.unquote_plus( category ))
		advertencia = xbmcgui.Dialog()
		resultado = advertencia.ok('V�deo quitado de favoritos' , title , 'Se ha quitado de favoritos')
		return

	elif opciones[seleccion]=="A�adir a favoritos":
		keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
		keyboard.doModal()
		if keyboard.isConfirmed():
			title = keyboard.getText()
			favoritos.savebookmark(title,url,thumbnail,server,plot)
			advertencia = xbmcgui.Dialog()
			resultado = advertencia.ok('Nuevo v�deo en favoritos' , title , 'se ha a�adido a favoritos')
		return

	elif opciones[seleccion]=="Quitar de lista de descargas":
		# La categor�a es el nombre del fichero en la lista de descargas
		os.remove(urllib.unquote_plus( category ))
		advertencia = xbmcgui.Dialog()
		resultado = advertencia.ok('V�deo quitado de lista de descargas' , title , 'Se ha quitado de lista de descargas')
		return

	elif opciones[seleccion]=="A�adir a lista de descargas":
		keyboard = xbmc.Keyboard(downloadtools.limpia_nombre_excepto_1(title))
		keyboard.doModal()
		if keyboard.isConfirmed():
			title = keyboard.getText()
			descargadoslist.savebookmark(title,url,thumbnail,server,plot)
			advertencia = xbmcgui.Dialog()
			resultado = advertencia.ok('Nuevo v�deo en lista de descargas' , title , 'se ha a�adido a la lista de descargas')
		return

	elif opciones[seleccion]=="A�adir a Biblioteca":  # Library
		library.savelibrary(title,url,thumbnail,server,plot,canal=canal,category=category,Serie=Serie)
		return

	elif opciones[seleccion]=="Buscar Trailer":
		xbmc.executebuiltin("Container.Update(%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s)" % ( sys.argv[ 0 ] , "trailertools" , "buscartrailer" , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( "" ) , server ))
		return

	# Si no hay mediaurl es porque el v�deo no est� :)
	xbmc.output("[xbmctools.py] mediaurl="+mediaurl)
	if mediaurl=="":
		alertnodisponibleserver(server)
		return

	# Obtenci�n datos de la Biblioteca (solo strms que est�n en la biblioteca)
	if strmfile:
		title,thumbnail,canal,plot = getMediaInfo (title,thumbnail,canal,plot,Serie)
		
	# Crea un listitem para pas�rselo al reproductor
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail, path=mediaurl)
	listitem.setInfo( "video", { "Title": title, "Plot" : plot , "Studio" : canal , "Genre" : category } )
#	listitem.setProperty('isPlayable', 'True')
	# Lanza el reproductor
	if strmfile: #Si es un fichero strm no hace falta el play
		xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),True,listitem)
	else:
		launchplayer(mediaurl, listitem)


def getMediaInfo (title,thumbnail,studio,plot,serie):
	'''Obtiene informaci�n de la Biblioteca si existe (ficheros strm) o de los par�metros
	'''
	xbmc.output('[xbmctools.py] playlist OBTENCI�N DE DATOS DE BIBLIOTECA')
	# Miniatura
	libthumbnail =xbmc.getInfoImage( "ListItem.Thumb" )
	if libthumbnail == "":
		xbmc.output('[xbmctools.py] playlist THUMBNAIL: xbmc.getInfoImage( "ListItem.Thumb" ) vacio')
	else:
		thumbnail = libthumbnail
		xbmc.output('[xbmctools.py] THUMBNAIL xbmc.getInfoImage( "ListItem.Thumb" ) = ' + libthumbnail)
	if serie == "":
		studio = studio + ' (streaming)'
	else:
		studio = serie
		
	return title,thumbnail,studio,plot

# Lanza el reproductor
def launchplayer(mediaurl, listitem):

	# A�adimos el listitem a una lista de reproducci�n (playlist)
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()
	playlist.add( mediaurl, listitem )

	# Reproduce
	playersettings = xbmcplugin.getSetting('player_type')
	xbmc.output("[xbmctools.py] playersettings="+playersettings)

	player_type = xbmc.PLAYER_CORE_AUTO
	if playersettings == "0":
		player_type = xbmc.PLAYER_CORE_AUTO
		xbmc.output("[xbmctools.py] PLAYER_CORE_AUTO")
	elif playersettings == "1":
		player_type = xbmc.PLAYER_CORE_MPLAYER
		xbmc.output("[xbmctools.py] PLAYER_CORE_MPLAYER")
	elif playersettings == "2":
		player_type = xbmc.PLAYER_CORE_DVDPLAYER
		xbmc.output("[xbmctools.py] PLAYER_CORE_DVDPLAYER")

		xbmcPlayer = xbmc.Player( player_type )
		xbmcPlayer.play(playlist)

def logdebuginfo(DEBUG,scrapedtitle,scrapedurl,scrapedthumbnail,scrapedplot):
	if (DEBUG):
		xbmc.output("[xmbctools.py] scrapedtitle="+scrapedtitle)
		xbmc.output("[xmbctools.py] scrapedurl="+scrapedurl)
		xbmc.output("[xmbctools.py] scrapedthumbnail="+scrapedthumbnail)
		xbmc.output("[xmbctools.py] scrapedplot="+scrapedplot)

def alertnodisponible():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('V�deo no disponible' , 'El v�deo ya no est� disponible en la p�gina,' , 'o no se ha podido localizar el enlace')

def alertnodisponibleserver(server):
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('V�deo borrado' , 'El v�deo ya no est� en '+server , 'Prueba con otro distinto')

def alerterrorpagina():
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.ok('Error en la p�gina' , 'No se puede acceder' , 'por un error en la p�gina')

def unseo(cadena):
	if cadena.upper().startswith("VER GRATIS LA PELICULA "):
		cadena = cadena[23:]
	elif cadena.upper().startswith("VER GRATIS PELICULA "):
		cadena = cadena[20:]
	elif cadena.upper().startswith("VER ONLINE LA PELICULA "):
		cadena = cadena[23:]
	elif cadena.upper().startswith("VER GRATIS "):
		cadena = cadena[11:]
	elif cadena.upper().startswith("VER ONLINE "):
		cadena = cadena[11:]
	return cadena

def addSingleChannelOptions(params,url,category):
	addnewfolder( "configuracion" , "mainlist" , "configuracion" , "Configuracion" , "" , "" , "" )
	addnewfolder( "descargados"   , "mainlist" , "descargados"   , "Descargas"     , "" , "" , "" )
	addnewfolder( "favoritos"     , "mainlist" , "favoritos"     , "Favoritos"     , "" , "" , "" )

# A�ADIDO POR JUR. SOPORTE DE FICHEROS STRM
def playstrm(params,url,category):
	'''Play para videos en ficheros strm
	'''
	xbmc.output("[xbmctools.py] playstrm url="+url)

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	if (params.has_key("Serie")):
		serie = params.get("Serie")
	else:
		serie = ""
	
	playvideo("Biblioteca pelisalacarta",server,url,category,title,thumbnail,plot,strmfile=True,Serie=serie)
