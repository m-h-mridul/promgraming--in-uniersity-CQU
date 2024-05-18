#sighting.py
from wildlife import search_sightings, search_species, display_sightings, display_species, filter_venomous
from location import gps_coordinate

def display_menu():
    print("Help")
    print("====")
    print("The following commands are recognized.")
    print("Display help:           wildlife> help")
    print("Exit the application: wildlife> exit")
    print("Display animal species in a city: wildlife> species <city>")
    print("Display animal sightings in a city: wildlife> sightings <city> <taxonid>")
    print("Display venomous species in a city: wildlife> species <city> venomous")

def main():
    display_menu()
    while True:
        command = input("wildlife> ")
        if command == "help":
            display_menu()
        elif command == "exit":
            print("Exiting the application.")
            break
        elif command.startswith("species"):
            args = command.split(" ")
            city = args[1]
            if len(args) == 3 and args[2] == "venomous":
                species_list = search_species(city)
                if species_list:
                    venomous_species = filter_venomous(species_list)
                    display_species(venomous_species)
                else:
                    print("No species found for the given city.")
            else:
                species_list = search_species(city)
                if species_list:
                    display_species(species_list)
                else:
                    print("No species found for the given city.")
        elif command.startswith("sightings"):
            args = command.split(" ")
            city = args[1]
            taxonid = args[2]
            sightings = search_sightings(taxonid, city)
            if sightings:
                display_sightings(sightings)
            else:
                print("No sightings found for the given city and taxonid.")
        else:
            print("Invalid command. Type 'help' for available commands.")

if __name__ == "__main__":
    main()