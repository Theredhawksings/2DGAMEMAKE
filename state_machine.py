# state_machine.py
# State Event Types
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE = range(5)

def right_down(e): return e[0] == 'INPUT' and e[1] == RIGHT_DOWN
def left_down(e): return e[0] == 'INPUT' and e[1] == LEFT_DOWN
def right_up(e): return e[0] == 'INPUT' and e[1] == RIGHT_UP
def left_up(e): return e[0] == 'INPUT' and e[1] == LEFT_UP
def space_down(e): return e[0] == 'INPUT' and e[1] == SPACE

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = None
        self.prev_state = None
        self.transitions = {}

    def add_event(self, event):
        self.boy.event_queue.append(event)

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self, grass):
        self.cur_state.do(self.boy, grass)
        for event in self.boy.event_queue:
            self.handle_event(event)
        self.boy.event_queue = []

    def handle_event(self, e):
        for check_event, next_state in self.transitions.get(self.cur_state, {}).items():
            if check_event(e):
                self.prev_state = self.cur_state
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True
        return False

    def set_transitions(self, transitions):
        self.transitions = transitions

