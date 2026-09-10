def is_valid_amount(amount):

    return amount > 0


def format_currency(amount):

    return f"₱{amount:,.2f}"

from datetime import datetime


DAILY_WITHDRAWAL_LIMIT = 20000.0


def generate_receipt(account, transaction_type, amount, balance_after):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    receipt = (
        "========================================\n"
        "           CARTIN BANK RECEIPT\n"
        "========================================\n"
        f"Date/Time:      {timestamp}\n"
        f"Account Name:   {account.account_name}\n"
        f"Account Number: {account.account_number}\n"
        f"Account Type:   {account.get_account_type()}\n"
        "----------------------------------------\n"
        f"Transaction:    {transaction_type}\n"
        f"Amount:         {format_currency(amount)}\n"
        f"Balance After:  {format_currency(balance_after)}\n"
        "========================================\n"
        "     Thank you for banking with us!\n"
        "========================================\n"
    )

    return receipt