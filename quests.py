import copy

from item import Weapon, Armour, Consumable, Item

class Quest:
    def __init__(self, name, dialogue, decline, level, steps=[], rewards=[], current_step = 0):
        self.name = name
        self.dialogue = dialogue
        self.decline = decline
        self.level = level
        self.steps = copy.deepcopy(steps)
        self.rewards = copy.deepcopy(rewards)
        self.current_step = current_step
        
        for step in self.steps:
            steps.append(step)
        
        for reward in self.rewards:
            rewards.append(reward)
    
    def get_dialogue(self):
        return self.steps[self.current_step]['dialogue']
    
    def advance_step(self):
        if len(self.steps) - 1 > self.current_step:
            self.current_step += 1
            return True
        else:
            return False