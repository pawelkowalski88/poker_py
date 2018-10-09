from card import card_to_int

hand_ranking = {
"High card": 1,
"Pair": 2,
"Two pairs": 3,
"Three of a kind": 4,
"Straight": 5,
"Flush": 6,
"Full house": 7,
"Four of a kind": 8,
"Straight flush": 9}

class HandDescription():

    def __init__(self, hand_name, value, returned_cards):
        self.hand_name = hand_name
        self.value = value
        self.returned_cards = returned_cards

    def __gt__(self, other):
        if isinstance(other, HandDescription):
            if hand_ranking[self.hand_name] == hand_ranking[other.hand_name]:
                if not self.value or not other.value:
                    return False 
                return card_to_int(self.value) > card_to_int(other.value)
            return hand_ranking[self.hand_name] > hand_ranking[other.hand_name]
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, HandDescription):
            if hand_ranking[self.hand_name] == hand_ranking[other.hand_name]:
                if not self.value and not other.value:
                    return True
                if not self.value or not other.value:
                    return False
                return card_to_int(self.value) == card_to_int(other.value)
            return False
        return NotImplemented
    
    def as_values(self):
        return [hand_ranking[self.hand_name], self.value]

    def as_name_and_value(self):
        return [self.hand_name, self.value]

                