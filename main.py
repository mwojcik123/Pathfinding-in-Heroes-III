

class Disease:
    def __init__(self, name, progress=0):
        self.name = name

        self.progress = progress

    def grow_progress(self):
        self.progress += 1
        self.name.hp -= 1
        print(self.progress)

    def decrease_progress(self):
        self.progress -= 1
        self.name.hp += 1

        print(self.progress)


class Animal:
    def __init__(self, name, say, master):
        self.name = name
        self.say = say
        self.master = master
        self.hp = 100
        self.sick = Disease(self)

    def get_status(self):
        return self.hp


class Dog(Animal):
    def __init__(self, name, say, master, color):
        super().__init__(name, say,  master)
        self.color = color

    def bark(self):
        print("{} {} say {}!".format(self.name, self.color, self.say))


dogie = Dog("szarik", "WOFF WOFF", "Max", "black")
dogie.bark()
dogie.sick.grow_progress()
dogie.sick.grow_progress()
dogie.sick.grow_progress()
dogie.sick.grow_progress()
print(dogie.sick.name)
print(dogie.get_status())
