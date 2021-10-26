# coding: utf-8
import argparse
import logging, sys

def parse_arguments():
    #verif parametre
    parser = argparse.ArgumentParser()
    parser.add_argument("Fichier", help="Fichier à traiter")
    parser.add_argument("-d" , "--Debug" , help="Mode debug : plus de trace", action="store_true")
    parser.add_argument("-f" , "--Force" , help="Mode forcé : mise à jour de  base même si déjà renseigné", action="store_true")
    return parser.parse_args()  
	
def debug(chaine):
   args=parse_arguments()
   if args.Debug:
       logging.debug(chaine)
	   
def trace(chaine):
    logging.info(chaine)

def warn(chaine):
    logging.warn(chaine)
    
def error(chaine):
    logging.error(chaine)

#fichier de log
#logging.basicConfig(filename='d:\\Torrents\Test_Kodi\script.log',format='%(asctime)s - %(levelname)s : %(message)s',level=logging.DEBUG)
#logger = logging.getLogger('Check_Kodi')
#logger.addHandler(logging.StreamHandler(sys.stdout))

logging.getLogger().setLevel(logging.DEBUG)  # This must be as verbose as the most verbose handler

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s\t: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

console_logging = logging.StreamHandler()
console_logging.setLevel(logging.DEBUG)
console_logging.setFormatter(formatter)
logging.getLogger().addHandler(console_logging)

file_logging = logging.FileHandler('d:\\Torrents\Test_Kodi\script.log')
file_logging.setLevel(logging.DEBUG)
file_logging.setFormatter(formatter)
logging.getLogger().addHandler(file_logging)

