class Loot_table():
    def __init__(self, list):
        self.list = list
    def choose_from_list(self):
        random.seed()
        percent_absolute = []
        percent_cumulative = []
        cumulative = 0
        chosen = None
        for percent in self.list:
            percent_absolute.append(percent['percent'])
            percent_cumulative.append(percent['percent'] + cumulative)
            cumulative += percent['percent']
            
        default = 1 - cumulative
        
        random_num = random.random()
        for i, percent in enumerate(percent_cumulative):
            if percent > random_num:
                chosen = self.list[i]
                break
        
        return(chosen)