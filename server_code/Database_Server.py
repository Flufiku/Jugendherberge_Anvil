import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3

@anvil.server.callable
def get_guest(columns="*"):
  conn = sqlite3.connect(data_files['Jugendherberge_Datenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {columns} FROM Gast"))
  conn.close()
  return res


@anvil.server.callable
def get_jugendherberge(column="*"):
  conn = sqlite3.connect(data_files['Jugendherberge_Datenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {column} FROM Jugendherberge"))
  conn.close()
  return res


@anvil.server.callable
def get_zimmer(fk_Jugendherberge, column="*"):
  conn = sqlite3.connect(data_files['Jugendherberge_Datenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {column} FROM Zimmer WHERE fk_Jugendherberge = {fk_Jugendherberge}"))
  conn.close()
  return res


@anvil.server.callable
def get_preis(Preiskategorie_ID, column="*"):
  conn = sqlite3.connect(data_files['Jugendherberge_Datenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {column} FROM Preiskategorie WHERE Preiskategorie_ID = {Preiskategorie_ID}"))
  conn.close()
  return res


@anvil.server.callable
def create_buchung(Buchung_ID, Startdatum, Enddatum, fk_Jugendherberge, fk_Zimmer, fk_Gast):
  conn = sqlite3.connect(data_files['Jugendherberge_Datenbank.db'])
  cursor = conn.cursor()
  cursor.execute(f"INSERT INTO Buchung (Buchung_ID, Startdatum, Enddatum, fk_Jugendherberge, fk_Zimmer, fk_Gast) VALUES ({Buchung_ID}, {Startdatum}, {Enddatum}, {fk_Jugemdherberge}, {fk_Zimmer}, {fk_Gast});")
  conn.commit()
  conn.close()
  return res


@anvil.server.callable
def get_buchungsnummer():
  conn = sqlite3.connect(data_files['Jugendherberge_Datenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("SELECT COUNT(Buchung_ID) FROM Buchung"))
  conn.close()
  return res


@anvil.server.callable
def add_buchung_gast(fk_Gast, fk_Buchung):
  conn = sqlite3.connect(data_files['Jugendherberge_Datenbank.db'])
  cursor = conn.cursor()
  cursor.execute(f"INSERT INTO Buchung_Gast (fk_Gast, fk_Buchung) VALUES ({fk_Gast}, {fk_Buchung});")
  conn.commit()
  conn.close()
  return res
