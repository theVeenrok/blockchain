from decimal import Decimal

from app.domain.entities import BlockChaine
from app.domain.entities import Wallet
from app.infrastructure.calculators import BlockchainBalanceCalculator
from app.infrastructure.validators import BlockchainTransactionValidator
from app.application.mempool import Mempool
from app.application.mining import MiningService
from app.application.nodes import BlockchainNode


def create_blockchain_node() -> BlockchainNode:
    """Собирает все компоненты вместе"""

    # 1. Доменная модель
    blockchain = BlockChaine()

    # 2. Инфраструктура
    balance_calculator = BlockchainBalanceCalculator(blockchain)
    validator = BlockchainTransactionValidator(balance_calculator)

    # 3. Приложение
    mempool = Mempool()
    mempool.set_validator(validator)

    mining_service = MiningService(
        mempool=mempool,
        blockchain=blockchain,
        miner_reward=Decimal("1.0"),
        difficulty=2
    )

    # 4. Нода
    node = BlockchainNode(
        mempool=mempool,
        mining_service=mining_service,
        blockchain=blockchain
    )

    return node