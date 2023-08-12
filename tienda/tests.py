from django.test import TestCase
from tienda.models import Orden
from datetime import datetime
from django.utils import timezone
import zoneinfo

class TiendaViewsTests(TestCase):

    def test_v_index(self):
        '''
            Debe entregar todos los registros
            si no existen filtros

        '''
        respuesta = self.client.get("/")
        ords = respuesta.context["ordenes"]
        self.assertEqual(0, len(ords))

        newo = Orden()
        newo.cliente = "Jaimie Olivier"
        newo.direccion = "Alamaeda 240"
        newo.fecha = "2023-12-12"
        newo.fecha_envio = "2023-12-12"
        newo.save()

        respuesta = self.client.get("/")
        ords = respuesta.context["ordenes"]
        self.assertEqual(1, len(ords))

    def test_v_filtros(self):
        '''
            Entrega los registros con filtros de fecha

        '''

        newo = Orden()
        newo.cliente = "Simon Bolivar"
        newo.direccion = "Alameda 240"
        newo.fecha = "2022-12-12"
        newo.fecha_envio = datetime(2022,12,12).\
            astimezone(zoneinfo.ZoneInfo('America/Santiago'))
        newo.save()

        newo = Orden()
        newo.cliente = "Maikol Yakson"
        newo.direccion = "Alameda 240"
        newo.fecha = "2023-12-12"
        newo.fecha_envio = datetime(2023,12,12).\
            astimezone(zoneinfo.ZoneInfo('America/Santiago'))
        newo.save()

        res = self.client.get("/?fecha_inicio=%s&fecha_fin=%s" % (
            '2023-11-01',
            '2023-12-25',
        ))

        ords = res.context["ordenes"]
        self.assertEqual(1, len(ords))