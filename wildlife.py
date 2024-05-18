# wildlife.py

import requests
from location import gps_coordinate

__all__ = ['search_sightings', 'search_species', 'display_sightings', 'display_species']

def display_species(species_list):
  for species in species_list:
    if "Species" in species and "AcceptedCommonName" in species["Species"]:
      print(species["Species"]["AcceptedCommonName"])
    else:
      print("Common name not available for this species.")

def search_species(city):
  coordinate = gps(city)
  if coordinate:
    radius = 100000
    species_list = get_species_list(coordinate, radius)
    if species_list:
      return species_list
  return []

def search_sightings(taxonid, city):
  coordinate = gps(city)
  if coordinate:
    radius = 100000
    sightings = get_surveys_by_species(coordinate, radius, taxonid)
    if sightings:
      return sightings
  return []

def sort_by_date(sightings):
  """Sorts a list of sightings by the 'StartDate' property."""
  return sorted(sightings, key=lambda sighting: sighting['properties']['StartDate'])

def display_sightings(sightings):
  if sightings:
    sorted_sightings = sort_by_date(sightings)
    print("Animal Sightings:")
    for sighting in sorted_sightings:
      print(f"Date: {sighting['properties']['StartDate']}, Location: {sighting['properties']['LocalityDetails']}")
  else:
    print("No animal sightings found.")

def filter_venomous(species_list):
      return [species for species in species_list if species["Species"]["PestStatus"] == "Venomous"]


def gps(city):
  return gps_coordinate(city)

def get_species_list(coordinate, radius):
  url = f"https://apps.des.qld.gov.au/species/?op=getspecieslist&kingdom=animals&circle={coordinate['latitude']},{coordinate['longitude']},{radius}"
  response = requests.get(url)
  data = response.json()
  if data and "SpeciesSightingSummariesContainer" in data:
    return data["SpeciesSightingSummariesContainer"]["SpeciesSightingSummary"]
  else:
    return None

def get_surveys_by_species(coordinate, radius, taxonid):
  url = f"https://apps.des.qld.gov.au/species/?op=getsurveysbyspecies&taxonid={taxonid}&circle={coordinate['latitude']},{coordinate['longitude']},{radius}"
  response = requests.get(url)
  data = response.json()
  if data and "features" in data:
    return data["features"]
  else:
    return None
