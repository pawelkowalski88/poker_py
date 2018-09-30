from itertools import groupby

class ABC():
    def __init__(self, val,description):
        self.val = val
        self.description = description

    def __lt__(self, other):
        if isinstance(other, ABC):
            return self.val < other.val


table = [
ABC(13, "saodjsa"),
ABC(43, "diosajf"),
ABC(6, "oijf"),
ABC(6, "hfidshf")
]
table.sort()

grouped = groupby(table)

print(table)

for g,h in grouped:
    for i in h:
        print(i)
    print()
print(grouped)
