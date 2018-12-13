from backend.utils.card import card_to_int
from backend.utils.jsonconvert import JsonConvert

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


@JsonConvert.register
class HandDescription:

    def __init__(self, hand_name="", value="", returned_cards=None):
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
        if self.value:
            return {"name": self.hand_name, "value": str(self.value)}
        return {"name": self.hand_name, "value": ""}
