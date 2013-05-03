import lucioni_broudy_player.player
import player2.player
import game_interface
import random
import signal
import sys
import time
import traceback
from optparse import OptionParser

class TimeoutException(Exception):
  def __init__(self):
    pass

def get_move(view, cmd, options, player_id):
  def timeout_handler(signum, frame):
    raise TimeoutException()
  signal.signal(signal.SIGALRM, timeout_handler)
  signal.alarm(1)
  try: 
    (mv, eat) = cmd(view)
    # Clear the alarm.
    signal.alarm(0)
  except TimeoutException:
    # Return a random value
    # Should probably log this to the interface
    (mv, eat) = (random.randint(0, 4), False)
    error_str = 'Error in move selection (%d).' % view.GetRound()
    if options.display:
      game_interface.curses_debug(player_id, error_str)
    else:
      print error_str
  return (mv, eat)

def run(options):
  game = game_interface.GameInterface(1,#options.plant_bonus,
                                      1,#options.plant_penalty,
                                      0,#options.observation_cost,
                                      50,#options.starting_life,
                                      0)#options.life_per_turn)
  lucioni_broudy_player_view = game.GetPlayer1View()
  player2_view = game.GetPlayer2View()

  if options.display:
    if game_interface.curses_init() < 0:
      return
    game_interface.curses_draw_board(game)
  
  # Keep running until one player runs out of life.
  while True:
    (mv1, eat1) = get_move(lucioni_broudy_player_view, lucioni_broudy_player.player.get_move, options, 1)
    (mv2, eat2) = get_move(player2_view, player2.player.get_move, options, 2)

    game.ExecuteMoves(mv1, eat1, mv2, eat2)
    if options.display:
      game_interface.curses_draw_board(game)
      game_interface.curses_init_round(game)
    else:
      print mv1, eat1, mv2, eat2
      print lucioni_broudy_player_view.GetLife(), player2_view.GetLife()
    # Check whether someone's life is negative.
    l1 = lucioni_broudy_player_view.GetLife()
    l2 = player2_view.GetLife()
  
    if l1 <= 0 or l2 <= 0:
      if options.display:
        winner = 0
        if l1 < l2:
          winner = 2
        else:
          winner = 1
        game_interface.curses_declare_winner(winner)
      else:
        if l1 == l2:
          print 'Tie, remaining life: %d v. %d' % (l1, l2)
        elif l1 < l2:
          print 'Player 2 wins: %d v. %d' % (l1, l2)
        else:
          print 'Player 1 wins: %d v. %d' % (l1, l2)
      # Wait for input
      sys.stdin.read(1)
      if options.display:
        game_interface.curses_close()
      break

def main(argv):
  parser = OptionParser()
  parser.add_option("-d", action="store", dest="display", default=1, type=int,
                    help="whether to display the GUI board")
  parser.add_option("--plant_bonus", dest="plant_bonus", default=20,
                    help="bonus for eating a nutritious plant",type=int)
  parser.add_option("--plant_penalty", dest="plant_penalty", default=10,
                    help="penalty for eating a poisonous plant",type=int)
  parser.add_option("--observation_cost", dest="observation_cost", default=1,
                    help="cost for getting an image for a plant",type=int)
  parser.add_option("--starting_life", dest="starting_life", default=100,
                    help="starting life",type=int)
  parser.add_option("--life_per_turn", dest="life_per_turn", default=1,
                    help="life spent per turn",type=int)
  (options, args) = parser.parse_args()

  try:
    run(options)
  except KeyboardInterrupt:
    if options.display:
      game_interface.curses_close()
  except:
    game_interface.curses_close()
    traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
  main(sys.argv)
