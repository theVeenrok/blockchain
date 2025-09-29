from app.domain.entities import Wallet
from app.domain.entities import BlockChaine
from app.domain.services import BalanceCalculator
from app.domain.value_objects import Amount


class BlockchainBalanceCalculator(BalanceCalculator):
    def __init__(self, blockchain: BlockChaine):
        self._blockchain = blockchain

    def get_wallet_amount(self, wallet: Wallet) -> Amount:
        return self._blockchain.get_wallet_amount(wallet)
