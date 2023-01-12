class Player:
    def __init__(self, strategy, initial_state):
        self.index = None
        self.score = 0
        self.memory_size = 1
        self.strategy = strategy
        self.initial_state = initial_state
