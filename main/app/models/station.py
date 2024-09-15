from pymongo import MongoClient, GEOSPHERE
from bson import ObjectId

class Station:
    def __init__(self, db):
        self.collection = db['charging_stations']
        self.collection.create_index([("location", GEOSPHERE)])

    def to_dict(self, station):
        return {
            "id": str(station["_id"]),
            "cost": station["cost"],
            "charging_points": station["charging_points"],
            "pay_at_location": station["pay_at_location"],
            "membership_required": station["membership_required"],
            "access_key_required": station["access_key_required"],
            "is_operational": station["is_operational"],
            "latitude": station["latitude"],
            "longitude": station["longitude"],
            "operator": station["operator"],
            "connection_type": station["connection_type"],
            "current_type": station["current_type"],
            "charging_points_flag": station["charging_points_flag"]
        }

    def find_all(self, page, size):
        offset = (page - 1) * size
        return list(self.collection.find().skip(offset).limit(size))

    def find_by_id(self, station_id):
        return self.collection.find_one({"_id": ObjectId(station_id)})

    def find_nearest(self, user_lat, user_lng):
        nearest_station = self.collection.find_one({
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [user_lng, user_lat]
                    }
                }
            }
        })
        return self.to_dict(nearest_station) if nearest_station else None
