from . import spriteobject
 
class user(spriteobject.SpObj):
 
   Score = 0
 
   def increase_score(self):
       self.Score += 1
 
   def get_hit_effect(self):
       if self.y:
           return self.y * -1
   
