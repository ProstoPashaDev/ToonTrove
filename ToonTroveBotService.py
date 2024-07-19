import random


class ToonTroveBotService:

    def __init__(self):
        self.common = (1, 60)
        self.rare = (60, 85)
        self.epic = (85, 95)
        self.legend = (95, 101)

    def get_card(self):
        # [*, *)
        card_type = random.randint(1, 100)
        amount = self.get_amount()
        common_amount = amount[0]
        rare_amount = amount[1]
        epic_amount = amount[2]
        legend_amount = amount[3]
        card_name = ""
        if self.common[0] <= card_type < self.common[1]:
            card_name = f"1_{random.randint(1, common_amount)}"
        elif self.rare[0] <= card_type < self.rare[1]:
            card_name = f"2_{random.randint(1, rare_amount)}"
        elif self.epic[0] <= card_type < self.epic[1]:
            card_name = f"3_{random.randint(1, epic_amount)}"
        elif self.legend[0] <= card_type < self.legend[1]:
            card_name = f"4_{random.randint(1, legend_amount)}"
        return card_name + ".jpg"

    def get_amount(self):
        file_amount = open("get_card.properties", "r")
        amount = []
        for i in range(4):
            amount.append(int(file_amount.readline().strip()[-1]))
        return amount
