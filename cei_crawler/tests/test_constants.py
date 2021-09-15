import pytest

from ..constants import (
    ASSET_ACTION_TYPE_MAPPER,
    ASSET_MARKET_TYPE_MAPPER,
    AssetExtractAction,
    AssetExtractMarketType,
    PassiveIncomeType,
    PASSIVE_INCOME_TYPE_MAPPER,
    PassiveIncomeEventType,
    PASSIVE_INCOME_EVENT_TYPE_MAPPER,
)


class TestConstantsMapper:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ("C", AssetExtractAction.BUY.value),
            ("V", AssetExtractAction.SELL.value),
        ],
    )
    async def test_asset_action_type_mapper(self, key, expected_value):
        assert ASSET_ACTION_TYPE_MAPPER[key] == expected_value

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ("Merc. Fracionário", AssetExtractMarketType.FRACTIONAL.value),
            ("Mercado a Vista", AssetExtractMarketType.UNIT.value),
        ],
    )
    async def test_asset_market_type_mapper(self, key, expected_value):
        assert ASSET_MARKET_TYPE_MAPPER[key] == expected_value

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ("Provisionado", PassiveIncomeEventType.FUTURE.value),
            ("Creditado", PassiveIncomeEventType.PAST.value),
        ],
    )
    async def test_passive_income_event_type_mapper(self, key, expected_value):
        assert PASSIVE_INCOME_EVENT_TYPE_MAPPER[key] == expected_value

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ("DIVIDENDO", PassiveIncomeType.DIVIDEND.value),
            ("JUROS SOBRE CAPITAL PRÓPRIO", PassiveIncomeType.JCP.value),
            ("RENDIMENTO", PassiveIncomeType.YIELD.value),
        ],
    )
    async def test_passive_income_type_mapper(self, key, expected_value):
        assert PASSIVE_INCOME_TYPE_MAPPER[key] == expected_value
