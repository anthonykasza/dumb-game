// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./SafeMath.sol";

contract Game {
  using SafeMath for uint256;

  // 0 -> more players need to join
  // 1 -> game is playable. go go go!
  // 2 -> game is over
  uint public gameState = 0;

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
    // because players that register later are able to see their stats.
    uint luck;
  }
  
  uint constant playerAllowance = 20;
  uint constant maxPlayers = 4;
  uint256 constant gameCost = 5 wei;

  address[maxPlayers] public players;
  mapping (address => Player) public ownerToPlayer;
  uint public playerCount = 0;
  uint public losers = 0;
  address public winner;

  // TODO: set params at contract creation instead of using constants
  constructor() {}

  function registerPlayer(uint _ak, uint _de, uint _ag, uint _hp) public payable returns (bool) {
    // players can register themselves with 0 HP then re-register themselves with different stats after they see how other players have registered.
    //  however this would cost them their luck points and they'd have to pay more to play the game
    require(ownerToPlayer[msg.sender].hp == 0, "you are already playing the game");
    require(playerCount <= maxPlayers, "max players already playing the game");
    require(_ak.add(_de).add(_ag).add(_hp) <= playerAllowance, "you're stats are over the allowance");
    require(msg.value >= gameCost, "it costs more than that to play the game");
    require(gameState == 0, "game has already begun");

    // for some reason safemath doesn't work when calling `0.add(1)`
    players[playerCount] = msg.sender;
    playerCount += 1;

    ownerToPlayer[msg.sender] = Player({
      ak: _ak,
      de: _de,
      ag: _ag,
      hp: _hp,
      luck: maxPlayers.sub(playerCount)
    });

    if (playerCount == maxPlayers) {
      gameState = 1;
    }

    return true;
  }

  // TODO: incorporate agility so that each player's actions are throttled based on how many blocks have passed
  // TODO: create more actions besides `hit`, like `brace` which would reduce damage

  // what happens when a player is targeted by multiple hits in a single block?
  function hit(address _target) public {
    require(gameState == 1);
    require(ownerToPlayer[msg.sender].hp > 0);

    Player storage defendingPlayer = ownerToPlayer[_target];
    Player storage attackingPlayer = ownerToPlayer[msg.sender];

    // TODO: do something with luck involving random numbers such that hits could miss
    uint offensePoints = attackingPlayer.ak.add(attackingPlayer.luck);
    uint defensePoints = defendingPlayer.de.add(defendingPlayer.luck);
    uint damage = offensePoints.sub(defensePoints);

    if (damage >= defendingPlayer.hp) {
      defendingPlayer.hp = 0;
      losers += 1;
      if (losers == maxPlayers.sub(1)) {
        gameState = 2;
        winner = msg.sender;
        payable(winner).transfer(address(this).balance);
      }
    } else {
      defendingPlayer.hp.sub(damage);
    }
  }

}
