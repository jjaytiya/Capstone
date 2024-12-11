import csv
import uuid
import random
import os
from pypokerengine.api.game import setup_config, start_poker
from pypokerengine.players import BasePokerPlayer

global_data = []
global_game_id = str(uuid.uuid4())
global_player_hands = {}

class MyRandomPlayer(BasePokerPlayer):
    def __init__(self, name, sb_amount, master=None):
        super().__init__()
        self.name = name
        self.sb_amount = sb_amount
        self.bb_amount = sb_amount * 2
        self.current_round_count = None
        self.initial_stack = None
        self.master = master

    def declare_action(self, valid_actions, hole_card, round_state):
        action = random.choice([a['action'] for a in valid_actions])
        global_player_hands[self.name] = hole_card
        if action == 'raise':
            pot_amount = sum([p['amount'] for p in round_state['pot'].values() if 'amount' in p])
            possible_fractions = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            fraction = random.choice(possible_fractions)
            chosen_amount = int(pot_amount * fraction)
            for va in valid_actions:
                if va['action'] == 'raise':
                    min_r = va['amount']['min']
                    max_r = va['amount']['max']
                    chosen_amount = max(min_r, min(chosen_amount, max_r))
                    break
            return action, chosen_amount
        elif action == 'call':
            for va in valid_actions:
                if va['action'] == 'call':
                    return action, va['amount']
        else:
            return 'fold', 0

    def receive_game_start_message(self, game_info):
        # Save initial stack
        for seat in game_info['seats']:
            if seat['uuid'] == self.uuid:
                self.initial_stack = seat['stack']
                break

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.current_round_count = round_count

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action_info, round_state):
        acting_player_uuid = action_info['player_uuid']
        acting_player_name = self.find_player_name_by_uuid(acting_player_uuid, round_state['seats'])

        pot_amount = sum([p['amount'] for p in round_state['pot'].values() if 'amount' in p])
        street = round_state['street']
        hole_cards = self.get_player_hole_cards(acting_player_name)
        community_cards = round_state['community_card']
        player_stack = self.get_player_stack(acting_player_name, round_state['seats'])

        record = {
            'game_id': global_game_id,
            'hand_id': self.current_round_count,
            'round_index': street,
            'player_name': acting_player_name,
            'action': action_info['action'],
            'amount': action_info['amount'],
            'hole_cards': "-".join(self.card_to_str(c) for c in hole_cards) if hole_cards else "",
            'community_cards': "-".join(self.card_to_str(c) for c in community_cards),
            'pot': pot_amount,
            'player_stack': player_stack,
            'small_blind': self.sb_amount,
            'big_blind': self.bb_amount,
            # Initialize winner as empty; we'll fill it in once the round ends
            'winner': ""
        }
        if self.master:
            global_data.append(record)

    def receive_round_result_message(self, winners, hand_info, round_state):
        # At the end of the round, we know who won.
        # winners is a list of dicts: [{'uuid':..., 'name':..., 'stack':...}, ...]
        winner_names = [w['name'] for w in winners]
        winner_str = "-".join(winner_names)
        # Update all actions for this hand_id with the winner info
        for row in global_data:
            if row['hand_id'] == self.current_round_count:
                row['winner'] = winner_str

    def find_player_name_by_uuid(self, uuid, seats):
        for s in seats:
            if s['uuid'] == uuid:
                return s['name']
        return None

    def get_player_stack(self, player_name, seats):
        for s in seats:
            if s['name'] == player_name:
                return s['stack']
        return None

    def get_player_hole_cards(self, acting_player_name):
        return global_player_hands.get(acting_player_name)

    @staticmethod
    def card_to_str(card):
        # Handle both dict and string formats
        if isinstance(card, dict):
            return card['rank'] + card['suit']
        elif isinstance(card, str):
            return card
        return str(card)


def simulate_and_collect_data(
    num_games=1,
    max_round=4,  # Set max_round to 4 for Texas Hold'em
    initial_stack=1000,
    small_blind_amount=10,
    output_csv="poker_data.csv",
    player_names=None
):
    global global_data, global_game_id
    global_data = []

    if player_names is None:
        player_names = ["P1", "P2", "P3", "P4"]

    config = setup_config(max_round=max_round, initial_stack=initial_stack, small_blind_amount=small_blind_amount)
    for name in player_names:
        config.register_player(name=name, algorithm=MyRandomPlayer(name, small_blind_amount, master=name==player_names[0]))

    for _ in range(num_games):
        global_game_id = str(uuid.uuid4())
        start_poker(config, verbose=0)

    fieldnames = [
        'game_id', 'hand_id', 'round_index', 'player_name', 'action', 'amount',
        'hole_cards', 'community_cards', 'pot', 'player_stack', 'small_blind', 'big_blind', 'winner'
    ]

    os.makedirs("../datasets", exist_ok=True)

    with open("../datasets/improved_poker_states.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(global_data)


if __name__ == "__main__":
    simulate_and_collect_data(
        num_games=1000,  # Set number of games to 1000
        max_round=4,  # Set max round to 4 for Texas Hold'em
        initial_stack=1000,
        small_blind_amount=10,
        output_csv="poker_data.csv",
        player_names=["Alice", "Bob", "Carol", "Dave"]
    )
