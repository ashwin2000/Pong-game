Class Game :  
 
import socket, sys
import pyglet, simplejson
from pyglet import clock
from . import settings
from .user import user
from .ball import Ball
 
def connect():
   try:
       connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       connection.connect((settings.SERVER_IP, settings.SERVER_PORT))
       me = str(connection.getsockname()[1])
       return [me, connection]
   except socket.error:
       sys.exit(1)
 
class Game(pyglet.window.Window):
   running = False
   sleepIdle = True
   primaryClient = False
 
   def __init__(self, boolMultiplayer= False):
       self.load_sprites()
       self.boolMultiplayer = boolMultiplayer
       if self.boolMultiplayer:
           self.me, self.connection = connect()
           clock.schedule(self.update_server_data)
 
   def draw(self):
       sleep_time = clock.get_sleep_time(self.sleep_idle)
       if self.boolMultiplayer:
           self.drawMultiplayer()
       else:
           self.drawSingleplayer()
 
   def run(self):
       if not self.running:
           if self.primaryClient:
               clock.schedule_interval(self.ball.moving, .005)
           self.running = True
 
   def pause(self):
       if self.running:
           if self.primaryClient:
               clock.unschedule(self.ball.moving)
           self.running = False
 
   def load_sprites(self):
       self.debug_text = pyglet.text.Label('', font_size=10, x=0, y=settings.WINDOW_HEIGHT, anchor_x='left', anchor_y='top')
       self.score = pyglet.text.Label('', font_size=15, x=settings.WINDOW_WIDTH/2, y=settings.WINDOW_HEIGHT - 15, anchor_x='center', anchor_y='center')
       self.user_left = user(pyglet.resource.image(settings.user_IMG)).center_anchor_y(settings.WINDOW_HEIGHT)
       self.user_right = user(pyglet.resource.image(settings.user_IMG)).center_anchor_y(settings.WINDOW_HEIGHT)
       self.ball = Ball(pyglet.resource.image(settings.BALL_IMG)).center_anchor_y(settings.WINDOW_HEIGHT).center_anchor_x(settings.WINDOW_WIDTH)
       self.userRight.x = settings.WINDOW_WIDTH - self.user_right.width
       self.userMe = self.userLeft 
 
    def define_players(self, serverResponse):
       if self.me == sorted(serverResponse.keys())[0]:
           self.primaryClient = True
           self.usere = self.userLeft
           self.userVs = self.userRight
           if not self.running:
               self.score.text = 'Host'
       else:
           self.userMe = self.userRight
           self.userVs = self.userLeft
           if not self.running:
               self.score.text = 'Joinee'
 
   def on_collision(self):
       player = self.ball.checkCollision([self.userLeft, self.userRight])
       if player:
           self.ball.hit_user(player is self.userLeft)
           player.increase_score()
           self.ball.prevent_stick(player)
       if self.ball.check_collision_laterals(settings.WINDOW_HEIGHT):
           self.ball.hit_lateral()
 
   def update_server_data(self, dt):
       data = {
           "ball": {
               "x": self.ball.x,
               "y": self.ball.y,
           },
           "user": {
               "x": self.userMe.x,
               "y": self.userMe.y,
           }
       }
       if self.primaryClient:
           data['score'] = [self.userLeft.SCORE, self.userRight.SCORE]
       self.conn.send(simplejson.dumps(data).encode('utf-8'))
       self.server_data = simplejson.loads(self.conn.recv(2000).decode('utf-8'))
       return self.server_data
 
   def update_multiplayer_positions(self, data):
       for playerid in data.keys():
           if playerid != self.me:
               player_data = data[playerid]
               if 'user' in player_data:
                   self.userVs.x = player_data['user']['x']
                   self.userVs.y = player_data['user']['y']
               if not self.primaryClient and 'ball' in player_data:
                   self.ball.x = player_data['ball']['x']
                   self.ball.y = player_data['ball']['y']
               if 'score' in player_data:
                   self.userLeft.SCORE = player_data['score'][0]
                   self.userRight.SCORE = player_data['score'][1]
 
   def drawMultiplayer(self):
       self.define_players(self.server_data)
 
       if len(self.server_data.keys()) == 2:
           self.run()
       else:
           self.pause()
 
       if self.primaryClient:
           self.on_collision()
 
       self.update_multiplayer_positions(self.server_data)
 
   def drawSingleplayer(self):
       self.run()
       self.on_collision()
