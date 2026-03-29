"""Endpoint for map rotation"""

from typing import Dict, Any
from ..models import MapRotation, MapInfo


class MapRotationEndpoint:
    """Handler for /maprotation endpoint"""

    def __init__(self, client):
        self.client = client

    def _parse_response(self, data: Dict[str, Any]) -> Dict[str, MapRotation]:
        """Parse JSON response to MapRotation objects"""
        rotations = {}

        if "battle_royale" in data:
            br_data = data["battle_royale"]
            rotations["battle_royale"] = MapRotation(
                current=self._parse_map(br_data.get("current", {})),
                next=self._parse_map(br_data.get("next", {})),
                mode="battle_royale"
            )

        if "arenas" in data:
            arenas_data = data["arenas"]
            rotations["arenas"] = MapRotation(
                current=self._parse_map(arenas_data.get("current", {})),
                next=self._parse_map(arenas_data.get("next", {})),
                mode="arenas"
            )

        if "control" in data:
            control_data = data["control"]
            rotations["control"] = MapRotation(
                current=self._parse_map(control_data.get("current", {})),
                next=self._parse_map(control_data.get("next", {})),
                mode="control"
            )

        return rotations

    def _parse_map(self, map_data: Dict[str, Any]) -> MapInfo:
        """Parse single map data"""
        return MapInfo(
            name=map_data.get("map", "Unknown"),
            image_url=map_data.get("asset", ""),
            remaining_seconds=map_data.get("remainingSecs", 0),
            remaining_timer=map_data.get("remainingTimer", "0:00"),
            is_ranked=map_data.get("ranked", False)
        )