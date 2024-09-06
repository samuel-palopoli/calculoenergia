from models.dispositivo import DispositivoDB


class DispositivoDB:
    def __init__(self, consumo: float, uso_diario: float):
        self.consumo = consumo
        self.uso_diario = uso_diario


def calcular_consumo(eletrodomesticos: list[DispositivoDB]):
    consumo_diario_total = sum(
        dispositivo.consumo * dispositivo.uso_diario
        for dispositivo in eletrodomesticos
    )

    # Considere que um mês tem aproximadamente 30 dias e um ano tem 365 dias
    consumo_mensal_total = consumo_diario_total * 30
    consumo_anual_total = consumo_diario_total * 365

    return consumo_diario_total, consumo_mensal_total, consumo_anual_total


# Exemplo de uso
eletrodomesticos = [
    DispositivoDB(consumo=1.5, uso_diario=3),
    DispositivoDB(consumo=0.5, uso_diario=4)
]

consumo_diario, consumo_mensal, consumo_anual = calcular_consumo(eletrodomesticos)
print(f"Consumo diário: {consumo_diario:.2f} kWh")
print(f"Consumo mensal: {consumo_mensal:.2f} kWh")
print(f"Consumo anual: {consumo_anual:.2f} kWh")