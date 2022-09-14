# create ui events listener
# create UI
from queue import Queue

from game import Game
from game_events import GameEventsListener
from gameui import Screen

# game events processed asynchronously
# ui events
screen_holder = {"screen": None}
game_events_listener = GameEventsListener(screen_holder)
game = Game(game_events_listener)

ui_events = Queue()
screen = Screen(game.game_state, ui_events)
screen_holder["screen"] = screen

print('starting to listen for ui events')
game.listen(ui_events)
# screen.listen(game_events)

# in the very end
screen.start()
