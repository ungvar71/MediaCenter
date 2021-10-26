# coding: utf-8
import sys, os
import sqlite3
import argparse
import shutil
from datetime import datetime


from lib import parse_arguments,debug,trace,warn,error
from artists import *
from albums import *
from genres import *

def Bonne_Balise(File,rep):
    trace("Function : Bonne_Balise")                    
    mot=[["musicBrainzAlbumID" , "musicbrainzalbumid"],["musicBrainzReleaseGroupID" , "musicbrainzreleasegroupid"]]
    out=open(rep+"\\"+"Nouveau.nfo","w")
    with open(File, 'r') as filin:
        lignes = filin.readlines()
        for ligne in lignes:
            #debug(ligne)
            for i in range(len(mot)):
                #debug("indice " +str(i) +" remplacement de : " + mot[i][0] + " par " + mot[i][1])
                newline=ligne.replace(mot[i][0],mot[i][1])
                ligne=newline
            out.write(newline)        
         #debug("Ecrire : " + newline)
    out.close()
    shutil.copy(rep+"\\"+"Nouveau.nfo",args.Fichier)
    try:
        os.remove(rep+"\\"+"Nouveau.nfo")
    except OSError as e:
        error(e)
    else:
        trace("File is deleted successfully")    
    
    
    
trace("###################")
trace("Programme principal")
trace("###################")
#gestion des arguments : debug force et nom+chemein du fichier à traiter    
args=parse_arguments()
debug("traitemnt du fichier : %s" % args.Fichier)

#decoupage du chemin en repertoire
rep=args.Fichier.split("\\")
#le dernier
Fichier=rep[-1]
#nom du sous repertoire contenent directement le fichier 
nom_rep=rep[-2]
trace("Le fichier "+Fichier+" est celui d'"+nom_rep)



absFilePath = os.path.abspath(args.Fichier)
path, filename = os.path.split(absFilePath)
debug("le chemin du fichier a lire est {} et le nom est {}".format(path, filename))
#le corp de nom de fichier permet de savoir quel traitement lancer
corp=Fichier.split(".")[0]
trace("traitement de données de type : "+corp)



if corp == "artist":
    #lecture du fichier artist.nfo donc artist avec au moins 1 sous-repertoire album
	traitement_Artiste(nom_rep,path)
elif corp == "album":
    #lecture du fichier album.nfo 
    #mise en forme des balises musicBrainzAlbumID en musicbrainzalbumid
    # et musicReleaseGroupID en musicreleasegroupid
    Bonne_Balise(args.Fichier,path)
    traitement_Album(nom_rep,path)
elif corp == "Renum":
    #renumerotation des artistes
    Renum_Artist(nom_rep,path)
elif corp == "Check_Genre":
    #ecriture dans Check_Genre.txt
    #verification des liaisons artist/genre , albulm/genre et song/genre
    traitement_Genre(nom_rep,path)
else:
    #lecture du fichier XXXXX.nfo donc artist dans 1 sous-repertoire album
    #il n'y a pas d'artist avec ce nom en tant que tel : juste pour avoir des infos
    #il doit y avoir aussi un fcihier XXXXX.jpg pour le thumb de ce guest!
	traitement_Guest(corp,path)