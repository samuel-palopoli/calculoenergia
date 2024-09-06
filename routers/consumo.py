from fastapi import APIRouter, Query
from models.dispositivo import DispositivoDB
from models.dependencia import DependenciaDB
from models.unidade_consumidora import UnidadeConsumidoraDB
from schemas.consumo import ConsumoRead
from services.consumo import calcular_consumo
from utils.enuns import EnumOrigemDoConsumo
from utils.erros import (
    dependencia_not_found_error,
    dispositivo_not_found_error,
    unidade_consumidora_not_found_error,
)

router = APIRouter(prefix='/consumos', tags=['Consumos'])

@router.get('/', response_model=ConsumoRead)
def calcular_consumo_endpoint(
    origem_do_consumo: EnumOrigemDoConsumo = Query(...),
    item_id: int = Query(...),
):
    dispositivos_eletricos = []

    if origem_do_consumo == EnumOrigemDoConsumo.dispositivo_eletrico:
        dispositivo = DispositivoDB.get_or_none(DispositivoDB.id == item_id)

        if not dispositivo:
            raise dispositivo_not_found_error()

        dispositivos_eletricos = [dispositivo]

    elif origem_do_consumo == EnumOrigemDoConsumo.dependencia:
        dependencia = DependenciaDB.get_or_none(DependenciaDB.id == item_id)
        if not dependencia:
            raise dependencia_not_found_error()

        dispositivos_eletricos = list(
            DispositivoDB.select().where(
                DispositivoDB.dependencia == dependencia
            )
        )

    elif origem_do_consumo == EnumOrigemDoConsumo.unidade_consumidora:
        unidade_consumidora = UnidadeConsumidoraDB.get_or_none(UnidadeConsumidoraDB.id == item_id)
        if not unidade_consumidora:
            raise unidade_consumidora_not_found_error()

        dispositivos_eletricos = list(
            DispositivoDB.select().where(
                DispositivoDB.unidade_consumidora == unidade_consumidora
            )
        )

    consumo_diario, consumo_mensal, consumo_anual = calcular_consumo(
        dispositivos_eletricos
    )

    return ConsumoRead(
        consumo_diario=consumo_diario,
        consumo_mensal=consumo_mensal,
        consumo_anual=consumo_anual,
    )
