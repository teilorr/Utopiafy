import random
import queue
from collections import defaultdict

Chain = defaultdict[str, defaultdict[str, int]]

class MarkovModel:
    def __init__(self, texts: str):
        self.texts = texts

    def get_tokens(self) -> list[str]:
        return self.texts.split()

    def create_markov_chain(self, tokens: list[str], state_size: int) -> Chain:
        if state_size > len(tokens):
            raise Exception("State size should be greater than the number of tokens.")

        markov_chain = defaultdict(lambda: defaultdict(int))
        state_queue = queue.Queue()
        for i, token in enumerate(tokens):
            if i < state_size:
                state_queue.put(token)
                if i == state_size - 1:
                    current_state = " ".join(list(state_queue.queue))

            elif i < len(tokens):
                state_queue.get()
                state_queue.put(token)
                next_state = " ".join(list(state_queue.queue))
                markov_chain[current_state][next_state] += 1
                current_state = next_state
        return markov_chain

    def _get_random_state(self, markov_chain: Chain) -> str:
        uppercase_states = [
            state for state in markov_chain.keys() if state[0].isupper()
        ]
        if len(uppercase_states) == 0:
            return random.choice(list(markov_chain.keys())).title()
        return random.choice(uppercase_states)

    def _get_next_state(self, markov_chain: Chain, state: str) -> str:
        next_states = list(markov_chain[state].keys())
        weights = list(markov_chain[state].values())

        next_state = random.choices(next_states, weights=weights, k=1)
        return next_state[0]

    def generate_text(self, markov_chain: Chain, words: int) -> str:
        state = self._get_random_state(markov_chain)
        text = state.split()
        while len(text) < words:
            state = self._get_next_state(markov_chain, state)
            if state is None:
                state = self._get_random_state(markov_chain)
            text.append(state.split()[-1])
        return " ".join(text)