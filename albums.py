# coding: utf-8
import codecs
import sqlite3
import os
from datetime import datetime
import xml.etree.ElementTree as ET
from sqlite3 import Error

from lib import parse_arguments,debug,trace,warn,error

class Album(object):
    "les infos sur un album"
    def __init__(self, title, musicbrainzalbumid, musicbrainzreleasegroupid, genre, type, artistdesc, label, releasedate):
        self.title = title
        self.musicbrainzalbumid = musicbrainzalbumid
        self.musicbrainzreleasegroupid = musicbrainzreleasegroupid
        self.genre = genre
        self.type = type 
        self.artistdesc = artistdesc
        self.label = label
        self.releasedate = releasedate
        
    def __str__(self):
        return "title:\t\t\t\t{c.title}\nmusicbrainzalbumid:\t\t{c.musicbrainzalbumid}\nmusicbrainzreleasegroupid:\t{c.musicbrainzreleasegroupid}\ngenre:\t\t\t\t{c.genre}\ntype:\t\t\t\t{c.type}\nartistdesc:\t\t\t{c.artistdesc}\nlabel:\t\t\t{c.label}\nreleasedate:\t\t\t{c.releasedate}".format(c=self)

def check(valeur,defaut):
    if valeur == None:
	    return defaut
    else:
	    return valeur.text

def parse_album(node):
    """
       Cette fonction parse un noeud de type "album", comme le suivant :
        <album>
            <title>Greatest Hits, Volume I &amp; Volume II</title>
            <musicbrainzalbumid>8bd9c465-28bb-37e4-bab5-aad725246bd7</musicbrainzalbumid>
            <musicbrainzreleasegroupid>4a8f66b9-2ebf-3ebf-bd5e-ad19386e76c0</musicbrainzreleasegroupid>
            <scrapedmbid>false</scrapedmbid>
            <artistdescartistdesc>Billy Joel</artistdesc>
            <genre>Rock</genre>
            <style>Rock/Pop</style>
            <mood>Happy</mood>
            <mood>Funny</mood>
            <theme>Partying</theme>
            <theme>TGIF</theme>
            <compilation>false</compilation>
            <boxset>false</boxset>
            <review>Billy Joel&apos;s Greatest Hits is a collection released in two sets, 12 years apart. The first set, consisting of two discs, titled Volume I and Volume II, was released in 1985. The second, single disc titled Volume III was released in 1997. All songs but the last three on Volume III, &quot;To Make You Feel My Love&quot;, &quot;Hey Girl&quot; and &quot;Light as the Breeze&quot; were written by Joel. &quot;You&apos;re Only Human (Second Wind)&quot; and &quot;The Night Is Still Young&quot; are only available on the first set. The other songs appear mostly in order of their release dates and generally represent Joel&apos;s most successful singles.</review>
            <type>album / compilation</type>
            <releasestatus>official</releasestatus>
            <releasedate>1985</releasedate>
            <originalreleasedate>1985-07-27</originalreleasedate>
            <label>Columbia</label>
            <duration>3948</duration>
            <thumb spoof="" cache="" aspect="thumb" preview="https://assets.fanart.tv/preview/music/64b94289-9474-4d43-8c93-918ccc1920d1/albumcover/greatest-hits-volume-i--volume-ii-4e80240798fa9.jpg">https://assets.fanart.tv/fanart/music/64b94289-9474-4d43-8c93-918ccc1920d1/albumcover/greatest-hits-volume-i--volume-ii-4e80240798fa9.jpg</thumb>
            <thumb spoof="" cache="" aspect="thumb" preview="http://coverartarchive.org/release/0a77a705-1bd5-4e54-80d1-eee6a8980ce9/7763963170-250.jpg">http://coverartarchive.org/release/0a77a705-1bd5-4e54-80d1-eee6a8980ce9/7763963170.jpg</thumb>
            <path>F:\Music\FLAC\Artist Albums\Billy Joel\Greatest Hits Vol I &amp; II\</path>
            <rating max="10">7.000000</rating>
            <userrating max="10">0</userrating>
            <votes>4</votes>
            <albumArtistCredits>
                <artist>Billy Joel</artist>
                <musicBrainzArtistID>64b94289-9474-4d43-8c93-918ccc1920d1</musicBrainzArtistID>
            </albumArtistCredits>
            <releasetype>album</releasetype>
        </album>
    """
    trace("Function : parse_album")
    title = node.find("title").text
    musicbrainzalbumid = node.find("musicbrainzalbumid").text
    musicbrainzreleasegroupid = node.find("musicbrainzreleasegroupid").text
    genre = check(node.find("genre"),None)
    type = check(node.find("type"),None)
    artistdesc = check(node.find("artistdesc"),None)
    label =  check(node.find("label"), None)
    releasedate = check(node.find("releasedate"), None)
    return Album( title, musicbrainzalbumid, musicbrainzreleasegroupid, genre, type, artistdesc, label, releasedate)
 
def parse_file_album(path):
    trace("Function : parse_file_album")
    debug("parsing de l'album de "+path)
    with codecs.open(path, 'r','utf8') as fichier:
        tree = ET.ElementTree()
        tree.parse (fichier)
        racine = tree.getroot()
        debug("la racine est " +racine.tag)
        #album est la racine donc pas de node!!
        #return [parse_album(node) for node in racine.findall("album")]
        albume = parse_album(racine)
        debug("On vient de parser dans : "+str(type(albume)))
        return albume
		
def Create_Connection(db_file):
    """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn    

def Verification_Album(Nom,Infos):
    trace("Function : Verification_Album")
    info="Verification de l'album : "+Nom+" en base"
    debug(info)
    #creation de la requete
    requete="SELECT idAlbum,strAlbum,strMusicBrainzAlbumID,strArtistDisp FROM album WHERE strMusicBrainzAlbumID = \'"+Infos.musicbrainzalbumid+"\'"
    debug(requete)
    #connexion a la base
    base=C_PathBase+"MyMusic82.db"
    conn = Create_Connection(base)
    with conn:
        #execution de la requete
        cur = conn.cursor()
        cur.execute(requete)
        #recuperation des donnees
        rows = cur.fetchall()
        nb_Id=len(rows)
        debug("renvoie"+str(nb_Id))
        if nb_Id != 0:
            print("%-10s %-25s %-38s %-25s" %("idAlbum","strAlbum","MusicBrainzAlbumID","ArtistDisp"))
            for row in rows:
                print("%-10s %-25s %-38s %-25s" %(row[0], row[1], row[2], row[3]))
            Verif_Album_Artist(row[0],row[3],Nom,conn)
        else:
            warn("Problème d'ID / Nom pour l'album " +Nom)
            requete="SELECT idAlbum,strAlbum,strMusicBrainzAlbumID,strArtistDisp FROM album WHERE strAlbum =\'"+Nom+"\'"
            debug(requete)
            cur.execute(requete)
			#recuperation des donnees
            rows = cur.fetchall()
            nb_Str=len(rows)
            debug("renvoie"+str(nb_Str))
            if nb_Str != 0:
                print("%-10s %-25s %-38s %-25s" %("idAlbum","strAlbum","MusicBrainzAlbumID","ArtistDisp"))
                for row in rows:
                    print("%-10s %-25s %-38s %-25s" %(row[0], row[1], row[2], row[3]))
                Maj_MusicBrainzAlbumID(row[2],Infos.musicbrainzalbumid,conn)
                Verif_Album_Artist(row[0],row[3],Nom,conn)
        if nb_Id == 0 and nb_Str == 0:
            warn("Pas d'album avec musicbrainzalbumid et avec strAlbum!!")
            warn("Il faut sans doute purger et metre à jour via KOFDI")
        if Infos.genre != None:
            Verif_Genre(Nom,Infos,conn)
            Verif_Song(Nom,Infos,conn)
        else:
            warn("Pas de genre donc pas de vérification!")
        Purge_Infos(Nom,Infos,conn)
        Purge_Genre(conn)
        #fermeture connexion
    conn.close()

def Verif_Genre(nom, Infos,connexion):
    trace("Function : Verif_Genre")
    requete ="SELECT idGenre FROM genre WHERE strGenre = \'" + Infos.genre + "\'"
    debug(requete)
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)
        row = cur.fetchone()
        if row is None:
            debug("pas de trace du genre en base : " +Infos.genre)
            print("Voulez-vous l'ajouter quand même?")
            reponse=input("Oui/Non")
            if reponse[0].upper() == "O":
                #ajout du nouveau genre dans la table des genres
                Ajoute_Genre(nom,Infos,connexion)
                #ajout du genre pour l'artist
                Maj_Genre(nom,Infos,connexion)
        else:
            debug(Infos.genre+" est bien présent donc MAJ")
            Maj_Genre(nom,Infos,connexion)
        
def Maj_Genre(nom,Infos,connexion):
    trace("Function : Maj Genre")
    requete="UPDATE album SET strGenres = \'" + Infos.genre + "\' WHERE strMusicBrainzAlbumID = \'" + Infos.musicbrainzalbumid + "\'"
    debug(requete)
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)

def Maj_MusicBrainzAlbumID(Ancien,Nouveau,connexion):
    "Change le musicbrainzalbumid en base pour celui  du fichier NFO"
    debug("Function : Maj_MusicBrainzAlbumID")
    requete = "UPDATE album set strMusicBrainzAlbumID =\'" + Nouveau + "\' WHERE strMusicBrainzAlbumID = \'" + Ancien +"\'"
    debug(requete)
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)
	
def Ajoute_Genre(nom,Infos,connexion):
    "Ajout d'un nouveau genre dans la table des genres"
    trace("Function : Ajoute Genre")
    with connexion:
        cur = connexion.cursor()
        max=Max_Table("genre","idGenre",connexion)
        debug("le max (table GENRE) est "+max)
        nouveau=max+1
        ajoute="INSERT INTO genre (idGenre, strGenre) VALUES ( \'" + str(nouveau) + "\' , \'" + Infos.genre + "\')"
        debug(ajoute)
        cur.execute(ajoute)

def Verif_Album_Artist(Id,Liste,nom,connexion):
    trace("Function : Verif_Album_Artist")
    args = parse_arguments()
    requete="SELECT idArtist,idAlbum,iOrder,strArtist FROM album_artist WHERE idAlbum = \'"+str(Id)+"\' "
    debug(requete)
    #on decoupe la liste pour avoir le nombre d'artist associé
    artists=Liste.split(" / ")
    associe=len(artists)
    #for art in artists:
    #    print("artist : " +art)
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)
        rows = cur.fetchall()
        nb=len(rows) 
        if nb == associe :
            trace("il y a les "+str(nb)+" artists associés")
            if args.Debug:
                debug(" data1 : artist album ordre nom")
                for row in rows:
                    debug(" data1 :" +str(row))
        else:
            warn("Il manque des artists")
            if args.Debug:
                debug(" data2 : artist album ordre nom")
                for row in rows:
                    debug(" data2 :" +str(row))
            Ajoute_Artist(Id,Liste,nom,rows,connexion)
			#on ajoute les infos dans la table album_source
            Ajoute_Source(Id,connexion)

def Ajoute_Artist(Id,Liste,nom,rows,connexion):
    trace("Function : Ajoute_Artist")
    debug("Mise à jour des artistes de l'album "+nom)
    debug("liste des artists à vérifier : " +str(Liste))
    #on decoupe la liste pour avoir le nombre d'artist associé
    artists=Liste.split(" / ")
    debug("Les artistes : "+str(artists))
    #pour le N° d'ordre dans la liste
    Ordre=0
    IdAlbum=Id
    for art in artists:
        debug("Recup infos pour : "+str(art))
        debug("il y a "+str(len(rows))+" album")
        if int(len(rows)) == 0:
            for row in rows:
                debug("traitement des albums "+str(row))
                #on recupere les infos (id) pour l'insertion ultérieure
                IdAlbum=row[1]
                debug("L'idArtist : " +IdArtist)
                #on recupere le max du l'ordre
                if row[2] > Ordre:
                    Ordre=row[2]
                debug("verification de "+art+" avec " +str(row[3]))
                if row[3] == art:
                    trace("l'artiste "+art+" est présent")
                    #on le supprime de la liste => la liste finale ne contiendra que ceux qui manquent!!!
                    artists.remove(art)
                else:
                    debug("RIEN")
        else:
            debug("l'IdAlbum = "+str(Id))
            IdAlbum=Id
    #on affiche la liste finale : donc les manquants            
    warn("il manque l(es)'artiste(s) en base " +str(artists))
    with connexion:
        cur = connexion.cursor()
        for art in artists:
            debug("recupération des identifiants de "+art+" en base")
            requete="SELECT idArtist FROM artist WHERE strArtist = \'" + art +"\'"
            debug(requete)
            cur.execute(requete)
            row = cur.fetchone()
            num=str(row).split(",")[0].split("(")[1]
            Ordre=int(Ordre+1)
            requete="INSERT INTO album_artist (idArtist,idAlbum,iOrder,strArtist) VALUES ("+str(num)+" , "+str(IdAlbum)+" ,"+str(Ordre)+", \'"+art+"\' )"
            debug(requete)
            cur.execute(requete)
        connexion.commit()

def traitement_Album(nom,chemin):
    trace("Function : traitement_Album")
    info="Traitement de l'album :"+chemin
    args = parse_arguments()
    debug(info)
    NomComplet=chemin+"\\album.nfo"
    trace("Verification Album : "+NomComplet)
    album = parse_file_album(NomComplet)
    debug("fin de lecture")
    if args.Debug:
        print(album)
    Verification_Album(nom,album)
 
def Maj_Scraped(ID,connexion):
    trace("Function : Maj_Scraped")
    Date = datetime.now()
    date_time = Date.strftime("%Y-%m-%d, %H:%M:%S")
    requete = "UPDATE artist SET lastScraped = \'" + date_time + "\' WHERE strMusicBrainzArtistID = \'"+ID+"\'"
    debug(requete)
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)
    
def Purge_Infos(nom,Infos,connexion):
    "suppression des informations inutiles : InfoSetting Images Rating Vote UserRating"
    trace("Function : Purge_Infos")
    vide="NULL"
    reqmood="UPDATE album set strMoods = NULL WHERE strMusicBrainzAlbumID = \'" + Infos.musicbrainzalbumid + "\'"
    debug(reqmood)
    reqsty="UPDATE album set strStyles = NULL WHERE strMusicBrainzAlbumID = \'" + Infos.musicbrainzalbumid + "\'"
    debug(reqsty)
    reqthe="UPDATE album set strThemes = NULL WHERE strMusicBrainzAlbumID = \'" + Infos.musicbrainzalbumid + "\'"
    debug(reqthe)
    reqima="UPDATE album set strImage = NULL WHERE strMusicBrainzAlbumID = \'" + Infos.musicbrainzalbumid + "\'"
    debug(reqima)
    reqrat="UPDATE album set fRating = 0.0 WHERE strMusicBrainzAlbumID = \'" + Infos.musicbrainzalbumid + "\'"
    debug(reqrat)
    reqvot="UPDATE album set iVotes = 0 WHERE strMusicBrainzAlbumID = \'" + Infos.musicbrainzalbumid + "\'"
    debug(reqvot)
    requser="UPDATE album set iUserRating = 0 WHERE strMusicBrainzAlbumID = \'" + Infos.musicbrainzalbumid + "\'"
    debug(requser)
    with connexion:
        cur = connexion.cursor()
        cur.execute(reqmood)
        cur.execute(reqsty)
        cur.execute(reqthe)
        cur.execute(reqima)
        cur.execute(reqrat)
        cur.execute(reqvot)
        cur.execute(requser)

def Ajoute_Source(Id,connexion):
    trace("Function : Ajoute_Trace")
    requete="INSERT INTO album_source VALUES (1," + str(Id) + ")"
    debug(requete)
    with connexion:
        cur=connexion.cursor()
        cur.execute(requete)

def Max_Table(Table,Col,Connexion):
   trace("Function :  Max_Table")
   requete = "SELECT MAX(" + Col + ") FROM " + Table
   debug(requete)
   with Connexion:
        cur = Connexion.cursor()
        try:
            cur.execute(requete)
        except Error as e:
            error(e)
        else:
            row = cur.fetchone()
            max=str(row).split(",")[0].split("(")[1]
            debug("le max (table " + Table + ") est "+max)
            return int(max)

def Verif_Song(Nom,Infos,connexion):
    trace ("Function ; Verif_Song")
    #Nom est le nom du répertoire donc de l'album
    requete = "SELECT idAlbum FROM album WHERE strAlbum = \'" + Nom + "\'"
    debug(requete)
    with connexion:
        cur= connexion.cursor()
        cur.execute(requete)
        row= cur.fetchone()
        idAlbum=str(row).split(",")[0].split("(")[1]
        print(idAlbum)
        reqrat="UPDATE song SET rating = 0.0 WHERE idAlbum = \'" + idAlbum + "\'"
        debug(reqrat)
        reqvot="UPDATE song SET votes = 0 WHERE idAlbum = \'" + idAlbum + "\'"
        debug(reqvot)
        requser="UPDATE song SET userrating = 0 WHERE idAlbum = \'" + idAlbum + "\'"
        debug(requser)
        reqcom="UPDATE song SET comment = \'\' WHERE idAlbum = \'" + idAlbum + "\'"
        debug(reqcom)
        reqmoo="UPDATE song SET mood = \'\' WHERE idAlbum = \'" + idAlbum + "\'"
        debug(reqmoo)
        cur.execute(reqrat)
        cur.execute(reqvot)
        cur.execute(requser)
        cur.execute(reqmoo)
        cur.execute(reqcom)
        reqgen="UPDATE song SET strGenres= \'" + Infos.genre + "\' WHERE idAlbum = \'" + idAlbum + "\'"
        debug(reqgen)
        cur.execute(reqgen)
        reqid="SELECT idGenre FROM genre WHERE strGenre = \'" + Infos.genre + "\'"
        debug(reqid)
        cur.execute(reqid)
        row= cur.fetchone()
        idGenre=str(row).split(",")[0].split("(")[1]
        print(idGenre)
        requni="DELETE FROM song_genre WHERE idSong IN ( SELECT idSong FROM song  WHERE idAlbum = " + idAlbum + ") AND iOrder > 0"
        debug(requni)
        cur.execute(requni)
        #verification si MAJ ou Insertion
        reqverif = "SELECT idGenre FROM song_genre WHERE idSong in ( SELECT idSong FROM song WHERE idAlbum = " + idAlbum + ")"
        debug(reqverif)
        cur.execute(reqverif)
        rows= cur.fetchall()
        if len(rows) > 0:
            trace("MAJ de song_genre")
            reqgen2="UPDATE song_genre SET idGenre = " + idGenre + " WHERE idSong IN ( SELECT idSong FROM song  WHERE idAlbum = " + idAlbum + ")"
            debug(reqgen2)
            cur.execute(reqgen2)
        else:
            trace("Insertion dans song_genre")
            requete = "SELECT idSong FROM song  WHERE idAlbum = " + idAlbum
            debug(requete)
            cur.execute(requete)
            rows=cur.fetchall()
            for row in rows:
                reqgen2="INSERT INTO song_genre (idSong, idGenre, iOrder) VALUES ( " + str(row[0]) + "," + str(idGenre) + ",0)"
                debug(reqgen2)
                cur.execute(reqgen2)
        
        
def Purge_Genre(connexion):
    "supprime de la table genre un genre qui n'est pas utilisé dans artist, album , song et song_genre"
    trace("Function : Purge_Genre")  
    requete="SELECT idGenre,strGenre FROM GENRE"
    debug(requete)
    with connexion:
        cur =  connexion.cursor()
        cur.execute(requete)
        rows= cur.fetchall()
        for row in rows:
           trace("Verification de " + str(row[0]) + " (" +row[1] +")")
           reqart="SELECT COUNT(*) FROM artist WHERE strGenres = \'" + row[1] + "\'"
           cur.execute(reqart)
           nb = cur.fetchone()
           nb_artist = str(nb).split(",")[0].split("(")[1]
           reqalb="SELECT COUNT(*) FROM album WHERE strGenres = \'" + row[1] + "\'"
           cur.execute(reqalb)
           nb = cur.fetchone()
           nb_album = str(nb).split(",")[0].split("(")[1]
           reqson="SELECT COUNT(*) FROM song WHERE strGenres = \'" + row[1] + "\'"
           cur.execute(reqson)
           nb = cur.fetchone()
           nb_song = str(nb).split(",")[0].split("(")[1]
           debug("il y a " + nb_artist + " et " +  nb_album + " et " + nb_song + " pour ce GENRE")
           if int(nb_artist) == 0 and int(nb_album) == 0 and int(nb_song) == 0 :
              trace("le gendre "+ row[1] + " n'est pas utilisé donc suppression!")
              requete= "DELETE FROM genre WHERE idGenre = " + str(row[0])
              debug(requete)
              cur.execute(requete)

    
    
# portable
#C_PathBase = "C:\\Users\\ungvar\\AppData\\Roaming\\Kodi\\userdata\\Database\\"
# maison
#C_PathBase = "C:\\Users\\dom\\AppData\\Roaming\\Kodi\\userdata\\Database\\"
#C_Image="D:\\Torrents\\Test_Kodi\\"
#MAJ REELLE 
C_PathBase = "C:\\Users\\dom\\AppData\\Roaming\\Kodi\\userdata\\Database\\"
C_Image="smb:\/\/OSMC\/Musiques"