// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Game {
  using SafeMath for uint256;

  enum GAME_STATE { PENDING, PLAYABLE, COMPLETED }
  GAME_STATE public gameState;

  enum PLAYER_STATE { READY, BRACED, LUNGED }

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
    PLAYER_STATE playerState;

    // the block in which the player took its previous action
    uint prevActionBlock;
  }
  
  uint public statsAllowance;
  uint public maxPlayers;
  uint256 public gameCost;

  mapping (address => Player) public ownerToPlayer;
  uint public playerCount = 0;
  address public winner;
  address[] public players;

  modifier canAct () {
    require(ownerToPlayer[msg.sender].hp > 0, "you're zed. zed's dead baby.");
    require(gameState == GAME_STATE.PLAYABLE, "the game isn't playable");
    _;
  }

  constructor(uint _statsAllowance, uint _maxPlayers, uint _gameCost) {
    gameState = GAME_STATE.PENDING;
    statsAllowance = _statsAllowance;
    maxPlayers = _maxPlayers;
    gameCost = _gameCost;
  }

  function registerPlayer(uint _ak, uint _de, uint _ag, uint _hp) public payable returns (bool) {
    require (_hp > 0, "cannot create a dead player");
    require(ownerToPlayer[msg.sender].hp == 0, "you are already playing the game");
    require(playerCount <= maxPlayers, "max players already playing the game");
    require(_ak.add(_de).add(_ag).add(_hp) <= statsAllowance, "you're stats are over the player allowance");
    require(msg.value >= gameCost, "it costs more than that to play the game");
    require(gameState == GAME_STATE.PENDING, "game has already begun");

    players.push(msg.sender);
    // for some reason safemath doesn't work when calling `0.add(1)`
    playerCount += 1;

    ownerToPlayer[msg.sender] = Player({
      ak: _ak,
      de: _de,
      ag: _ag,
      hp: _hp,
      luck: maxPlayers.sub(playerCount),
      playerState: PLAYER_STATE.READY,
      prevActionBlock: 0
    });

    if (playerCount == maxPlayers) {
      gameState = GAME_STATE.PLAYABLE;
    }

    return true;
  }

  function brace() canAct public {
    Player storage bracingPlayer = ownerToPlayer[msg.sender];

    updatePlayerState(bracingPlayer);
    require(bracingPlayer.playerState == PLAYER_STATE.READY, "you're already braced, wait a few blocks");
    require(bracingPlayer.playerState == PLAYER_STATE.READY, "you just hit somebody, stay LUNGED for a while");

    bracingPlayer.playerState = PLAYER_STATE.BRACED;
    bracingPlayer.prevActionBlock = block.number;
  }

  function hit(address _target) canAct public {
    require(_target != msg.sender, "stop hitting yourself");
    require(ownerToPlayer[_target].hp > 0, "no sense in beating a dead horse");

    Player storage attackingPlayer = ownerToPlayer[msg.sender];
    updatePlayerState(attackingPlayer);
    require(attackingPlayer.playerState == PLAYER_STATE.READY, "you ain't READY to hit nobody");

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
    if (defendingPlayer.playerState == PLAYER_STATE.BRACED && defensePoints > 0) {
      damage = offensePoints.div(defensePoints);
    } else {
      damage = offensePoints.sub(defensePoints);
    }

    defendingPlayer.playerState == PLAYER_STATE.READY;
    attackingPlayer.playerState = PLAYER_STATE.LUNGED;
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
    if (_player.playerState == PLAYER_STATE.LUNGED) {
      if (block.number - _player.prevActionBlock >= statsAllowance - _player.ag) {
        _player.playerState = PLAYER_STATE.READY;
      }
    } else if (_player.playerState == PLAYER_STATE.BRACED) {
      if (block.number - _player.prevActionBlock > braceDuration) {
       _player.playerState = PLAYER_STATE.READY;
      }
    }
  }

  function checkForWinner() public {
    require(gameState == GAME_STATE.PLAYABLE, "game is not in a playable state");
    require(winner == address(0x0), "game is over. call winner() getter function to see who won");
    uint loserCount = 0;
    for (uint i=0; i<maxPlayers; i++) {
      address playerAddress = players[i];
      if (ownerToPlayer[playerAddress].hp == 0) {
        loserCount++;
      }
    }
    if (loserCount == maxPlayers.sub(1)) {
      gameState = GAME_STATE.COMPLETED;
      winner = msg.sender;
      payable(winner).transfer(address(this).balance);
    }
  }


}
