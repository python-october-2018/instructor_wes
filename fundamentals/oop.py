class Animal:
  def __init__(self, name, habitat, num_limbs, diet):
    self.name = name
    self.habitat = habitat
    self.num_limbs = num_limbs
    self.diet = diet
    self.health = 100
    self.endurance = 0
  
  def print_info(self):
    print(self.__dict__)
    return self
  
  def exercise(self):
    self.health = self.health + 10
    return self

class Mammal(Animal):
  def __init__(self, name, habitat, num_limbs, diet):
    super().__init__(name, habitat, num_limbs, diet)
    self.hunger = 0
    self.lungs = 2
  

my_animal = Animal("Froggy the Frog", 'Tropical Rainforest', 4, "Bugs n stuff")
other_animal = Animal("Doggy the Dog", "The Suburbs", 4, "Kibbles")
mammal = Mammal("Shamoo", "Water", 0, "Small fish")
mammal.print_info()
