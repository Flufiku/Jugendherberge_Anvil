from ._anvil_designer import Main_PageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime


class Main_Page(Main_PageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    self.all_guests = []
    
    self.populate_guest()
    self.reset_herberge()
    
    


  def reset_herberge(self):
    self.reset_room()
    self.drop_down_herberge.items = ["Bitte wählen Sie zuerst aus, wer Sie sind."]
  
  def reset_room(self):
    self.reset_extra_guest()
    self.label_price.text = "Preis: 0,00€"
    self.drop_down_room.items = ["Bitte wählen Sie zuerst eine Herberge aus."]
  
  def reset_extra_guest(self):
    self.drop_down_extra_guest.items = ["Bitte wählen Sie zuerst ein Zimmer aus."]
    self.label_extra_guest.text = ""
    self.all_guests = []


  def populate_guest(self):
    content = anvil.server.call('get_guest', "Vorname, Nachname")
    items = [f"{Vorname} {Nachname}" for Vorname, Nachname in content]
    items.insert(0, "Bitte wählen Sie einen Account aus.")
    self.drop_down_guest.items = items
    self.drop_down_guest.selected_value = self.drop_down_guest.items[0]
  def populate_herberge(self):
    content = anvil.server.call('get_jugendherberge', "Name")
    items = [f"{Name[0]}" for Name in content]
    items.insert(0, "Bitte wählen Sie eine Herberge aus.")
    self.drop_down_herberge.items = items
    self.drop_down_herberge.selected_value = self.drop_down_herberge.items[0]
  def populate_room(self):
    content = anvil.server.call('get_zimmer', self.drop_down_herberge.items.index(self.drop_down_herberge.selected_value), "Zimmernummer, Kapazitaet")
    items = [f"{Zimmernummer} ({Kapazitaet} Personen)" for Zimmernummer, Kapazitaet in content]
    items.insert(0, "Bitte wählen Sie ein Zimmer aus.")
    self.drop_down_room.items = items
    self.drop_down_room.selected_value = self.drop_down_room.items[0]
    self.label_price.text = "Preis: 0,00€"
  def populate_extra_guest(self):
    content = anvil.server.call('get_guest', "Vorname, Nachname")
    items = [f"{Vorname} {Nachname}" for Vorname, Nachname in content]
    items.remove(self.drop_down_guest.selected_value)
    items.insert(0, "Fügen Sie weitere Gäste hinzu.")
    self.drop_down_extra_guest.items = items
    self.drop_down_extra_guest.selected_value = self.drop_down_extra_guest.items[0]



  
  def drop_down_guest_change(self, **event_args):
    if self.drop_down_guest.items.index(self.drop_down_guest.selected_value) == 0:
      self.reset_herberge()
    else:
      self.populate_herberge()
      self.reset_room()

  def drop_down_herberge_change(self, **event_args):
    if self.drop_down_herberge.items.index(self.drop_down_herberge.selected_value) == 0:
      self.reset_room()
    else:
      self.populate_room()
      self.reset_extra_guest()

  def drop_down_room_change(self, **event_args):
    if self.drop_down_room.items.index(self.drop_down_room.selected_value) == 0:
      self.reset_extra_guest()
      self.label_price.text = "Preis: 0,00€"
    else:
      self.reset_extra_guest()
      self.populate_extra_guest()

      
      selected_jugendherberge = self.drop_down_herberge.items.index(self.drop_down_herberge.selected_value)
      selected_room = self.drop_down_room.selected_value.split(" ")[0]
      preis_kategorie = anvil.server.call("get_zimmer", f"{selected_jugendherberge} AND Zimmernummer = {selected_room}", "fk_Preiskategorie")[0][0]
      preis = anvil.server.call('get_preis', f"{preis_kategorie}", "Preis")[0][0]
      self.label_price.text = f"Preis: {preis:.2f}€"

  def outlined_button_extra_guest_click(self, **event_args):
    selected_extra_guest = self.drop_down_extra_guest.items.index(self.drop_down_extra_guest.selected_value)
    if selected_extra_guest >= self.drop_down_guest.items.index(self.drop_down_guest.selected_value):
      selected_extra_guest += 1
    if selected_extra_guest not in self.all_guests and len(self.all_guests) < int(self.drop_down_room.selected_value.split("(")[1][0])-1 and selected_extra_guest > 0:
      self.all_guests.append(selected_extra_guest)
      prefix = "" if self.label_extra_guest.text == "" else "\n"
      self.label_extra_guest.text +=  prefix + self.drop_down_extra_guest.selected_value

  def outlined_button_book_click(self, **event_args):
    Buchung_ID = anvil.server.call('get_buchungsnummer')[0][0]+1
    Startdatum = datetime.datetime.now().date()
    Enddatum = datetime.datetime.now().date() + datetime.timedelta(days=7)
    fk_Jugendherberge = self.drop_down_herberge.items.index(self.drop_down_herberge.selected_value)
    fk_Zimmer = self.drop_down_room.selected_value.split(" ")[0]
    fk_Gast = self.drop_down_guest.items.index(self.drop_down_guest.selected_value)

    anvil.server.call('create_buchung', Buchung_ID, Startdatum, Enddatum, fk_Jugendherberge, fk_Zimmer, fk_Gast)

    for guest in self.all_guests:
      anvil.server.call('add_buchung_gast', guest, Buchung_ID)
  

  