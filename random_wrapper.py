import random
import string


class Random:
    def __init__(self):
        self.strlen = 10

    @property
    def string(self):
        chars = string.ascii_uppercase + string.digits
        return''.join(
            random.SystemRandom().choice(chars) for _ in range(self.strlen))

    @property
    def one_to_ten(self):
        return random.SystemRandom().randint(1, 10)

    @property
    def one_to_hundred(self):
        return random.SystemRandom().randint(1, 100)
