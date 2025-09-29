import dataclasses
from app.domain.entities import Transaction, Wallet, BlockChaine
from app.application.mempool import Mempool
from app.application.mining import MiningService
from app.domain.value_objects import Amount


@dataclasses.dataclass
class BlockchainNode:
    _mempool: Mempool
    _mining_service: MiningService
    _blockchain: BlockChaine

    def submit_transaction(self, tx: Transaction) -> bool:
        """Основной API для пользователей"""
        return self._mempool.add_transaction(tx)

    def mine_block(self, miner_wallet: Wallet) -> bool:
        """API для майнеров"""
        return self._mining_service.mine_block(miner_wallet)

    def get_balance(self, wallet: Wallet) -> Amount:
        """API для запроса баланса"""
        return self._blockchain.get_wallet_amount(wallet)

    def verify_chain(self) -> bool:
        """Проверка целостности цепи"""
        return self._blockchain.verify_chain()