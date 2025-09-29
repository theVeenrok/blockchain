from decimal import Decimal

from app.bootstrap import create_blockchain_node
from app.domain.entities import Transaction, Wallet
from app.domain.value_objects import Amount


def main():
    # Создаем ноду
    node, initial_wallet = create_blockchain_node()

    # Создаем пользователей
    alice = Wallet()
    bob = Wallet()

    # Alice отправляет транзакцию
    tx = Transaction(
        sender=alice,
        recipient=bob,
        amount=Amount(Decimal("10.0")),
        fee=Amount(Decimal("0.1"))
    )

    node.submit_transaction(tx)
    node.mine_block(initial_wallet)

    print(f"Баланс Alice: {node.get_balance(alice)}")


if __name__ == "__main__":
    main()
