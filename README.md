# CPSC481-Project-OthelloAI


## Installation
Pygame must be installed in order to run the program, if it is not it will install a version for you

```
If on mac: python3 main.py
If on Windows: py main.py
```

## Layout
The code is split into 4 main files. 
```
- Othello-CPSC481
    - assets 
        - BlackToken.png
        - WhiteToken.png
        - grid.png
    - computerai.py
    - main.py
    - othello.py
    - player.py
```

- The main Othello gameplay is run through othello.py, and uses the classes in player.py (Player and Grid) to generate the tokens and board. 
- Within othello.py, it will call the class in computerai.py in order to run through the AI for each turn. 
- Within the assets will be the items that render for the different tokens, and the grid. 


## To change the functionality of the code 
Look into the othello.py initializations to switch from "Player vs AI" to "AI vs AI", or change the depths of the two AI's (Player 1 is Black, Player 2 is White)
```
        self.ai_vs_ai = False  # Set this to True for AI vs AI mode

        self.ai1_depth = 5 # Depth for AI Player 1
        self.ai2_depth = 5  # Depth for AI Player 2
```


