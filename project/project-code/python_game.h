#ifndef _GAME1_H__
#define _GAME1_H__

#include <vector>

class Player;
class PlayerView;
class Game;

enum Move {
  UP,
  LEFT,
  DOWN,
  RIGHT,
};

enum PlantStatus {
  STATUS_UNKNOWN_PLANT,
  STATUS_NO_PLANT,
  STATUS_NUTRITIOUS_PLANT,
  STATUS_POISONOUS_PLANT,
};

typedef std::vector<int> Image;

// Interface that will be exposed to the python code.
class GameInterface {
 public:
  GameInterface(int plant_bonus,
                int plant_penalty,
                int observation_cost,
                int starting_life,
                int life_per_turn);
  void StartGame();
  void ExecuteMoves(Move player1, bool eat1, Move player2, bool eat2);
  PlayerView* GetPlayer1View();
  PlayerView* GetPlayer2View();
};

class PlayerView {
 public:
  int GetLife();
  int GetXPos();
  int GetYPos();
  int GetRound();
  // Returns an image for the plant in a flat vector.
  // The image is actually a 6x6 image, but you can think of the first 6
  // elements as row 1, the next 6 as row 2, etc.
  Image GetImage();

  // Returns the plant information for the current square.
  PlantStatus GetPlantInfo();
};

int curses_init();
void curses_close();
void curses_draw_board(GameInterface* game);
void curses_center_cursor();
void curses_init_round(GameInterface* game);
void curses_declare_winner(int winner_id);
void curses_debug(int player, char* str);

#endif
