#!/usr/bin/python3

import psycopg2
from datetime import date

HOST = "tuxa.sme.utc"
USER = "nf18a016"
PASSWORD = "EX8GdC5vmx9e"
DATABASE = "nf18a016"

conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))


def quote(s):
  if s:
    return '\'%s\'' % s
  else:
    return 'NULL'

def ajouterModele(conn):
    
    print("Vous voulez ajouter un nouveau mpodele\n")
    name= quote(input("Entrez le nom du modele: \n"))
    descript= quote(input("Entrez la description du modele : \n"))
    dateCreation= date.today()
    
    types_modele= ["image", "texte", "video"]
    type = quote(input("Type de modèle (image / texte / video) : ").lower())
    while type not in types_modele:
        print("Valeur invalide. Veuillez entrer : image, texte ou video.")
        type = quote(input("Type de modèle (image / texte / video) : ").lower())

    longueur= int(input("Entrez la longueur max de la saisie: \n"))
    resolution= int(input("Entrez la resolutuon du modele: \n"))
    duree= int(input("Entrez la duree: \n"))

    cur = conn.cursor()
    sql = "INSERT INTO Modele (nom, description, dateCreation, TypeModele, longueurMax, resolution, duree) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql, (name, descript, dateCreation, type, longueur, resolution, duree))
    conn.commit()
