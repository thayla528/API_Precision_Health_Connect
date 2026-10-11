from math import asin, cos, radians, sin, sqrt

from database.institutions.institution_model import InstitutionModel
from database.professionals.professional_entity_model import ProfessionalEntityModel


class InstitutionService:
    EARTH_RADIUS_KM = 6371.0

    def __init__(self):
        self.institution_model = InstitutionModel()
        self.professional_model = ProfessionalEntityModel()

    @staticmethod
    def _valid_coordinates(latitude, longitude):
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            return None
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            return None
        return latitude, longitude

    @staticmethod
    def _distance_km(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        value = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        return 2 * InstitutionService.EARTH_RADIUS_KM * asin(sqrt(min(1, value)))

    def get_active_institutions(self):
        return {
            "success": True,
            "institutions": [dict(row) for row in self.institution_model.get_active()]
        }

    def nearby(self, latitude, longitude, radius_km=25):
        coordinates = self._valid_coordinates(latitude, longitude)
        if not coordinates:
            return {"success": False, "message": "Valid latitude and longitude are required."}
        try:
            radius_km = float(radius_km)
        except (TypeError, ValueError):
            return {"success": False, "message": "radius_km must be a number."}
        if not 0 < radius_km <= 500:
            return {"success": False, "message": "radius_km must be between 0 and 500."}

        lat, lon = coordinates
        results = []
        for row in self.institution_model.get_with_coordinates():
            item = dict(row)
            distance = self._distance_km(lat, lon, item["latitude"], item["longitude"])
            if distance <= radius_km:
                item["distance_km"] = round(distance, 2)
                results.append(item)
        results.sort(key=lambda item: item["distance_km"])
        return {"success": True, "radius_km": radius_km, "institutions": results}

    def create_institution(self, data):
        name = (data.get("name") or "").strip()
        if not name:
            return {"success": False, "message": "Institution name is required."}

        latitude = data.get("latitude")
        longitude = data.get("longitude")
        if (latitude is None) != (longitude is None):
            return {"success": False, "message": "Provide both latitude and longitude, or neither."}
        if latitude is not None:
            coordinates = self._valid_coordinates(latitude, longitude)
            if not coordinates:
                return {"success": False, "message": "Invalid latitude or longitude."}
            latitude, longitude = coordinates

        institution_id = self.institution_model.create(
            name=name,
            institution_type=data.get("institution_type"),
            phone=data.get("phone"),
            email=data.get("email"),
            postal_code=data.get("postal_code"),
            address=data.get("address"),
            house_number=data.get("house_number"),
            address_line2=data.get("address_line2"),
            neighborhood=data.get("neighborhood"),
            city=data.get("city"),
            state=data.get("state"),
            latitude=latitude,
            longitude=longitude,
        )
        return {"success": True, "message": "Institution created successfully.", "institution_id": institution_id}

    def link_professional(self, professional_id, institution_id, is_primary=False):
        professional = self.professional_model.get_by_id(professional_id)
        institution = self.institution_model.get_by_id(institution_id)
        if not professional:
            return {"success": False, "message": "Professional not found."}
        if not institution or not institution["active"]:
            return {"success": False, "message": "Active institution not found."}
        self.institution_model.link_professional(professional_id, institution_id, is_primary)
        return {"success": True, "message": "Professional linked to institution successfully."}
