from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ShipFromAddress:
    name: str
    phone: str
    company_name: Optional[str]
    address_line1: str
    address_line2: Optional[str]
    address_line3: Optional[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    address_residential_indicator: str  

    def __post_init__(self):
        valid_residential_indicators = ("yes", "no", "unknown")
        if self.address_residential_indicator not in valid_residential_indicators:
            raise ValueError(f"address_residential_indicator must be on of {valid_residential_indicators}")


@dataclass
class ShipToAddress:
    name: str
    phone: str
    company_name: Optional[str]
    address_line1: str
    address_line2: Optional[str]
    address_line3: Optional[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    address_residential_indicator: str  

    def __post_init__(self):
        valid_residential_indicators = ("yes", "no", "unknown")
        if self.address_residential_indicator not in valid_residential_indicators:
            raise ValueError(f"address_residential_indicator must be on of {valid_residential_indicators}")


@dataclass
class ReturnAddress:
    name: str
    phone: str
    company_name: Optional[str]
    address_line1: str
    address_line2: Optional[str]
    address_line3: Optional[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    address_residential_indicator: str  

    def __post_init__(self):
        valid_residential_indicators = ("yes", "no", "unknown")
        if self.address_residential_indicator not in valid_residential_indicators:
            raise ValueError(f"address_residential_indicator must be on of {valid_residential_indicators}")


@dataclass
class PackageWeight:
    value: float
    unit: str  

    def __post_init__(self):
        valid_units = ("pound", "ounce", "gram", "kilogram")
        if self.unit not in valid_units:
            raise ValueError(f"weight unit must be one of {valid_units}.")


@dataclass
class PackageDimensions:
    unit: str
    length: float
    width: float
    height: float

    def __post_init__(self):
        valid_units = ("inch", "centimeter")
        if self.unit not in valid_units:
            raise ValueError(f"dimension unit must be one of {valid_units}.")


@dataclass
class PackageInsuredValue:
    currency: str
    amount: float


@dataclass
class PackageLabelMessages:
    reference1: Optional[str]


@dataclass
class Package:
    weight: PackageWeight
    dimensions: Optional[PackageDimensions]
    label_messages: PackageLabelMessages


@dataclass
class Shipment:
    carrier_id: str
    service_code: str
    external_shipment_id: Optional[str]
    ship_date: str
    ship_to: ShipToAddress
    ship_from: ShipFromAddress
    warehouse_id: Optional[str]
    return_to: Optional[ReturnAddress]
    confirmation: str
    insurance_provider: str
    packages: List[Package]

    def __post_init__(self):
        confirmation_options = ("none", "delivery", "signature", "adult_signature",
                                "direct_signature", "delivery_mailed")
        if self.confirmation not in confirmation_options:
            return ValueError(f"confirmation must be one of {confirmation_options}")


@dataclass
class PickupWindow:
    start_at: str
    end_at: str


@dataclass
class PickupContactDetails:
    name: str
    email: str
    phone: str


@dataclass
class PickupObj:
    label_ids: List[str]
    contact_details: PickupContactDetails
    pickup_notes: str
    pickup_window: PickupWindow
