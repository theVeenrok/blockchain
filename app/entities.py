import dataclasses
import hashlib
import json
import time
import uuid
from dataclasses import asdict
from decimal import Decimal

from app.value_objects import Amount


@dataclasses.dataclass()
class Wallet:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid4)


@dataclasses.dataclass()
class Transaction:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid4)
    sender: Wallet
    recipient: Wallet
    amount: Amount
    timestamp: float = dataclasses.field(init=False, default_factory=time.time)

    def __repr__(self):
        return f"<Tx {self.sender} -> {self.recipient}: {self.amount}>"


@dataclasses.dataclass()
class Block:
    index: int
    data: Transaction
    previous_hash: str

    def __post_init__(self):
        self.hash = self.get_hash()

    def get_hash(self) -> str:
        data = json.dumps(asdict(self.data), sort_keys=True)
        data_hash = hashlib.sha256(data.encode()).hexdigest()
        return data_hash

    def __repr__(self) -> str:
        return f"<Block {self.index}, hash={self.get_hash()}, txs={self.data}>"


@dataclasses.dataclass()
class BlockChaine:
    __chain: list[Block]

    def __post_init__(self):
        self.__init_wallet = Wallet()
        self.__init_amount = 10
        self.__create_genesis_block()

    def __create_genesis_block(self):
        genesis_tx = Transaction(
            sender=Wallet(),
            recipient=self.__init_wallet,
            amount=Amount(Decimal(self.__init_amount))
        )
        genesis_block = Block(
            index=0,
            data=genesis_tx,
            previous_hash="0"
        )
        self.__chain.append(genesis_block)

    def add_block(self, transaction: Transaction) -> None:
        new_block_index = len(self.__chain)
        previous_block_hash = self.__chain[-1].get_hash()
        new_block = Block(
            index=new_block_index,
            data=transaction,
            previous_hash=previous_block_hash
        )
        self.__chain.append(new_block)

    def verify_chain(self) -> bool:
        if not self.__chain:
            return True

        for i, block in enumerate(self.__chain):
            # Проверяем корректность хэша блока
            if block.hash != block.get_hash():
                return False

            # Проверяем previous_hash для всех кроме генезис-блока
            if i > 0 and block.previous_hash != self.__chain[i - 1].hash:
                return False

        return True

    def get_wallet_amount(self, wallet: Wallet) -> Amount:
        ...


vlad = Wallet()
alex = Wallet()


bc = BlockChaine()
for i in range(100000):
    t = Transaction(
        sender=vlad,
        recipient=alex,
        amount=Amount(Decimal(1))
    )
    bc.add_block(t)

start = time.time()
bc.verify()
end = time.time()
print(f"Верификация цепочки прошла за {end-start}")


bc.get_wallet_amount(alex)
