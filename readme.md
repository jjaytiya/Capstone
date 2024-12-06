## 📘 Data Dictionary

Each dictionary entry represents a snapshot of a **single round's state** during a poker game. Each snapshot contains:

---

## 📘 **Data Dictionary**

| Key                  | Data Type  | Description                                                               |
|----------------------|------------|---------------------------------------------------------------------------|
| `config_id`         | **int**    | The ID representing the configuration setting (e.g., different initial stacks and small blind amounts). |
| `round`             | **str**    | The current street of the game (e.g., `"preflop"`, `"flop"`, `"turn"`, `"river"`).|
| `acting_player`     | **str**    | A unique identifier representing the player who is currently acting (UUID).  |
| `action`            | **str**    | The action the player chose to take (`"fold"`, `"call"`, `"raise"`).       |
| `action_amount`     | **int/str** | The amount associated with the action (only relevant for `"raise"` action). |
| `hole_cards`        | **str**    | A comma-separated string representing the hole cards (e.g., `"7D,4C"`).    |
| `community_cards`    | **str**    | A comma-separated string representing the community cards (e.g., `"9H,JD,3S"`).|
| `pot`               | **int**    | The total amount currently in the pot.                                    |
| `stacks`            | **str**    | A semicolon-separated string showing the stacks of all players (e.g., `"1000;1200;1500;1000"`).|
| `actions_this_street`| **str**    | A description of actions taken during the current street (e.g., `uuid1:raise:500;uuid2:call`).|

---

