# coding: utf-8
import codecs
import sqlite3
import os
from datetime import datetime
import xml.etree.ElementTree as ET
from sqlite3 import Error
from pathlib import Path
from lib import parse_arguments,debug,trace,warn,error
   
class Artist(object):
    "les infos sur un artist"
    def __init__(self,musicBrainzArtistID,name,type,biography,born,died,formed,disbanded,genre,sortname,album=[]):
        self.musicBrainzArtistID = musicBrainzArtistID
        self.name = name
        self.type = type
        self.biography = biography
        self.born = born
        self.died = died
        self.formed = formed
        self.disbanded = disbanded
        self.genre = genre
        self.sortname = sortname
        self.album = album
     
    def __str__(self):
        s = "musicBrainzArtistID:\t{a.musicBrainzArtistID}\nname:\t\t\t{a.name}\nsortname:\t\t{a.sortname}\ntype:\t\t\t{a.type}\nbiography:\t\t{a.biography}\nborn:\t\t\t{a.born}\ndied:\t\t\t{a.died}\nformed:\t\t\t{a.formed}\ndisbanded:\t\t{a.disbanded} \ngenre:\t\t\t{a.genre}".format(a=self)
        s += "\nalbum: "
        for alb in self.album:
            s += "\n{0}".format(alb)
        return s

class Album(object):
    "la liste des albums d'un artist"
    def __init__(self, title, year):
        self.title = title
        self.year = year
        
    def __str__(self):
        return "\ttitle: {d.title}\n\tyear: {d.year}\n".format(d=self)

def parse_album(node):
    """
        <album>
                <title>Captain Morgan&amp;#39;s Revenge</title>
                <year></year>
        </album>
    """
    title = node.find("title").text
    year = node.find("year").text
    return Album(title, year)

def check(valeur,nom):
    if valeur == None:
	    return nom
    else:
	    return valeur.text

def parse_artiste(node):
    """
        Cette fonction parse un noeud de type "artiste", comme le suivant :
        <artist>
            <musicBrainzArtistID>c0252a1b-0133-46bb-8c4f-cade46349ec3</musicBrainzArtistID>
            <allmusicid>mn0000950099</allmusicid>
            <name>alestorm</name>
            <sortname>alestorm, autre</sortname>
            <type>artist</type>
            <yearsactive></yearsactive>
            <formed></formed>
            <biography>Alestorm are a power/folk metal band from Perth, Scotland, formed under the name Battleheart in 2004. Their music is characterised by a pirate theme, for which reason they describe their style as &amp;quot;True Scottish Pirate Metal&amp;quot;, (a joke in reference to True Norwegian Black Metal). After releasing two EPs, they were signed by Napalm Records in 2007 and renamed themselves to Alestorm.</biography>
            <born></born>
            <died></died>
            <disbanded></disbanded>
            <album>
                <title>Captain Morgan</title>
                <year>1990</year>
            </album>
            <album>
                <title>autre</title>
                <year>1995</year>
            </album>
        </artist>
    """
    trace("Function : parse_artiste")
    musicBrainzArtistID = node.find("musicBrainzArtistID").text
    name = node.find("name").text
    type = node.find("type").text
    biography  = node.find("biography").text
    born = node.find("born").text
    died = node.find("died").text
    formed = node.find("formed").text
    disbanded = node.find("disbanded").text
    genre = node.find("genre").text
    sortname = check(node.find("sortname"),name)
    album = [parse_album(elt) for elt in node.findall("album")]
    return Artist(musicBrainzArtistID, name, type, biography, born, died, formed, disbanded, genre, sortname, album)
 
def parse_file_artist(path):
    trace("Function : parse_file_artist")
    #tree = ET.parse(path)
    with codecs.open(path, 'r','utf8') as fichier:
        tree = ET.ElementTree()
        tree.parse (fichier)
        racine = tree.getroot()
        debug("racine : " +racine.tag)
        #artist est la racine donc pas de node!!
        #return [parse_artiste(node) for node in racine.findall("artist")]
        artiste = parse_artiste(racine)
        debug("On vient de parser dans : "+str(type(artiste)))
        return artiste
 
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

def Verification_Artist(Nom,Infos,chemin,Flag):
    trace("Function : Verification_Artist")
    info="Verification de l'artiste : "+Nom+" en base"
    debug(info)
    #creation de la requete
    requete="SELECT idArtist,strArtist,strMusicBrainzArtistID,strSortName FROM artist WHERE strMusicBrainzArtistID = \'"+Infos.musicBrainzArtistID+"\'"
    debug(requete)
    #connexion a la base
    base=C_PathBase+"MyMusic82.db"
    conn = Create_Connection(base)
    with conn:
        #execution de la requete
        cur = conn.cursor()
        cur.execute(requete)
        #recuperation des donnees : nomalement 1 seule ligne!!
        rows = cur.fetchall()
        if len(rows) !=0:
            print("%-10s %-25s %-38s %-10s" %("IdArtist","StrArtist","MusicBrainzArtistId","strSortName"))
            for row in rows:
                print("%-10s %-25s %-38s %-10s" %(row[0],row[1],row[2],row[3]))
            Verif_Images(row[0],Nom,Infos,conn,chemin,Flag)
            Verif_Infos(Nom,Infos,conn)
            Verif_Tri(Nom,Infos,conn)
            Purge_Infos(Nom,Infos,conn)
            if Flag:
                Verif_Disco(Nom,Infos,chemin,conn)
            else:
                Verif_Disco_Guest(Nom,Infos,chemin,conn)
        else:
            warn("L'artist "+Nom+" n'est pas en base avec l'id : "+Infos.musicBrainzArtistID+" !")
    #fermeture connexion
    conn.close()
    
def Verif_Images(Id,nom,Infos,connexion,chemin,Flag):
    trace("Function : Verif_Images")
    requete="SELECT art_id,media_id,type,url FROM art WHERE media_id = \'"+str(Id)+"\' and media_type = \'artist\'"
    debug(requete)
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)
        rows = cur.fetchall()
        nb=len(rows) 
        if nb != 0 :
            trace(    "il y a "+str(nb)+" lignes pour "+nom)
            for row in rows:
                print(row)
                if not Flag:
                    #le chemin ne doit pas contenir le nom de fichier ne doit pas etre folder et fanart
                    if row[3].split("\\")[-1] == "fanart.jpg":
                        requete="DELETE FROM art where art_id = " + str(row[0])
                        debug(requete)
                        cur.execute(requete)
                    elif row[3].split("\\")[-1] == "folder.jpg":
                        requete="DELETE FROM art where art_id = " + str(row[0])
                        debug(requete)
                        cur.execute(requete)
                        Ajoute_Images(Id,nom,connexion,chemin,Flag)
                    else:
                        trace("L'image est :" + row[3].split("\\")[-1])
                    
                    
        else:
            warn("Il manque des images!")
            Ajoute_Images(Id,nom,connexion,chemin,Flag)
            
def Verif_Infos(nom,Infos,connexion):
    trace("Function : Verif_Infos")
    #recuperation des parametres d'appel : debug/forced
    args = parse_arguments()
    requete="SELECT strBiography FROM artist WHERE strMusicBrainzArtistID = \'"+Infos.musicBrainzArtistID+"\'"
    debug(requete)
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)
        row = cur.fetchone()
        nb=len(row) 
        if nb != 0 :
            trace("Retour bio : " +str(row))
            if row == (None,):
                warn("Il manque la Biographie!")
                Ajoute_Bio(nom,Infos,connexion)
            else:
                trace("la Biographie est déjà présente")
                if args.Force:
                    trace("Forcage mise à jour")
                    Ajoute_Bio(nom,Infos,connexion)
        else:
            warn("Il manque la Biographie!")
            Ajoute_Bio(nom,Infos,connexion)

def Verif_Tri(nom,Infos,connexion):
    trace("Function : Verif_Tri")
    #recuperation des parametres d'appel : debug/forced
    args = parse_arguments()
    requete="Select strSortName from artist where strMusicBrainzArtistID = \'"+Infos.musicBrainzArtistID+"\'"
    debug(requete)
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)
        row = cur.fetchone()
        nb=len(row)
        if nb != 0 :
            trace("Ordre de tri : " +str(row))
            if row == (None,):
                warn("Il manque SortName!")
                Maj_Tri(nom,Infos,connexion)
            else:
                trace("l'orde de tri est déjà présent")
                if args.Force:
                    warn("Forcage mise à jour")
                    Maj_Tri(nom,Infos,connexion)
        else:
            warn("Il manque SortName!")
            Maj_Tri(nom,Infos,connexion)
        
def Ajoute_Images(Id,nom,connexion,chemin,Flag):
    trace("Function : Ajoute_Images")
    trace("Mise à jour des images foler/fanart")
    with connexion:
        max= Max_Table("art","art_id",connexion)
        cur = connexion.cursor()
        debug("le max (table ART) est "+str(max))
        nouveau=max+1
        #debut de la requete 
        req = "INSERT INTO art (art_id, media_id, media_type, type, url) VALUES ("
        #image : folder : thumb ou nom : thumb si GUEST
        if Flag:
            url=C_Image+nom+"\\folder.jpg"
        else:
            url=chemin+"\\"+nom+".jpg"
        debug("URL : "+url)
        if os.path.isfile(url):
            requete = req + str(nouveau)+","+str(Id)+",\"artist\",\"thumb\",\""+url+"\")"
            debug(requete)
            cur.execute(requete)
        else:
            warn("le fichier FOLDER :" +str(url)+" n'est pas accessible")
        #Flag : True = artiste False = Guest donc pas de fanart
        if Flag:
            #image : fanart : fanart
            url=C_Image+nom+"\\fanart.jpg"
            if os.path.isfile(url):
                nouveau=nouveau+1
                requete = req + str(nouveau)+","+str(Id)+",\"artist\",\"fanart\",\""+url+"\")"
                debug(requete)
                cur.execute(requete)
            else:
                warn("le fichier FANART :" +str(url)+" n'est pas accessible")
        connexion.commit()
        
def Ajoute_Bio(nom,Infos,connexion):
    trace("Function : Ajoute_Bio")
    with connexion:
        cur = connexion.cursor()
        #mise en forme du text 
        #&quot; => ""
        OK = Forme_Bio(Infos.biography)
        req = "UPDATE artist SET strBiography = \""
        requete = req + OK + "\" , strType = \"" + str(Infos.type) + "\" "
        #selon de type (Person ou Group) les infos ne sont pas les mêmes
        if Infos.type == "Group":
            if str(Infos.formed) != "None":
                requete = requete + ", strFormed = \"" + str(Infos.formed) + "\" "
            if str(Infos.disbanded) != "None":    
                requete = requete + " , strDisbanded = \"" + str(Infos.disbanded)  + "\" "
        else:
            if str(Infos.born) != "None":
                requete = requete + ", strBorn = \"" + str(Infos.born) + "\" "
            if str(Infos.died) != "None":    
                requete = requete + " , strDied = \"" + str(Infos.died) + "\" "
        requete = requete + " WHERE strMusicBrainzArtistID = \'"+Infos.musicBrainzArtistID+"\'"
        debug(requete)
        cur.execute(requete)
        #Verification du genre de l'artitst/groupe par rapport au genre des albums
        if Infos.genre != None:
            Verif_Genre(nom,Infos,connexion)
        else:
            warn("Pas de genre donc pas de vérification!")
        #mise à jour de la date de scraping 
        Maj_Scraped(Infos.musicBrainzArtistID,connexion)
        connexion.commit()
        
def Maj_Tri(nom,Infos,connexion):
    trace("Function : Maj_Tri")
    with connexion:
        cur = connexion.cursor()
        req = "UPDATE artist SET strSortName = \""
        requete = req +  str(Infos.sortname) + "\" "
        requete = requete + " WHERE strMusicBrainzArtistID = \'"+Infos.musicBrainzArtistID+"\'"
        debug(requete)
        cur.execute(requete)
        #mise à jour de la date de scraping 
        Maj_Scraped(Infos.musicBrainzArtistID,connexion)
        connexion.commit()

def traitement_Artiste(nom,chemin):
    trace("Function : traitement_Artiste")
    info="Traitement de l'artiste dans : "+chemin
    trace(info)
    args = parse_arguments()
    #ouverture et lecture fichier artist.nfo
    NomComplet=chemin+"\\artist.nfo"
    trace("Verification Artiste : "+NomComplet)
    artist = parse_file_artist(NomComplet)
    debug("fin de lecture du fichier NFO")
    debug("Type = "+str(type(artist)))
    if args.Debug:
        print(artist)
    Verification_Artist(nom,artist,chemin,True)

def traitement_Guest(nom,chemin):
    trace("Function : traitement_Guest")
    info="Traitement de la Guest Start :"+nom
    trace(info)
    args = parse_arguments()
    #ouverture et lecture fichier artist.nfo
    NomComplet=chemin+"\\"+nom+".nfo"
    trace("Verification Guest : "+NomComplet)
    guest = parse_file_artist(NomComplet)
    debug("fin de lecturedu fichier NFO")
    debug("Type = "+str(type(guest)))
    if args.Debug:
        print(guest)
    Verification_Artist(nom,guest,chemin,False)

def Maj_Scraped(ID,connexion):
    trace("Function : Maj_Scraped")
    Date = datetime.now()
    date_time = Date.strftime("%Y-%m-%d, %H:%M:%S")
    requete = "UPDATE artist SET lastScraped = \'" + date_time + "\' WHERE strMusicBrainzArtistID = \'"+ID+"\'"
    debug(requete)
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)
    
def Forme_Bio(original):
    "mise en forme de la biographie : remplacement de certain caractère qui serait mal afficher"
    #debug("mise en forme biographie: "+original)
    # cas des doubles quotes : fin de chaine!
    OK=original.replace('&quot;','\'')
    new=OK.replace('&apos','\'')
    OK=new
    new=OK.replace('&amp','&')
    OK=new
    new=OK.replace('&lt','<')
    OK=new
    new=OK.replace('&gt','>')
    OK=new
    new=OK.replace('« ','\'')
    OK=new
    new=OK.replace(' »','\'')
    #debug("renvoie : "+new)
    return new
     
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
    requete="UPDATE artist SET strGenres = \'" + Infos.genre + "\' WHERE strMusicBrainzArtistID = \'" + Infos.musicBrainzArtistID + "\'"
    debug(requete)
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)
        
def Ajoute_Genre(nom,Infos,connexion):
    "Ajout d'un nouveau genre dans la table des genres"
    trace("Function : Ajoute Genre")
    #requete="SELECT max(idGenre) FROM genre "
    #debug(requete)
    with connexion:
        cur = connexion.cursor()
        #cur.execute(requete)
        max=Max_Table("genre","idGenre",connexion)
        debug("le max (table GENRE) est "+str(max))
        nouveau=max+1
        ajoute="INSERT INTO genre (idGenre, strGenre) VALUES ( \'" + str(nouveau) + "\' , \'" + Infos.genre + "\')"
        debug(ajoute)
        cur.execute(ajoute)

def Purge_Infos(nom,Infos,connexion):
    "suppression des informations inutiles : Mood Styles"
    trace("Function : Purge_Infos")
    vide="NULL"
    reqmood="UPDATE artist set strMoods = NULL WHERE strMusicBrainzArtistID = \'" + Infos.musicBrainzArtistID + "\'" 
    debug(reqmood)
    reqstyl="UPDATE artist set strStyles = NULL WHERE strMusicBrainzArtistID = \'" + Infos.musicBrainzArtistID + "\'" 
    debug(reqstyl)
    with connexion:
        cur = connexion.cursor()
        cur.execute(reqmood)
        cur.execute(reqstyl)

def Recupere_album(Chemin):
    trace("Function : Recupere_album")
    debug("On cherche dans ="+Chemin)
    rep = [f.path for f in os.scandir(Chemin) if f.is_dir()]
    return rep

def Verif_Disco(nom,Infos,Chemin,connexion):
    trace("Function : Verif_Disco")
    debug(Chemin)
    disco = []
    dir=Recupere_album(Chemin)
    debug("Repertoire"+str(dir))
    for d in dir:
        rep=d.split("\\")[-1]
        disco.append(rep)
        debug("album : "+rep)
	#recuperartion de l'ID pour la purge dans discography
    requete = "SELECT idArtist FROM artist WHERE strMusicBrainzArtistID = \'" + Infos.musicBrainzArtistID + "\'"
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)
        IdArtist = cur.fetchone()
        debug("IdArist : " +str(IdArtist))
        requete = "DELETE FROM discography WHERE idArtist = "+str(IdArtist[0])+" AND strAlbum NOT IN ("
        for disque in disco:
            requete = requete +"\'" +str(disque)+"\',"
        requete = requete[0:-1] +")"
        debug(requete)
        cur.execute(requete)
        for disque in disco:
            reqmaj="INSERT INTO discography (idArtist, strAlbum) VALUES ("+str(IdArtist[0])+", \'"+str(disque)+"\' ) EXCEPT SELECT idArtist, strAlbum FROM discography WHERE strAlbum = \'"+str(disque)+"\' AND idArtist = "+str(IdArtist[0])
            debug(reqmaj)
            cur.execute(reqmaj)
			
def Verif_Disco_Guest(nom,Infos,Chemin,connexion):
    trace("Function : Verif_Disco_Guest")
    debug(Chemin)
    rep=Chemin.split("\\")
    #le dernier
    dir=rep[-1]
	#recuperartion de l'ID pour la purge dans discography
    requete = "SELECT idArtist FROM artist WHERE strMusicBrainzArtistID = \'" + Infos.musicBrainzArtistID + "\'"
    with connexion:
        cur = connexion.cursor()
        cur.execute(requete)
        IdArtist = cur.fetchone()
        debug("IdArist : " +str(IdArtist))
        requete = "DELETE FROM discography WHERE idArtist = "+str(IdArtist[0])+" AND strAlbum NOT IN (\""+dir+"\")"
        debug(requete)
        cur.execute(requete)
        reqmaj="INSERT INTO discography (idArtist, strAlbum) VALUES ("+str(IdArtist[0])+", \""+str(dir)+"\" ) EXCEPT SELECT idArtist, strAlbum FROM discography WHERE strAlbum = \""+str(dir)+"\" AND idArtist = "+str(IdArtist[0])
        debug(reqmaj)
        cur.execute(reqmaj)

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
# portable
#C_PathBase = "C:\\Users\\ungvar\\AppData\\Roaming\\Kodi\\userdata\\Database\\"
# maison
#C_PathBase = "C:\\Users\\dom\\AppData\\Roaming\\Kodi\\userdata\\Database\\"
#C_Image="D:\\Torrents\\Test_Kodi\\"
#MAJ REELLE 
C_PathBase = "C:\\Users\\dom\\AppData\\Roaming\\Kodi\\userdata\\Database\\"
C_Image="smb:\/\/OSMC\/Musiques"