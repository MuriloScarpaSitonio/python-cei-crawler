from datetime import date as date_typing
from functools import cached_property
from typing import Any, Dict, List, Optional, Union

from aiohttp import TCPConnector

from .crawlers import AssetsCrawler, PassiveIncomesCrawler
from .exceptions import CeiCrawlerBlankCredentialsException
from .models import Broker, AssetExtract, PassiveIncome

BLANK_VALUES = (None, "")


class CeiCrawler:
    def __init__(self, username: str, password: str) -> None:
        if username in BLANK_VALUES or password in BLANK_VALUES:
            raise CeiCrawlerBlankCredentialsException()

        self._connector = TCPConnector(limit=30, ssl=False)
        self.username = username
        self.password = password

    @cached_property
    def _assets_crawler(self) -> AssetsCrawler:
        return AssetsCrawler(
            connector=self._connector,
            username=self.username,
            password=self.password,
        )

    @cached_property
    def _passive_incomes_crawler(self) -> PassiveIncomesCrawler:
        return PassiveIncomesCrawler(
            connector=self._connector,
            username=self.username,
            password=self.password,
        )

    async def close(self) -> None:
        await self._assets_crawler.session_close()
        await self._passive_incomes_crawler.session_close()
        await self._connector.close()

    async def get_brokers(self) -> List[Broker]:
        return await self._assets_crawler.get_brokers_with_accounts()

    async def get_assets_extract(
        self,
        brokers: Optional[List[Broker]] = None,
        start_date: Optional[date_typing] = None,
        end_date: Optional[date_typing] = None,
        as_dict: bool = False,
    ) -> Union[List[AssetExtract], List[Dict[str, Any]]]:
        return await self._assets_crawler.get_brokers_account_portfolio_assets_extract(
            brokers=brokers if brokers is not None else await self.get_brokers(),
            start_date=start_date,
            end_date=end_date,
            as_dict=as_dict,
        )

    async def get_passive_incomes_extract(
        self, date: Optional[date_typing] = None, as_dict: bool = False
    ) -> Union[List[PassiveIncome], List[Dict[str, Any]]]:
        return await self._passive_incomes_crawler.get_passive_incomes_extract(
            date=date, as_dict=as_dict
        )
