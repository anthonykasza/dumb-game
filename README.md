A dumb game in solidity to better learn solidity, brownie, and hardhat.


The game has a configurable maximum number of addresses which can play at any time. The examples and tests use 4 addresses.
Each address registers a Player using a configurable points budget to create their player. The tests and examples use a budget of 20 points.
Points can be applied to the following Player attributes:
- attack
- defense
- health
- agility

Players who register before others are at a slight disadvantage as their attribute budget can be read by other Players. This disadvantage is balanced by providing luck points according to which Player registered earliest.

Once the maximum number of Players is created, the game begins and Players may submit actions. Currently actions include:
- brace
- hit

The game operates in real-time, measured in mined blocks. Each action require a certain number of blocks to be mined before a Player may take another action.
The game is structured as a free-for-all and assumes no collusion.

The object of the game is to be the last player with health point balance greater than zero.

Future ideas include:
- incorporating random chance into actions
- expanding the set of actions a Player may take
- including mechanisms to alter attribute points, besides decrementing health, during game-play
- randomize everything and have bots play each other to find optimal strategies
