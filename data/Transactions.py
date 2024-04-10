import enum
import random

import discord

from data.Purse import CoinType


transaction_list = []


def get(member: str, item: str):
    for transaction in transaction_list:
        if transaction.member == member and transaction.item == item:
            return transaction
    return None


def contains(member: str, item: str) -> bool:
    for transaction in transaction_list:
        if transaction.member == member and transaction.item == item:
            return True
    return False


def remove(member: str, item: str):
    for transaction in transaction_list:
        if transaction.member == member and transaction.item == item:
            transaction_list.remove(transaction)
            return True
    return False


def transaction_list_to_str():
    result: str = ""
    for transaction in transaction_list:
        if transaction.state == TransactionState.WAITING_FOR_PRICE:
            result += f"Adventurer: {transaction.member}  ;  Item: {transaction.item}  ;  Price: Yet to be set.\n"
        else:
            result += f"Adventurer: {transaction.member}  ;  Item: {transaction.item}  ;  Price: {transaction.price} {transaction.coin_type}\n"

    if result is "":
        return "No transactions yet."
    else:
        return result


def add(member: str, item: str):
    transaction_list.append(Transaction(member, item))


class TransactionState(enum.Enum):
    WAITING_FOR_PRICE = 0
    PRICE_SET = 1


class Transaction:

    state: TransactionState
    price: int
    coin_type: CoinType

    def __init__(self, member: str, item: str):
        self.state = TransactionState.WAITING_FOR_PRICE
        self.member = member
        self.item = item
