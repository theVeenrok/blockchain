import dataclasses
import uuid

from app.domain.entities import Transaction
from app.domain.services import TransactionValidator


@dataclasses.dataclass
class Mempool:
    _pending_transactions: dict[uuid.UUID, Transaction] = dataclasses.field(default_factory=dict)
    _validator: TransactionValidator = None
    _max_size = 10000

    def set_validator(self, validator: TransactionValidator):
        self._validator = validator

    def add_transaction(self, tx: Transaction) -> bool:
        if not self._validator:
            raise ValueError("Validator not set")

        if self.contains(tx.id):
            return False

        if not self._validator.validate_transaction(tx):
            return False

        if self.get_size() >= self._max_size:
            self._evict_low_fee_transactions()

        self._pending_transactions[tx.id] = tx
        return True

    def get_transactions(self, limit: int = 1000) -> list[Transaction]:
        sorted_txs = sorted(
            self._pending_transactions.values(),
            key=lambda tx: tx.fee.value,
            reverse=True
        )
        return sorted_txs[:limit]

    def remove_transactions(self, tx_ids: list[uuid.UUID]) -> None:
        for tx_id in tx_ids:
            self._pending_transactions.pop(tx_id, None)

    def _evict_low_fee_transactions(self) -> None:
        if not self._pending_transactions:
            return

        min_fee_tx = min(
            self._pending_transactions.values(),
            key=lambda tx: tx.fee.value
        )
        del self._pending_transactions[min_fee_tx.id]
        print(f"Удалена транзакция с низкой комиссией: {min_fee_tx.id}")

    def get_size(self) -> int:
        return len(self._pending_transactions)

    def contains(self, tx_id: uuid.UUID) -> bool:
        return tx_id in self._pending_transactions

    def clear(self):
        self._pending_transactions.clear()