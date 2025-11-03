from enum import Enum


class CryptoAsset(str, Enum):
    BITCOIN = "bitcoin"
    ETHEREUM = "ethereum"
    SOLANA = "solana"
    BINANCECOIN = "binancecoin"
