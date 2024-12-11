## 📘 Data Dictionary


| **Field Name**         | **Description**                                                                                                                                           |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `game_id`              | Unique identifier for each game (UUID)                                                                                                                     |
| `hand_id`              | The current round count (hand_id)                                                                                                                          |
| `round_index`          | The current street (e.g., pre-flop, flop, turn, river)                                                                                                     |
| `player_name`          | The name of the player taking the action                                                                                                                   |
| `action`               | The action taken by the player (e.g., 'call', 'raise', 'fold')                                                                                           |
| `amount`               | The amount of money involved in the action (for raise or call)                                                                                             |
| `hole_cards`           | Hole cards of the player, represented as a string of card values (e.g., '2H-3D') if available                                                            |
| `community_cards`      | Community cards at that point in the round, represented as a string of card values (e.g., '5H-7S-9C')                                                    |
| `pot`                  | The total amount of money in the pot at that point                                                                                                         |
| `player_stack`         | The remaining stack of the player after the action                                                                                                        |
| `small_blind`          | The small blind amount                                                                                                                                    |
| `big_blind`            | The big blind amount                                                                                                                                      |
| `winner`               | The winner of the round (empty until determined at the round's end)                                                                                      |

This structure captures all key information for each action taken during the game. Let me know if you'd like to add or adjust anything!
