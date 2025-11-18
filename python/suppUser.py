#!/usr/bin/python3

import psycopg2

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

def suppUser(conn):
  
  print("Vous voulez supprimer un utilisateur\n")
  email_supp= quote(input("Entrez l'adresse mail de l'utiulisateur a supprimer': \n"))
  
  cur = conn.cursor()
  sql = "DELETE FROM Utilisateur WHERE email = %s"
  cur.execute(sql, (email_supp,))

  #si on veut verifier l'existence de l'utilisateur avant de le supprimer 
  #if cur.fetchone() is NULL:
    #print("Cet utilisateur n'existe pas.")
  #else:
    #cur.execute("DELETE FROM Utilisateur WHERE email = %s", (email_supp,))
    #conn.commit()
    
  conn.commit()