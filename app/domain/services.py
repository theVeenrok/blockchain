from abc import ABC, abstractmethod

from app.domain.entities import Wallet, Transaction, Block
from app.domain.value_objects import Amount


class BalanceCalculator(ABC):
    @abstractmethod
    def get_wallet_amount(self, wallet: Wallet) -> Amount:
        pass

class TransactionValidator(ABC):
    @abstractmethod
    def validate_transaction(self, tx: Transaction) -> bool:
        pass

class BlockMiner(ABC):
    @abstractmethod
    def mine_block(self, transactions: list[Transaction], miner_wallet: Wallet) -> Block:
        pass