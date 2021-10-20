import pyglet
 
class SpObj(pyglet.sprite.Sprite):
 
   def __init__(self, img, x=0, y=0, blend_src=770, blend_dest=771, batch, group, usage='dynamic'):
       pyglet.sprite.Sprite.__init__(self, img, x, y, blend_src, blend_dest, batch, group, usage)
       self.img = img
 
   def getleft(self):
       return self.x
 
   def getright(self):
       return self.x + self.width
 
   def gettop(self):
       return self.y + self.height
 
   def getbottom(self):
       return self.y
 
   def move(self, dx, dy, x_bounds=None, y_bounds=None):
       return self.move_absolute(self.x + dx, self.y + dy, x_bounds=x_bounds, y_bounds=y_bounds)
 
   def move(self, dx, dy, x_bounds=None, y_bounds=None):
       if x_bounds is not None:
           self.x = min(max(self.x+dx, x_bounds[0]), x_bounds[1])
       if y_bounds is not None:
           self.y = min(max(self.y+dy, y_bounds[0]), y_bounds[1])
 
   def setWidth(self, width):
       self.img.width = width
 
   def setHeight(self, height):
       self.img.height = height
 
   def midAnchorY(self, winh):
       self.y = winh / 2 - self.height // 2
       return self
 
   def midAnchorX(self, winw):
       self.x = winw / 2 - self.width // 2
       return self
