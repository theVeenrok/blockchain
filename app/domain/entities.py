import dataclasses
import hashlib
import json
import time
import uuid
from dataclasses import asdict
from decimal import Decimal

from app.domain.value_objects import Amount


@dataclasses.dataclass()
class Wallet:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid4)


@dataclasses.dataclass()
class Transaction:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid4)
    sender: Wallet
    recipient: Wallet
    amount: Amount
    fee: Amount
    timestamp: float = dataclasses.field(init=False, default_factory=time.time)

    def __repr__(self):
        return f"<Tx {self.sender} -> {self.recipient}: {self.amount}>"


@dataclasses.dataclass()
class Block:
    index: int
    data: list[Transaction]
    previous_hash: str
    nonce: int = 0

    def __post_init__(self):
        self.hash = self.get_hash()

    def get_hash(self) -> str:
        block_data = {
            "index": self.index,
            "data": sorted([asdict(tx) for tx in self.data], key=lambda v: v.id),
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        data_string = json.dumps(block_data, sort_keys=True)
        data_hash = hashlib.sha256(data_string.encode()).hexdigest()
        return data_hash

    def mine(self, difficulty: int):
        target = "0" * difficulty

        while True:
            hash_attempt = self.get_hash()
            if hash_attempt.startswith(target):
                object.__setattr__(self, "hash", hash_attempt)
                break
            self.nonce += 1

    def __repr__(self) -> str:
        return f"<Block {self.index}, hash={self.hash}, txs={self.data}>"


@dataclasses.dataclass()
class BlockChaine:
    __chain: list[Block] = dataclasses.field(default_factory=list)
    __system_wallet: Wallet = dataclasses.field(default_factory=Wallet)
    __init_wallet: Wallet = dataclasses.field(default_factory=Wallet)

    def __post_init__(self):
        self.__init_amount: int = 10

        self.__create_genesis_block()

    def __create_genesis_block(self):
        genesis_tx = Transaction(
            sender=self.__system_wallet,
            recipient=self.__init_wallet,
            amount=Amount(Decimal(self.__init_amount)),
            fee=Amount(Decimal(0))
        )
        genesis_block = Block(
            index=0,
            data=[genesis_tx],
            previous_hash="0" * 64
        )
        genesis_block.mine(difficulty=2)
        self.__chain.append(genesis_block)

    def add_block(self, block: Block) -> bool:
        if not self.__validate_new_block(block):
            return False

        self.__chain.append(block)
        return True

    def __validate_new_block(self, block: Block) -> bool:
        if block.index != len(self.__chain):
            return False
        if block.previous_hash != self.__chain[-1].get_hash():
            return False
        return block.hash == block.get_hash()

    def verify_chain(self) -> bool:
        if not self.__chain:
            return True

        # Проверяем генезис-блок
        if self.__chain[0].index != 0 or self.__chain[0].previous_hash != "0" * 64:
            return False

        for i, block in enumerate(self.__chain):
            # Проверяем корректность хэша блока
            if block.hash != block.get_hash():
                return False

            # Проверяем previous_hash для всех кроме генезис-блока
            if i > 0 and block.previous_hash != self.__chain[i - 1].hash:
                return False

        return True

    def get_wallet_amount(self, wallet: Wallet) -> Amount:
        balance = Decimal(0)
        for block in self.__chain:
            for transaction in block.data:
                if transaction.recipient.id == wallet.id:
                    balance += transaction.amount.value
                if transaction.sender.id == wallet.id:
                    balance -= (transaction.amount.value + transaction.fee.value)
        return Amount(balance)

    def get_chain(self) -> list[Block]:
        return self.__chain.copy()

    def get_last_block_hash(self) -> str:
        return self.__chain[-1].get_hash()
