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

--------------------------------------------------------------------------------------------------------------------------------------------------------------

## 📊 Modeling Performance Insight:

I have run a total of 3 models:

1. Logistic Regression
2. Random Forest
3. Neural Network

The results in all 3 models show at least 80% accuracy. However, the Random Forest model seems to be overfitting, as the training score is 99%, while the testing score is 85%.


### 📍 Logistic Regression Performance
### Accuracy **80%**

| Metric     | Class 0 | Class 1 | Class 2 |
|-------------|---------|---------|---------|
| Precision   | 0.70    | 0.84    | 0.89    |
| Recall      | 0.74    | 0.81    | 0.87    |
| F1-score    | 0.72    | 0.82    | 0.88    |
      
---
### 📍 Random Forest Performance
### Accuracy **85%**

| Metric     | Class 0 | Class 1 | Class 2 |
|-------------|---------|---------|---------|
| Precision   | 0.79    | 0.88    | 0.88    |
| Recall      | 0.78    | 0.91    | 0.85    |
| F1-score    | 0.79    | 0.90    | 0.87    |

---
### 📍 Neural Netwok Performance
### Accuracy **83%**
| Metric     | Class 0 | Class 1 | Class 2 |
|-------------|---------|---------|---------|
| Precision   | 0.76    | 0.88    | 0.86    |
| Recall      | 0.77    | 0.87    | 0.87    |
| F1-score    | 0.76    | 0.87    | 0.87    |

