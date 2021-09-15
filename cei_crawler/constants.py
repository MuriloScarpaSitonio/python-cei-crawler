from enum import Enum, unique


@unique
class AssetExtractAction(Enum):
    BUY = "buy"
    SELL = "sell"


@unique
class AssetExtractMarketType(Enum):
    FRACTIONAL = "fractional_share"
    UNIT = "unit"
    OPTIONS = "options"


ASSET_ACTION_TYPE_MAPPER = {
    "C": AssetExtractAction.BUY.value,
    "V": AssetExtractAction.SELL.value,
}

ASSET_MARKET_TYPE_MAPPER = {
    "Merc. Fracionário": AssetExtractMarketType.FRACTIONAL.value,
    "Mercado a Vista": AssetExtractMarketType.UNIT.value,
    "Opção de Compra": AssetExtractMarketType.OPTIONS.value,
    "Opção de Venda": AssetExtractMarketType.OPTIONS.value,
    "Exercicio de Opções": AssetExtractMarketType.OPTIONS.value,
}


@unique
class PassiveIncomeType(Enum):
    DIVIDEND = "dividend"
    JCP = "jcp"
    YIELD = "FII yield"


PASSIVE_INCOME_TYPE_MAPPER = {
    "DIVIDENDO": PassiveIncomeType.DIVIDEND.value,
    "JUROS SOBRE CAPITAL PRÓPRIO": PassiveIncomeType.JCP.value,
    "RENDIMENTO": PassiveIncomeType.YIELD.value,
}


@unique
class PassiveIncomeEventType(Enum):
    FUTURE = "provisioned"
    PAST = "credited"


PASSIVE_INCOME_EVENT_TYPE_MAPPER = {
    "Provisionado": PassiveIncomeEventType.FUTURE.value,
    "Creditado": PassiveIncomeEventType.PAST.value,
}
