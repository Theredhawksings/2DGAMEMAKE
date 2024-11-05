'''
class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = None
        self.transitions = {}
        self.event_que = []

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.boy, ('START', 0))

    def update(self, grass):
        self.cur_state.do(self.boy, grass)
        while len(self.event_que) > 0:
            event = self.event_que.pop(0)
            self.handle_event(event)

    def handle_event(self, e):
        for check_event, next_state in self.transitions.get(self.cur_state, {}).items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True
        return False

    def add_event(self, event):
        self.event_que.append(event)

    def set_transitions(self, transitions):
        self.transitions = transitions
'''
