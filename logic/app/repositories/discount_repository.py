import json
import os.path
from typing import List
from uuid import UUID, uuid4

from logic.app.configs import config
from logic.app.models.discount import Discount
from logic.app.models.qr import Qr
from logic.app.services import qr_service

_DIRECOTRIO_JSON: str = f'{config.DIRECTORIO_DB}/discount.json'
_DB: List[Discount] = []


def _discounts_hard() -> List[Discount]:

    id_1 = uuid4()
    id_2 = uuid4()
    id_3 = uuid4()
    id_4 = uuid4()

    return [
        Discount(
            description='Descuento de $100 en el total de tu próxima compra',
            qr=qr_service.crear_qr(id=id_1),
            discount_price=100.0,
            id=id_1
        ),
        Discount(
            description='Descuento de $300 en el total de tu próxima compra',
            qr=qr_service.crear_qr(id=id_2),
            discount_price=300.0,
            id=id_2
        ),
        Discount(
            description='Descuento del 10% del total de tu próxima compra',
            qr=qr_service.crear_qr(id=id_3),
            discount_percent=10,
            id=id_3
        ),
        Discount(
            description='Descuento de 20% en el total de tu próxima compra',
            qr=qr_service.crear_qr(id=id_4),
            discount_percent=20,
            id=id_4
        )
    ]


def _cargar_db():
    global _DB

    if not os.path.exists(_DIRECOTRIO_JSON):
        with open(_DIRECOTRIO_JSON, 'w+') as db:
            db.write(json.dumps([c.to_json() for c in _discounts_hard()]))

    with open(_DIRECOTRIO_JSON, 'rb+') as db:
        _DB = [Discount.from_json(d) for d in json.load(db)]


def _actualizar_db():
    with open(_DIRECOTRIO_JSON, 'w+') as db:
        json.dump([o.to_json() for o in _DB], db)


def guardar_discount(discount: Discount) -> UUID:
    if discount in _DB:
        _DB.remove(discount)

    _DB.append(discount)
    _actualizar_db()

    return discount.id


def buscar_discount(id: UUID) -> Discount:
    for discount in _DB:
        if discount.id == id:
            return discount

    return None


def todos_los_discount() -> List[Discount]:
    return _DB


def borrar_discount(id: UUID) -> Discount:
    discount = buscar_discount(id)
    if discount is None:
        return

    _DB.remove(discount)
    _actualizar_db()

    return discount


_cargar_db()
