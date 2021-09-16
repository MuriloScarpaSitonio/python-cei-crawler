# cei-crawler
Biblioteca em python para obtenção de seus dados de investimentos na bolsa de valores (B3/CEI).

Esse projeto é altamente influenciado por [bolsa](https://github.com/gicornachini/bolsa). De fato, eu apenas simplifiquei, adicionei e estendi algumas funcionalidades.

# Requisitos
 - Python 3.8.x

## Instalação
```
$ pip install cei-crawler
```

## Utilização
```python
import asyncio

from cei_crawler import CeiCrawler


async def main():
    crawler = CeiCrawler(username="CPF/CNPJ", password="Sua senha")
    
    assets_extract = await crawler.get_assets_extract()
    print(assets_extract) # seus ativos negociados no CEI

    passive_income_extract = await crawler.get_passive_incomes_extract()
    print(passive_income_extract) # seus proventos registrados no CEI

    await crawler.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

## Funções disponíveis

Através da classe de client `CeiCrawler`, você terá acesso as seguintes funções:

### `get_brokers`
Obtém os brokers disponíveis para aquela conta. Retorna uma lista de `Broker` (Ex: XP Inc, Clear, Easynvest...) com uma lista de `BrokerAccount`.

### `get_assets_extract`
Obtém uma lista de ativos filtrados pelo parâmetros passados à função. Retorna uma lista de `AssetExtract`.

#### Parâmetros
| Atributo | Tipo | Descrição |
| :-------------: |:-------------:| -----|
| `brokers` | `Optional[List[Broker]]` | Retorna apenas os ativos destes brokers |
| `start_date` | `Optional[date]` | Retorna apenas os ativos com data posterior ou igual a esta |
| `end_date` | `Optional[date]` | Retorna apenas os ativos com data inferior ou igual a esta |
| `as_dict` | `bool` | Retorna os ativos como dicionários ao invés de objetos `AssetExtract`. Default: `False` |

### `get_passive_incomes_extract`
Obtém uma lista de rendimentos passivos filtrados pelo parâmetros passados à função. Retorna uma lista de `PassiveIncome`.

#### Parâmetros
| Atributo | Tipo | Descrição |
| :-------------: |:-------------:| -----|
| `date` | `Optional[date]` | Retorna apenas os ativos com data posterior ou igual a esta. Por favor, note que o CEI só aceita datas iguais ou 5 dias anteriores ao dia de hoje. Se uma data fora desse intervalo for passado, a consulta será feita com a data de hoje. |
| `as_dict` | `bool` | Retorna os ativos como dicionários ao invés de objetos `PassiveIncome`. Default: `False` |

## Models

#### Broker
Model responsável pelos dados do broker.

| Atributo        | Tipo           | Descrição  |
| :-------------: |:-------------:| -----|
| `value`      | `str` | Identificador da corretora na B3. |
| `name`      | `str`      |   Nome do broker na B3. |
| `accounts` | `List[BrokerAccount]`      |    Lista de contas no broker. |


#### BrokerAccount
Model responsável pelos dados da conta no broker.

| Atributo        | Tipo           | Descrição  |
| :-------------: |:-------------:| -----|
| `id`      | `str` | Número da conta no broker. |


#### AssetExtract
Model responsável pelos dados do ativo.

| Atributo        | Tipo           | Descrição  |
| :-------------: |:-------------:| -----|
| `operation_date`      | `datetime` | Data de operação do ativo. |
| `action`      | `AssetExtractAction`      |   Identificador do tipo de operação compra/venda. |
| `market_type` | `AssetExtractMarketType`      |   Tipo de mercado. |
| `raw_negotiation_code` | `str`      |    Código de negociação. |
| `asset_specification` | `str`      |    Especificação do ativo no CEI. |
| `unit_amount` | `int`      |    Quantidade de ativo. |
| `unit_price` | `Decimal`      |    Valor unitário do ativo. |
| `total_price` | `Decimal`      |    Valor total do ativo. |
| `quotation_factor` | `int`      |    Fator de cotação. |

#### PassiveIncome
Model responsável pelos dados de rendimento passivo.

| Atributo        | Tipo           | Descrição  |
| :-------------: |:-------------:| -----|
| `operation_date`      | `datetime` | Data do evento. |
| `income_type`      | `PassiveIncomeType`      |   Tipo de provento (Dividendo, JCP...). |
| `event_type`      | `PassiveIncomeEventType`      |   Tipo de evento do provento (provisionado, creditado...). |
| `raw_negotiation_name` | `str`      |    Nome do ativo. |
| `raw_negotiation_code` | `str`      |    Código de negociação. |
| `asset_specification` | `str`      |    Especificação do ativo no CEI. |
| `unit_amount` | `int`      |    Quantidade de ativo. |
| `gross_value` | `Decimal`      |    Valor bruto do provento. |
| `net_value` | `Decimal`      |    Valor líquido do provendo. |
| `quotation_factor` | `int`      |    Fator de cotação. |