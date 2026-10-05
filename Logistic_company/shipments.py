
"""
    SwiftLink Logistics courier Company
    Implemented by oabdulaz
    
"""

"""
data members: tracking_id, sender_name, recipient_name, destination_city, weight_kg, base_rate_per_kg
methods: get_tracking_id(), get_sender_name(), get_recipient_name(), get_destination_city(), get_weight_kg(), get_base_rate_per_kg()
return: String
"""
import json

class Shipment:

    company_name = "SwiftLink Logistics"
    shipment_count = 0

    def __init__(self, tracking_id, sender_name, recipient_name, destination_city, weight_kg, base_rate_per_kg):
        if not self.is_valid_tracking_id(tracking_id):
          raise ValueError("Invalid tracking ID. Format must be SL-1234")

        self.__tracking_id = tracking_id
        self._sender_name = sender_name
        self._recipient_name = recipient_name
        self._destination_city = destination_city
        self._weight_kg = weight_kg
        self._base_rate_per_kg = base_rate_per_kg
        Shipment.shipment_count += 1


    def get_tracking_id(self):
        return self.__tracking_id

    def get_sender_name(self):
          return self._sender_name

    def get_recipient_name(self):
          return self._recipient_name

    def get_destination_city(self):
          return self._destination_city

    def get_weight_kg(self):
          return self._weight_kg

    def set_weight_kg(self, new_weight):
      if new_weight <= 0 or new_weight > 1000:
        raise ValueError("Weight must be greater than 0 and not more than 1000")
      self._weight_kg = new_weight


    def get_base_rate_per_kg(self):
          return self._base_rate_per_kg

    def set_recipient_name(self, new_name):
          self._recipient_name = new_name

    def set_destination_city(self, city):
          self._destination_city = city

    def update_base_rate_per_kg(self, new_rate):
        if new_rate <= 0:
          raise ValueError("Base rate per kg must be greater than zero")
        self._base_rate_per_kg = new_rate

    def display_details(self):
          print(f"Tracking ID: {self.__tracking_id}")
          print(f"Sender Name: {self._sender_name}")
          print(f"Recipient Name: {self._recipient_name}")
          print(f"Destination City: {self._destination_city}")
          print(f"Weight (kg): {self._weight_kg}")

    def calculate_cost(self):
        return self._weight_kg * self._base_rate_per_kg

    @classmethod
    def get_shipment_count(cls):
     return cls.shipment_count

    @staticmethod
    def is_valid_tracking_id(tracking_id):
     import re
     return bool(re.fullmatch(r"SL-\d{4}", tracking_id))


    def to_dict(self):
      return {
        "type": "Shipment",
        "tracking_id": self.__tracking_id,
        "sender_name": self._sender_name,
        "recipient_name": self._recipient_name,
        "destination_city": self._destination_city,
        "weight_kg": self._weight_kg,
        "base_rate_per_kg": self._base_rate_per_kg
     }


    def __str__(self):
     return f"Tracking ID: {self.__tracking_id}\nSender Name: {self._sender_name}\nRecipient Name: {self._recipient_name}\nDestination City: {self._destination_city}\nWeight (kg): {self._weight_kg}\nBase Rate per kg: {self._base_rate_per_kg}\nCost: {self.calculate_cost()} RWF"

"""
data members: declare_value, insurance_rate
methods: get_declare_value(), get_insurance_rate()
return: float
"""
class TrackedShipment(Shipment):
  def __init__(self, tracking_id, sender_name, recipient_name, destination_city, weight_kg, base_rate_per_kg, declare_value, insurance_rate, current_status):
    self._declare_value = declare_value
    self._insurance_rate = insurance_rate
    self._current_status = current_status
    super().__init__(tracking_id, sender_name, recipient_name, destination_city, weight_kg, base_rate_per_kg)

  def get_declare_value(self):
     return self._declare_value

  def get_insurance_rate(self):
    return self._insurance_rate

  def set_declare_value(self, new_value):
    if new_value < 0:
      raise ValueError("Declare value cannot be negative")
    self._declare_value = new_value

  def set_insurance_rate(self, new_rate):
    if new_rate < 0 or new_rate > 0.05:
      raise ValueError("Insurance rate must be between 0% and 5%")
    self._insurance_rate = new_rate

  def get_current_status(self):
    return self._current_status

  def set_current_status(self, new_status):
    status = ["received", "in transit", "out for delivery", "delivered"]

    if new_status.lower() not in status:
        raise ValueError(
            "Invalid status. One of received, in transit, out for delivery, delivered"
        )

    self._current_status = new_status

  def calculate_cost(self):
      return super().calculate_cost() + self._declare_value * self._insurance_rate


  def to_dict(self):
       data = super().to_dict()
       data["type"] = "TrackedShipment"
       data["declared_value"] = self._declare_value
       data["insurance_rate"] = self._insurance_rate
       data["current_status"] = self._current_status
       return data

  def __str__(self):
    return f"{super().__str__()}\nDeclare Value: {self._declare_value}\nInsurance Rate: {self._insurance_rate}\nCurrent Status: {self._current_status}"



"""
data members: guaranteed_hours
methods: get_guaranteed_hours()
return: int
"""
class ExpressParcel(TrackedShipment):

  PRIORITY_FEES = {6: 20000, 12: 12000, 24: 6000, 48: 3000}

  def __init__(self, tracking_id, sender_name, recipient_name, destination_city, weight_kg, base_rate_per_kg, declare_value, insurance_rate, current_status, guaranteed_hours):
    self._guaranteed_hours = guaranteed_hours
    super().__init__(tracking_id, sender_name, recipient_name, destination_city, weight_kg, base_rate_per_kg, declare_value, insurance_rate, current_status)

  def set_guaranteed_hours(self, new_hours):
    if new_hours in {6, 12, 24, 48}:
      self._guaranteed_hours = new_hours
    else:
      raise ValueError("Invalid guaranteed hours. Exactly 6, 12, 24 or 48")

  def get_guaranteed_hours(self):
    return self._guaranteed_hours

  def calculate_cost(self):
    return super().calculate_cost() + self.PRIORITY_FEES[self._guaranteed_hours]

  def to_dict(self):
    data = super().to_dict()
    data["type"] = "ExpressParcel"
    data["guaranteed_hours"] = self._guaranteed_hours
    return data

  def __str__(self):
    return f"{super().__str__()}\nGuaranteed Hours: {self._guaranteed_hours}"


"""
data members: handling_class, packaging_fee
methods: get_handling_class(), get_packaging_fee(), set_handling_class(), set_packaging_fee()
return: float
"""
class FragileParcel(TrackedShipment):
  def __init__(self, tracking_id, sender_name, recipient_name, destination_city, weight_kg, base_rate_per_kg, declare_value, insurance_rate, current_status, handling_class, packaging_fee):
    self._handling_class = handling_class
    self._packaging_fee =  packaging_fee
    super().__init__(tracking_id, sender_name, recipient_name, destination_city, weight_kg, base_rate_per_kg, declare_value, insurance_rate, current_status)

  def get_handling_class(self):
    return self._handling_class

  def get_packaging_fee(self):
    return self._packaging_fee

  def set_handling_class(self, new_class):
    if new_class in ["glass", "electronics", "artwork"]:
      self._handling_class = new_class
    else:
      raise ValueError("Invalid handling class. One of glass, electronics or artwork")

  def set_packaging_fee(self, new_fee):
    if new_fee < 0:
      raise ValueError("Packaging fee must not be negative")
    self._packaging_fee = new_fee

  def calculate_cost(self):
    base_transport_charge =self._weight_kg * (self._base_rate_per_kg * 0.15)
    return super().calculate_cost() + self._packaging_fee + base_transport_charge

  def to_dict(self):
    data = super().to_dict()
    data["type"] = "FragileParcel"
    data["handling_class"] = self._handling_class
    data["packaging_fee"] = self._packaging_fee
    return data

  def __str__(self):
    return f"{super().__str__()}\nHandling Class: {self._handling_class}\nPackaging Fee: {self._packaging_fee}"


"""
data members: pallet_count, volume_m3
methods: get_pallet_count(), get_volume_m3(), set_pallet_count(), set_volume_m3()
return: float
"""
class BulkFreight(Shipment):

  VOLUMETRIC_RATE_PER_M3 = 25000
  PALLET_HANDLING_FEE = 2000

  def __init__(self, tracking_id, sender_name, recipient_name, destination_city, weight_kg, base_rate_per_kg, declare_value, insurance_rate, current_status, pallet_count, volume_m3):
    self._pallet_count = pallet_count
    self._volume_m3 = volume_m3
    super().__init__(tracking_id, sender_name, recipient_name, destination_city, weight_kg, base_rate_per_kg)

  def get_pallet_count(self):
    return self._pallet_count

  def get_volume_m3(self):
    return self._volume_m3

  def set_pallet_count(self, new_count):
    if new_count < 1 or new_count > 20:
      raise ValueError("Pallet count must be between 1 and 20 inclusive")
    self._pallet_count = new_count

  def set_volume_m3(self, new_volume):
    if new_volume <= 0:
      raise ValueError("Volume must be greater than zero")
    self._volume_m3 = new_volume

  def calculate_cost(self):
      weight_cost = super().calculate_cost()
      volume_cost = self._volume_m3 * self.VOLUMETRIC_RATE_PER_M3
      pallet_cost = self._pallet_count * self.PALLET_HANDLING_FEE
      return max(weight_cost, volume_cost) + pallet_cost

  def to_dict(self):
    data = super().to_dict()
    data["type"] = "BulkFreight"
    data["pallet_count"] = self._pallet_count
    data["volume_m3"] = self._volume_m3
    return data

  def __str__(self):
    return f"{super().__str__()}\nPallet Count: {self._pallet_count}\nVolume (m3): {self._volume_m3} m\u00b3"

  



    
    