'''
Author:  Boss Oberlin
Date: 04/25/2024
Assignment: Project 2
Course: CPSC1051
'''
import csv


class PlayableMap: #Sets map
    def __init__(self):
        self.playable_map = {}
    def add_place(self, placeobject):
        self.playable_map[placeobject.get_name().lower()] = placeobject
    def get_place(self, placename):
        return self.playable_map.get(placename.lower())
    def add_item(self, itemobject):
        self.playable_map[itemobject.get_itemname().lower()] = itemobject
    def get_item(self,itemname):
        return self.playable_map.get(itemname.lower())


class Place: #Sets place and features of place in map
    def __init__(self, name, areadescrip, nearby, animals, items):
        self.name = name
        self.areadescrip = areadescrip
        self.nearby = nearby
        self.animals = animals
        self.items = items
   
    def get_name(self):
        return self.name
    def get_areadescrip(self):
        return self.areadescrip
    
    def get_nearby(self):
        return self.nearby
    def list_nearby(self):
        return '\n'.join(self.nearby)
    
    def get_animals(self):
        return self.animals
    def list_animals(self):
        return '\n'.join(self.animals)

    def get_items(self):
        return self.items
    def list_items(self):
        return '\n'.join(self.items)
    def __str__(self):
        return f"{self.get_name()}: {self.get_areadescrip()}\nThese are the nearby areas, take a look and explore!\n{self.list_nearby()}" 



class AreaNotFound(Exception): #if person chooses incorrect area
    def __init__(self, area):
        self.area = area
    def __str__(self):
        return f"{self.area}? Where are you going? Head to another area."


class Animal(): #animal class
    def __init__(self, animalname):
        self.animalname = animalname
        
    def get_animal_name(self):
        return self.animalname

class Horse(Animal): #horse derived class
    
    def __init__(self):
        super().__init__("Horse")
        self.sound = "Neigh"

    def get_sound(self):
        return self.sound

class Fish(Animal): #fish derived class
    def __init__(self):
        super().__init__("Fish")
        self.sound = "blub"
    def get_sound(self):
        return self.sound

def main():
    inventory = [] #sets inventory
    count = 0
    with open('Project2Finalstats.csv', 'r') as file: #adds items from inventory, but only a max of two items may be taken or it goes to zero
        filelines = csv.reader(file)
        for line in filelines:
            if line[0] == "Blank":
                inventory = []
                
            else:
                inventory.append(line[0])
                count = count+1
            if count == 3:
                inventory = []
                break
            
    playable_map = PlayableMap() #initiales map
    
    #initializes animals
    horse = Horse()
    fish = Fish()
    deer = Animal("Deer")
    person = Animal("Person")
    
    #adds places
    playable_map.add_place(Place("Town Square", "The center of town, it is always high noon around here",["Bar","River","Plains"], ['Horses'],["Gun"]))
    playable_map.add_place(Place("Bar", "The other center of town", ["Town Square"], ["Person"], ['Booze']))
    playable_map.add_place(Place("River", "A good place for relxaing", ["Town Square", "Plains" ], ["Fish"], ["Fishing Rod"]))
    playable_map.add_place(Place("Plains", "Hotter than hell, but many deer are found here", ["Town Square", "River"], ["Deer"], ["Lucky Antler"]))

    #more initializing
    choiceplace = "Town Square"
    skiptown = False
    print("Welcome to the the WILD WEST game\nTo leave, type skip town")
    current_place = playable_map.get_place(choiceplace)
    
    #loop of game
    while not skiptown:
        try: #try block for errors
            leavechoice = input(f"Please choose a place to go or skip town.\n{current_place.list_nearby()} \n").lower().strip() #goes through places
            if leavechoice == "skip town":
                print("Skipping town, will be back")
                skiptown = True

            elif leavechoice in [placeexits.lower() for placeexits in current_place.get_nearby()]: #finds exits
                current_place = playable_map.get_place(leavechoice)
                print(current_place)
                if not current_place.list_items(): #if no items
                    print("There are no items left...")
                else:
                    print(f"These are the items found here.\n{current_place.list_items()}") #if items
                    pickup = input("Would you like an item?\n").lower()
                    if pickup == "yes":
                        itemtoinv = current_place.items.pop(0) #takes item from list and puts it into inventory
                        inventory += [itemtoinv]
                        print(f'Your inventory: \n{inventory}')
                    
                    elif pickup == "no":
                        print("It'll still be here when you get back")
                
                    else:
                        while pickup != "yes" and pickup != "no": #validation
                            print("You made no choice")
                            pickup = input("Would you like one?\n").lower()
                if not current_place.list_animals():
                    print("There are no animals left")  

                elif horse.get_animal_name() in (current_place.list_animals()): #all similar, if animalname in list of animals
                        print(f"This is the animal found here")
                        print(horse.get_animal_name())
                        print(f'In the distance you hear {horse.get_sound()}')

                elif fish.get_animal_name() in (current_place.list_animals()):
                        print(f"This is the animal found here")
                        print(fish.get_animal_name())
                        print(f'Under the water, you hear {fish.get_sound()}')

                elif deer.get_animal_name() in (current_place.list_animals()):
                        print(f"This is the animal found here")
                        print(deer.get_animal_name())

                elif person.get_animal_name() in (current_place.list_animals()):
                        print(f"This is the animal found here")
                        print(person.get_animal_name())
                    
                if "Gun" in inventory and "Deer" in current_place.list_animals(): #to go hunting, need both
                    hunting = input("Would you like to hunt?\n").lower()
                    if hunting == "yes":
                        print("You shot a deer")
                        animaltoinv = current_place.animals.pop(0) #very much removes deer
                        inventory += [animaltoinv]
                        print(f'Your inventory: \n{inventory}')
                    while hunting != "yes" and hunting != "no":
                        print("Come on, it's a yes or no question") #validation
                        hunting = input("Would you like to hunt?\n").lower()

                elif "Fishing Rod" in inventory and "Fish" in current_place.list_animals(): #to go fishing, need both
                    fishing = input("Would you like to fish?\n").lower()
                    if fishing == "yes":
                        print("You caught a state record fish!!")
                        fishtoinv = current_place.animals.pop(0) #removes fish
                        inventory += [fishtoinv]
                        print(f'Your inventory: \n{inventory}')
                    while fishing != "yes" and fishing != "no": #validation
                        print("Come on, it's a yes or no question")
                        fishing = input("Would you like to fish?\n").lower()
                    
            else:
                raise AreaNotFound(leavechoice) #custom exception being raised
        except AreaNotFound as e:
            print(e)

    with open('Project2Finalstats.csv', 'w') as file: #writes inventory
        inventfile = csv.writer(file)
        for inventitem in inventory:
            inventfile.writerow([inventitem])
            
if __name__ == "__main__":
    main()