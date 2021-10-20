from . import spriteobject
 
class Ball(spriteobject.SpriteObj):
   horizMove= 1
   verMove = 0.4
   moveRight = True
   moveTop = True
 
   def userHit(self, leftSide):
       self.moveRight = leftSide
 
   def sideHit(self):
       self.moveTop = not self.moveTop
 
   def prevent_stick(self, user):
       self.move(self.get_x_movement() *.1* user.width, 0)
 
   def moving(self, clock):
       self.move(self.get_x_movement(), self.get_y_movement())
 
   def get_x_movement(self):
       if self.MOVING_RIGHT:
           return self.horizMove
       else:
           return -self.horizMove
 
   def get_y_movement(self):
       if self.MOVING_TOP:
           return self.verMove
       else:
           return -self.verMove
