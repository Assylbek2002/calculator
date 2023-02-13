from datetime import date as time
import datetime

DATE_FORMAT = '%d.%m.%Y'
TODAY_DATE = time.today()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        total_waste = 0
        for record in self.records:
            if record.date == TODAY_DATE:
                total_waste += record.amount
        return total_waste

    def get_week_stats(self):
        total_week = 0
        start_week_date = TODAY_DATE - datetime.timedelta(days=7)
        for record in self.records:
            if TODAY_DATE >= record.date > start_week_date:
                total_week += record.amount
        return total_week


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        waste_total = self.get_today_stats()
        remained_calories = self.limit - waste_total
        if self.limit > remained_calories > 0:
            return f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remained_calories} кКал"
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 73.11
    EURO_RATE = 78.21

    currency_dict = {
        'usd': 'USD',
        'eur': 'Euro',
        'rub': 'руб'
    }

    def get_today_cash_remained(self, currency):
        currency_limit = {
            'rub': self.limit,
            'usd': self.limit / CashCalculator.USD_RATE,
            'eur': self.limit / CashCalculator.EURO_RATE
        }
        waste_total = self.get_today_stats()
        remained_money = currency_limit['rub'] - waste_total
        remained_dict = {
            'rub': remained_money,
            'usd': remained_money / CashCalculator.USD_RATE,
            'eur': remained_money / CashCalculator.EURO_RATE
        }
        if remained_money == 0:
            return "Денег нет, держись"
        elif currency_limit[currency] > remained_dict[currency] > 0:
            return f"На сегодня осталось {round(remained_dict[currency], 2)} {CashCalculator.currency_dict[currency]}"
        else:
            return f"Денег нет, держись: твой долг - {abs(round(remained_dict[currency], 2))} {CashCalculator.currency_dict[currency]}"


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = datetime.datetime.strptime(date, DATE_FORMAT).date()
        else:
            self.date = TODAY_DATE
