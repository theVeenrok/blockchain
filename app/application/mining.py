import dataclasses
from decimal import Decimal
from app.domain.entities import Block, Transaction, Wallet, BlockChaine
from app.domain.value_objects import Amount
from app.application.mempool import Mempool


@dataclasses.dataclass
class MiningService:
    _mempool: Mempool
    _blockchain: BlockChaine
    _miner_reward: Decimal = Decimal("1.0")
    _difficulty: int = 2

    def mine_block(self, miner_wallet: Wallet, count_transactions: int = 10) -> bool:
        # 1. Берем транзакции из mempool
        transactions = self._mempool.get_transactions(limit=count_transactions)
        if not transactions:
            return False

        # 2. Создаем награду майнеру
        reward_tx = Transaction(
            sender=Wallet(),  # системный кошелек
            recipient=miner_wallet,
            amount=Amount(self._miner_reward),
            fee=Amount(Decimal("0"))
        )

        # 3. Создаем и майним блок
        previous_hash = self._blockchain.get_last_block_hash()
        new_block = Block(
            index=len(self._blockchain.get_chain()),
            data=transactions + [reward_tx],
            previous_hash=previous_hash
        )

        new_block.mine(self._difficulty)

        # 4. Добавляем блок в цепь
        success = self._blockchain.add_block(new_block)
        if success:
            # 5. Удаляем из mempool
            tx_ids = [tx.id for tx in transactions]
            self._mempool.remove_transactions(tx_ids)

        return success