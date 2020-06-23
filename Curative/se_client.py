import dataclasses
import datetime
import os
import pprint as p
from typing import List

import requests
from requests.auth import AuthBase

from Curative import load_dotenv
from Curative.models import (
    Shipment,
    ShipFromAddress,
    ShipToAddress,
    Package,
    PackageWeight,
    PackageDimensions,
    AdvancedOptions
)

load_dotenv()

dt = datetime.datetime.now()


class ShipEngineAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, request):
        request.headers["API-Key"] = self.api_key
        return request


class ShipEngine:
    _BASE_URL = "https://api.shipengine.com/v1/"
    _CURRENT_DATE = dt.strftime("%m/%d/%Y")

    def __init__(self, api_key: str = os.getenv("SHIPENGINE_API_KEY"), carrier_id: str = os.getenv("UPS_CARRIER-ID")):
        self.api_key = api_key
        self.carrier_id = carrier_id
        self.session = requests.Session()

    def request(self, method: str, endpoint: str, *args, **kwargs):
        kwargs["auth"] = ShipEngineAuth(self.api_key)
        resp = self.session.request(
                method, self._BASE_URL + endpoint.strip("/"), *args, **kwargs
        )
        resp.raise_for_status()
        return resp.json()

    def get(self, endpoint, *args, **kwargs):
        return self.request("GET", endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        return self.request("POST", endpoint, *args, **kwargs)

    def create_label(
            self,
            ship_to_address: ShipToAddress,
            ship_from_address: ShipFromAddress,
            packages: List[Package],
            label_message: str
    ):
        advanced_options = AdvancedOptions(custom_field1=label_message)

        shipment = Shipment(
                carrier_id=self.carrier_id,
                service_code="ups_next_day_air",
                external_shipment_id=None,
                ship_date=self._CURRENT_DATE,
                ship_to=dataclasses.asdict(ship_to_address),
                ship_from=dataclasses.asdict(ship_from_address),
                warehouse_id=None,
                return_to=None,
                confirmation='delivery',
                advanced_options=dataclasses.asdict(advanced_options),
                insurance_provider='none',
                packages=[dataclasses.asdict(package) for package in packages]
        )

        request = {"shipment": dataclasses.asdict(shipment)}
        return self.post("labels", json=request)
