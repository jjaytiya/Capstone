import os
import csv
import random
from pypokerengine.api.game import setup_config, start_poker
from pypokerengine.players import BasePokerPlayer

# GLOBAL LOGGER: This will store all states from all hands until we write them out.
game_states_log = []

class LoggingRandomPlayer(BasePokerPlayer):
    def __init__(self, player_id):
        super().__init__()
        self.player_id = player_id

    def declare_action(self, valid_actions, hole_card, round_state):
        street = round_state['street']  # "preflop", "flop", "turn", or "river"
        community_card = round_state['community_card']
        pot = round_state['pot']['main']['amount']
        player_states = round_state['seats']

        # Find this player's stack and seat info
        my_seat = next(seat for seat in player_states if seat['uuid'] == self.uuid)
        my_stack = my_seat['stack']
        my_name = my_seat['uuid'][:5]  # Limit name to 5 characters

        # Choose a random valid action
        chosen_action = random.choice(valid_actions)
        action_type = chosen_action["action"]

        if action_type == "raise":
            chosen_action["amount"] = random.randint(chosen_action["amount"]["min"], chosen_action["amount"]["max"])

        action_amount = chosen_action.get("amount", 0)

        # Record actions taken so far
        actions_this_street = round_state.get('action_histories', {}).get(street, [])
        action_str = ";".join(
            f"{a['uuid']}:{a['action']}:{a.get('amount', 0)}" for a in actions_this_street
        )

        # Combine hole cards and community cards into strings
        hole_str = ",".join(hole_card)  # Combine ranks and suits like '7D', '10H'
        community_str = ",".join(community_card)

        # Save the current state to the global log
        game_states_log.append({
            "round": street,
            "acting_player": my_name,
            "action": action_type,
            "action_amount": action_amount,
            "hole_cards": hole_str,
            "community_cards": community_str,
            "pot": pot,
            "stacks": ";".join(str(p['stack']) for p in player_states),
            "actions_this_street": action_str
        })

        return chosen_action["action"], action_amount

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def main():
    global game_states_log

    configurations = [
        {"max_round": 100, "initial_stack": 5000, "small_blind_amount": 100},
        {"max_round": 100, "initial_stack": 20000, "small_blind_amount": 200},
        {"max_round": 100, "initial_stack": 100000, "small_blind_amount": 500},
        {"max_round": 100, "initial_stack": 200000, "small_blind_amount": 1000}
    ]

    fieldnames = [
        "config_id", "round", "acting_player",
        "action", "action_amount",
        "hole_cards", "community_cards",
        "pot", "stacks", "actions_this_street"
    ]

    all_game_states = []

    num_games_per_config = 1000 // len(configurations)

    for config_id, config_values in enumerate(configurations):
        for _ in range(num_games_per_config):
            config = setup_config(
                max_round=config_values["max_round"],
                initial_stack=config_values["initial_stack"],
                small_blind_amount=config_values["small_blind_amount"]
            )

            for i in range(4):
                player = LoggingRandomPlayer(player_id=f"p{i+1}")
                config.register_player(name=f"p{i+1}", algorithm=player)

            game_states_log = []
            start_poker(config, verbose=0)

            for state in game_states_log:
                state["config_id"] = config_id
                all_game_states.append(state)

    os.makedirs("../datasets", exist_ok=True)

    with open("../datasets/poker_states.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_game_states)


if __name__ == "__main__":
    main()
