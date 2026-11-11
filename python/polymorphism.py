class mammel:
    def intro(self):
        print("Every mammel has legs")
    
    def legs(self):
        print("They have no legs")

class humans(mammel):
    def legs(self):
        print("They have two legs")

class cat(mammel):
    def legs(self):
        print("They have four legs")

obj_bird = mammel()
obj_spr = humans()
obj_ost = cat()

obj_bird.intro()
obj_bird.legs()

obj_spr.intro()
obj_spr.legs()

obj_ost.intro()
obj_ost.legs()