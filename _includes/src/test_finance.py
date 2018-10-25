class Employee:
    def __init__(self, salary):
        self.salary = salary

    def give_a_raise(self, increase):
        self.salary += increase


from hypothesis import given
from hypothesis import strategies as st


money_strategy = st.floats(min_value=1, max_value=1000000, allow_nan=False, allow_infinity=False)


@given(money_strategy, money_strategy, money_strategy)
def test_bonus_distribution(salary1, salary2, bonus_fund):
    e1 = Employee(salary1)
    e2 = Employee(salary2)
    increase1 = bonus_fund / 2
    increase2 = bonus_fund - increase1
    e1.give_a_raise(increase1)
    e2.give_a_raise(increase2)
    money_spent = e1.salary - salary1 + e2.salary - salary2
    assert bonus_fund == money_spent
