from app.domain.entities import Transaction
from app.domain.services import BalanceCalculator, TransactionValidator


class BlockchainTransactionValidator(TransactionValidator):
    def __init__(self, balance_calculator: BalanceCalculator):
        self._balance_calculator = balance_calculator

    def validate_transaction(self, tx: Transaction) -> bool:
        sender_balance = self._balance_calculator.get_wallet_amount(tx.sender)
        required = tx.amount.value + tx.fee.value
        return sender_balance.value >= required