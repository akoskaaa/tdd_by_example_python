

class Expression(object):

    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

    def reduce(self, bank, to):
        pass

    def times(self, multiplier):
        pass


class Sum(Expression):

    def reduce(self, bank, to):
        amount = self.augend.reduce(bank, to).amount + self.addend.reduce(bank, to).amount
        return Money(amount, to)

    def plus(self, addend):
        return Sum(self, addend)

    def times(self, multiplier):
        return Sum(self.augend.times(multiplier), self.addend.times(multiplier))


class Money(Expression):

    def __init__(self, amount, currency):
        self._amount = amount
        self._currency = currency

    @property
    def amount(self):
        return self._amount

    def currency(self):
        return self._currency

    def equals(self, other):
        return self._amount == other.amount and self._currency == other._currency

    def times(self, multiplier):
        return Money(self._amount * multiplier, self._currency)

    def plus(self, addend):
        return Sum(self, addend)

    def reduce(self, bank, to):
        rate = bank.rate(self._currency, to)
        return Money(self._amount / rate, to)

    @staticmethod
    def dollar(amount):
        return Money(amount, 'USD')

    @staticmethod
    def franc(amount):
        return Money(amount, 'CHF')


class Bank(object):

    def __init__(self):
        self.rates = {}

    def add_rate(self, from_currency, to_currency, rate):
        self.rates[(from_currency, to_currency)] = rate

    def reduce(self, source, to):
        return source.reduce(self, to)

    def rate(self, from_currency, to_currency):
        if from_currency == to_currency:
            return 1
        return self.rates[(from_currency, to_currency)]
