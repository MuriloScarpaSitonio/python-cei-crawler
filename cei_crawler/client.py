from datetime import date as date_typing, datetime
from typing import Dict, Optional, Union
from urllib.parse import urljoin, urlparse

from aiohttp import ClientSession
from aiohttp.client_reqrep import ClientResponse
from bs4 import BeautifulSoup

from .exceptions import CeiCrawlerUnableToLoginException
from .models import Broker, BrokerAccount


class CeiClient:
    __is_logged__ = False
    LOGIN_URL = "https://ceiapp.b3.com.br/CEI_Responsivo/login.aspx"
    _HEADERS_ORIGIN_URL = "https://cei.b3.com.br"
    WRONG_CREDENTIALS_TEXTS = (
        "Usuário/Senha/Código de verificação inválido(a)",
        "Sua sessão expirou. Favor efetuar um novo acesso.",
        "não há dados disponíveis para serem consultados.",
    )
    CEI_SERVER_ERROR_TEXT = "Desculpe-nos pelo transtorno. Ocorreu um erro inesperado."

    def __init__(
        self,
        username: str,
        password: str,
        session: ClientSession,
        base_url: str,
    ) -> None:
        self.username = username
        self.password = password
        self.session = session
        self.base_url = base_url

    async def _get_referer(self) -> str:
        return urljoin(self._HEADERS_ORIGIN_URL, urlparse(self.base_url).path)

    async def _get_headers(self) -> Dict[str, str]:
        return {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": await self._get_referer(),
            "Origin": self._HEADERS_ORIGIN_URL,
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 "
                "Safari/537.36"
            ),
        }

    async def login(self) -> bool:
        async with self.session.get(self.LOGIN_URL) as response:
            html = BeautifulSoup(await response.text(), "html.parser")
            try:
                view_state = html.find(id="__VIEWSTATE")["value"]
                viewstate_generator = html.find(id="__VIEWSTATEGENERATOR")["value"]
                event_validation = html.find(id="__EVENTVALIDATION")["value"]
            except TypeError as error:
                raise CeiCrawlerUnableToLoginException(repr(error)) from error

        payload = {
            "ctl00$ContentPlaceHolder1$smLoad": (
                "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHold"
                "er1$btnLogar"
            ),
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATEGENERATOR": viewstate_generator,
            "__EVENTVALIDATION": event_validation,
            "__VIEWSTATE": view_state,
            "ctl00$ContentPlaceHolder1$txtLogin": self.username,
            "ctl00$ContentPlaceHolder1$txtSenha": self.password,
            "__ASYNCPOST": True,
            "ctl00$ContentPlaceHolder1$btnLogar": "Entrar",
        }

        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://cei.b3.com.br/CEI_Responsivo/login.aspx",
            "Origin": self._HEADERS_ORIGIN_URL,
            "Host": "cei.b3.com.br",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 "
                "Safari/537.36"
            ),
        }

        async with self.session.post(
            self.LOGIN_URL,
            data=payload,
            headers=headers,
        ) as response:

            html = await response.text()
            if any(text in html for text in self.WRONG_CREDENTIALS_TEXTS):
                raise CeiCrawlerUnableToLoginException("Usuário/Senha inválido(a)")

            if self.CEI_SERVER_ERROR_TEXT in html:
                raise CeiCrawlerUnableToLoginException(
                    "Parece que o site do CEI está fora do ar. "
                    f"Resposta do servidor: {self.CEI_SERVER_ERROR_TEXT}"
                )

            self.__is_logged__ = True
            return self.__is_logged__

    async def get_brokers(self) -> ClientResponse:
        if not self.__is_logged__:
            await self.login()
        return await self.session.get(self.base_url)

    async def get_broker_accounts(
        self, payload: Dict[str, Union[str, bool]]
    ) -> ClientResponse:
        if not self.__is_logged__:
            await self.login()
        return await self.session.post(
            self.base_url, data=payload, headers=await self._get_headers()
        )

    async def get_broker_account_portfolio_assets_extract(
        self,
        broker: Broker,
        account: BrokerAccount,
        start_date: Optional[date_typing] = None,
        end_date: Optional[date_typing] = None,
    ) -> ClientResponse:
        if not self.__is_logged__:
            await self.login()

        start_date_str = (
            start_date.strftime("%d/%m/%Y")
            if start_date is not None
            else broker.parse_extra_data.start_date
        )
        end_date_str = (
            end_date.strftime("%d/%m/%Y")
            if end_date is not None
            else broker.parse_extra_data.end_date
        )

        payload = {
            "ctl00$ContentPlaceHolder1$ToolkitScriptManager1": (
                "ctl00$ContentPlaceHolder1$updFiltro|ctl00$ContentPlaceHolder1"
                "$btnConsultar"
            ),
            "__EVENTTARGET": "",
            "__VIEWSTATE": account.parse_extra_data.view_state,
            "__VIEWSTATEGENERATOR": account.parse_extra_data.view_state_generator,
            "__EVENTVALIDATION": account.parse_extra_data.event_validation,
            "ctl00$ContentPlaceHolder1$ddlAgentes": broker.value,
            "ctl00$ContentPlaceHolder1$ddlContas": account.id,
            "ctl00$ContentPlaceHolder1$txtDataDeBolsa": start_date_str,
            "ctl00$ContentPlaceHolder1$txtDataAteBolsa": end_date_str,
            "ctl00$ContentPlaceHolder1$btnConsultar": "Consultar",
            "__ASYNCPOST": True,
        }

        return await self.session.post(
            self.base_url, data=payload, headers=await self._get_headers()
        )

    @staticmethod
    async def _get_date_str(broker: Broker, date: Optional[date_typing]) -> str:
        if (
            date
            and datetime.strptime(broker.parse_extra_data.start_date, "%d/%m/%Y").date()
            <= date
            <= datetime.strptime(broker.parse_extra_data.end_date, "%d/%m/%Y").date()
        ):
            # By some reason, CEI will return some "nonsense" data if
            # we pass a date out of range
            return date.strftime("%d/%m/%Y")
        return broker.parse_extra_data.end_date

    async def get_passive_incomes_extract(
        self, broker: Broker, date: Optional[date_typing] = None
    ) -> ClientResponse:
        if not self.__is_logged__:
            await self.login()

        account = broker.accounts[0]  # accounts[0] it's relative to all accounts
        payload = {
            "ctl00$ContentPlaceHolder1$ToolkitScriptManager1": (
                "ctl00$ContentPlaceHolder1$updFiltro|ctl00$ContentPlaceHolder1"
                "$btnConsultar"
            ),
            "__EVENTTARGET": "",
            "__VIEWSTATE": account.parse_extra_data.view_state,
            "__VIEWSTATEGENERATOR": account.parse_extra_data.view_state_generator,
            "__EVENTVALIDATION": account.parse_extra_data.event_validation,
            "ctl00$ContentPlaceHolder1$ddlAgentes": broker.value,
            "ctl00$ContentPlaceHolder1$ddlContas": account.id,
            "ctl00$ContentPlaceHolder1$txtData": await self._get_date_str(
                broker=broker, date=date
            ),
            "ctl00$ContentPlaceHolder1$btnConsultar": "Consultar",
            "__ASYNCPOST": True,
        }

        return await self.session.post(
            self.base_url, data=payload, headers=await self._get_headers()
        )
