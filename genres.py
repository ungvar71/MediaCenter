# coding: utf-8
import codecs
import sqlite3
import os
from datetime import datetime
import xml.etree.ElementTree as ET
from sqlite3 import Error

from lib import parse_arguments,debug,trace,warn,error


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
        error(e)

    return conn    

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


def traitement_Genre(nom,chemin):
    trace("Function : traitement_Genre")
    info="Traitement des genres :"+chemin 
    trace(info)
    args = parse_arguments()
    #fichier ecrasé par le nouveau contenu
    out=open(chemin+"\\"+nom,"w")
    #connexion a la base
    base=C_PathBase+"MyMusic82.db"
    connexion = Create_Connection(base)
    requete="SELECT idGenre,strGenre FROM genre"
    debug(requete)
    with connexion:
        cur =  connexion.cursor()
        cur.execute(requete)
        rows= cur.fetchall()
        trace("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        Ecrit("Liste des genres",out)
        for row in rows:
           Ecrit("Genre id " + str(row[0]) + " : " +row[1] ,out)
        trace("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        Ecrit("+                       ARTISTES                               +",out)
        trace("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        reqart="SELECT idArtist, strArtist, strgenres FROM artist WHERE strGenres NOT IN (SELECT strGenre FROM genre)"
        debug(reqart)
        cur.execute(reqart)
        arts=cur.fetchall()
        for art in arts:
            Ecrit("L'artiste " + art[1] + "( " +str(art[0])+ ") n'a pas de Genre connu ("+art[2]+")!",out)
        trace("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        Ecrit("+                         ALBUMS                               +",out)
        trace("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        reqalb="SELECT idAlbum, strAlbum, strGenres FROM album WHERE strGenres NOT IN (SELECT strGenre FROM genre)"
        debug(reqalb)
        cur.execute(reqalb)
        albs=cur.fetchall()
        for alb in albs:
            Ecrit("L'album " + alb[1] + "( " +str(alb[0])+ ") n'a pas de Genre connu ("+alb[2]+")!",out)
        trace("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        Ecrit("+                          SONGS                               +",out)
        trace("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        reqsong="SELECT idSong, strTitle, strGenres FROM song WHERE strGenres NOT IN (SELECT strGenre FROM genre)"
        debug(reqsong)
        cur.execute(reqsong)
        songs=cur.fetchall()
        for song in songs:
            Ecrit("La chanson " + song[1] + "( " +str(song[0])+ ") n'a pas de Genre connu ("+song[2]+")!",out)
        if args.Force:
            #mise a jour des songs strGenres d'apres la liaison song_genre
            requete = "SELECT idSong FROM song"
            debug(requete)
            cur.execute(requete)
            rows=cur.fetchall()
            for row in rows:
                reqgenre = "SELECT g.strGenre  FROM genre g ,song_genre sg WHERE g.idGenre = sg.idGenre and sg.idSong = " + str(row[0])
                debug (reqgenre)
                cur.execute(reqgenre)
                songs=cur.fetchall()
                for song in songs:
                    print("strGenre : " +song[0])
                    reqmaj="UPDATE song SET strGenres = \'" + song[0] +"\' where idSong = " + str(row[0])
                    debug(reqmaj)
                    cur.execute(reqmaj)
    connexion.commit()
    out.close()
	
def Renum_Artist(nom,chemin):
    "renumerote les artistes à partir de 2"
    trace("Function : Renum_Artist")
    requete = "SELECT COUNT(*) FROM artist"
    debug(requete)
    base=C_PathBase+"MyMusic82.db"
    connexion = Create_Connection(base)
    with connexion:
        cur =  connexion.cursor()
        cur.execute(requete)
        row= cur.fetchone()
        trace(" il y a " + str(row[0]) + " artistes en base")
        i=4
        while i <= int(row[0]):
            print("I : "+str(i))
            reqmin= "SELECT MIN(idArtist),strArtist FROM artist where idArtist > " +str(i)
            debug(reqmin)
            cur.execute(reqmin)
            indice=cur.fetchone()
            trace(" le min correspond à " + str(indice[0]) + " qui est : " + indice[1])
            reqmaj="UPDATE artist SET idArtist = " +str(i) + " WHERE idArtist = " +str(indice[0])
            debug(reqmaj)
            cur.execute(reqmaj)
            reqalb= "UPDATE album_artist SET idArtist = " + str(i) + " , strArtist = \"" + indice[1] + "\" WHERE idArtist = " +str(indice[0])
            debug(reqalb)
            cur.execute(reqalb)
            reqart="UPDATE art SET media_id = " +str(i) + " WHERE media_id = " +str(indice[0]) + " AND media_type = \'artist\'"
            debug(reqart)
            cur.execute(reqart)
            reqdis="UPDATE discography SET idArtist = " +str(i) + " WHERE idArtist = " +str(indice[0])
            debug(reqdis)
            cur.execute(reqdis)
            reqsong="UPDATE song_artist SET idArtist = " +str(i) + " , strArtist = \"" + indice[1] + "\" WHERE idArtist = " +str(indice[0])
            debug(reqsong)
            cur.execute(reqsong)
            i = i + 1

    
def Ecrit(Chaine,fichier):
    "ecrit la chaine dans un fichier et dans les logs"
    trace(Chaine)
    ligne=Chaine = "\n"
    fichier.write(ligne)

# portable
#C_PathBase = "C:\\Users\\ungvar\\AppData\\Roaming\\Kodi\\userdata\\Database\\"
# maison
#C_PathBase = "C:\\Users\\dom\\AppData\\Roaming\\Kodi\\userdata\\Database\\"
C_Image="D:\\Torrents\\Test_Kodi\\"

#test
#C_PathBase = "C:\\Users\\dom\\Desktop\\"
C_PathBase="D:\\Torrents\\Test_Kodi\\Scripts\\"