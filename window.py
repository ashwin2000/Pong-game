
import simplejson, socket, sys, pyglet
from . import settings
from . import game
 
class Window(pyglet.window.Window):
   keys = None
   game = None
 
   def __init__(self, *args, **kwargs):
	 #initialise window for messaging
       pyglet.window.Window.__init__(self, *args, **kwargs)
       self.game = game.Game(boolMultiplayer=True)
       self.keys = pyglet.window.key.KeyStateHandler()
       self.pushHandlers(self.keys)
 
   def moveuser(self, dx, dy):
       user = self.game.userMe
       user.move(0, dy, y_bounds=(0, settings.WINDOW_HEIGHT - user.height))
 
   def parseKeys(self):
       dy = (settings.MOVE_SPEED if self.keys[pyglet.window.key.UP] else 0) \
           + (-settings.MOVE_SPEED if self.keys[pyglet.window.key.DOWN] else 0)
       self.moveuser(0, dy)
 
   def MouseScroll(self, x, y, scrollX, scrollY):
       self.moveuser(scrollX * settings.MOVE_SPEED, scrollY * settings.MOVE_SPEED)
 
   def on_draw(self):
       self.clear()
       self.parse_keys()
       self.game.draw()
       self.game.debug_text.draw()
       self.game.ball.draw()
       self.game.score.draw()
       self.game.userLeft.draw()
       self.game.userRight.draw()
