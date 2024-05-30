import enum

from data.Purse import CoinType


class TransactionState(enum.Enum):
    WAITING_FOR_PRICE = 0
    PRICE_SET = 1


class TransactionType(enum.Enum):
    BUY = 0
    SELL = 1

    @staticmethod
    def enum_from_str(transaction_type: str):
        transaction_type = transaction_type.upper()
        if transaction_type == "BUY":
            return TransactionType.BUY
        elif transaction_type == "SELL":
            return TransactionType.SELL
        else:
            return None


class Transaction:

    state: TransactionState
    price: int
    coin_type: CoinType
    transaction_type: TransactionType

    def __init__(self, member: str, item: str, amount: int, transaction_type: TransactionType):
        self.state = TransactionState.WAITING_FOR_PRICE
        self.member = member
        self.item = item
        self.amount = amount
        self.transaction_type = transaction_type


transaction_list = []


def get(member: str, item: str, transaction_type: TransactionType) -> Transaction | None:
    for transaction in transaction_list:
        if transaction.member == member and transaction.item == item and transaction_type == transaction.transaction_type:
            return transaction
    return None


def contains(member: str, item: str, transaction_type: TransactionType) -> bool:
    for transaction in transaction_list:
        if transaction.member == member and transaction.item == item and transaction_type == transaction.transaction_type:
            return True
    return False


def remove(member: str, item: str, transaction_type: TransactionType) -> bool:
    for transaction in transaction_list:
        if transaction.member == member and transaction.item == item and transaction_type == transaction.transaction_type:
            transaction_list.remove(transaction)
            return True
    return False


def transaction_list_to_str() -> str:
    result: str = ""
    for transaction in transaction_list:
        if transaction.state == TransactionState.WAITING_FOR_PRICE:
            result += f"Adventurer: {transaction.member}  ; {transaction.transaction_type} {transaction.amount} item(s): {transaction.item}  ;  Price: Yet to be set.\n"
        else:
            result += f"Adventurer: {transaction.member}  ; {transaction.transaction_type} {transaction.amount} item(s): {transaction.item}  ;  Price: {transaction.price} {transaction.coin_type}\n"

    if result == "":
        return "No transactions yet."
    else:
        return result


def add(member: str, item: str, amount: int, transaction_type: TransactionType):
    transaction_list.append(Transaction(member, item, amount, transaction_type))
