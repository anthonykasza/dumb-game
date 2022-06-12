// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./SafeMath.sol";

contract Game {
  using SafeMath for uint256;

  // 0 -> more players need to join
  // 1 -> game is playable. go go go!
  // 2 -> game is over
  uint public gameState = 0;

  enum PlayerStates { READY, BRACED, LUNGED }

  struct Player {
    // attack. how much damage you inflict
    uint ak;

    // defense. how much attacks affect your hp
    uint de;

    // agility. how quickly you can do things
    uint ag;

    // health points. once your hp is zero or less, you're dead
    uint hp;

    // how lucky you are. players are rewarded for registering early.
    // because players that register later are able to see their opponents stats.
    uint luck;

    // the state of the player
    PlayerStates playerState;

    // the block in which the player took its previous action
    uint prevActionBlock;
  }
  
  uint constant statsAllowance = 20;
  uint constant maxPlayers = 4;
  uint256 constant gameCost = 5 wei;

  address[maxPlayers] public players;
  mapping (address => Player) public ownerToPlayer;
  uint public playerCount = 0;
  address public winner;

  modifier canAct () {
    require(ownerToPlayer[msg.sender].hp > 0, "you're zed. zed's dead baby.");
    require(gameState == 1, "the game isn't playable");
    _;
  }

  // TODO: set params at contract creation instead of using constants
  constructor() {}

  function registerPlayer(uint _ak, uint _de, uint _ag, uint _hp) public payable returns (bool) {
    require (_hp > 0, "cannot create a dead player");
    require(ownerToPlayer[msg.sender].hp == 0, "you are already playing the game");
    require(playerCount <= maxPlayers, "max players already playing the game");
    require(_ak.add(_de).add(_ag).add(_hp) <= statsAllowance, "you're stats are over the player allowance");
    require(msg.value >= gameCost, "it costs more than that to play the game");
    require(gameState == 0, "game has already begun");

    players[playerCount] = msg.sender;
    // for some reason safemath doesn't work when calling `0.add(1)`
    playerCount += 1;

    ownerToPlayer[msg.sender] = Player({
      ak: _ak,
      de: _de,
      ag: _ag,
      hp: _hp,
      luck: maxPlayers.sub(playerCount),
      playerState: PlayerStates.READY,
      prevActionBlock: 0
    });

    if (playerCount == maxPlayers) {
      gameState = 1;
    }

    return true;
  }

  function brace() canAct public {
    Player storage bracingPlayer = ownerToPlayer[msg.sender];

    updatePlayerState(bracingPlayer);
    require(bracingPlayer.playerState == PlayerStates.READY, "you're already braced, wait a few blocks");
    require(bracingPlayer.playerState == PlayerStates.READY, "you just hit somebody, stay LUNGED for a while");

    bracingPlayer.playerState = PlayerStates.BRACED;
    bracingPlayer.prevActionBlock = block.number;
  }

  function hit(address _target) canAct public {
    require(_target != msg.sender, "stop hitting yourself");
    require(ownerToPlayer[_target].hp > 0, "no sense in beating a dead horse");

    Player storage attackingPlayer = ownerToPlayer[msg.sender];
    updatePlayerState(attackingPlayer);
    require(attackingPlayer.playerState == PlayerStates.READY, "you ain't READY to hit nobody");

    Player storage defendingPlayer = ownerToPlayer[_target];
    updatePlayerState(defendingPlayer);

    // TODO: based on a player's luck a hit can result in 3 outcomes:
    //  1. a hit misses the defending player. The attacking player still ends up LUNGED
    //  2. a hit disregards the defending player's BRACE status and defense points. A direct hit.
    //  3. a hit which incorporates the defending player's BRACE status and defense points. A normal hit.
    // TODO: consider how this randomness will affect tests.. maybe we can seed chainlink VRF?

    uint offensePoints = attackingPlayer.ak.add(attackingPlayer.luck);
    uint defensePoints = defendingPlayer.de.add(defendingPlayer.luck);

    uint damage = 0;
    if (defendingPlayer.playerState == PlayerStates.BRACED && defensePoints > 0) {
      damage = offensePoints.div(defensePoints);
    } else {
      damage = offensePoints.sub(defensePoints);
    }

    defendingPlayer.playerState == PlayerStates.READY;
    attackingPlayer.playerState = PlayerStates.LUNGED;
    attackingPlayer.prevActionBlock = block.number;

    if (damage >= defendingPlayer.hp) {
      defendingPlayer.hp = 0;
      checkForWinner();
    } else {
      defendingPlayer.hp.sub(damage);
    }
  }

  function updatePlayerState(Player storage _player) internal {
    uint braceDuration = 5;
    if (_player.playerState == PlayerStates.LUNGED) {
      if (block.number - _player.prevActionBlock >= statsAllowance - _player.ag) {
        _player.playerState = PlayerStates.READY;
      }
    } else if (_player.playerState == PlayerStates.BRACED) {
      if (block.number - _player.prevActionBlock > braceDuration) {
       _player.playerState = PlayerStates.READY;
      }
    }
  }

  function checkForWinner() public {
    require(gameState == 1, "game is not in a playable state");
    require(winner == address(0x0), "game is over. call winner() getter function to see who won");
    uint loserCount = 0;
    for (uint i=0; i<maxPlayers; i++) {
      address playerAddress = players[i];
      if (ownerToPlayer[playerAddress].hp == 0) {
        loserCount++;
      }
    }
    if (loserCount == maxPlayers.sub(1)) {
      gameState = 2;
      winner = msg.sender;
      payable(winner).transfer(address(this).balance);
    }
  }


}
