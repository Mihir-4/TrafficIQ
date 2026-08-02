"""
TrafficIQ - Smart Traffic Analytics & Optimization Engine
Computes real-time traffic statistics, Passenger Car Units (PCU), weighted road load,
dynamic signal timing optimization (Current vs Recommended), CO2/NOx/PM emission rates,
and Corridor Route Optimization & Traffic Diversion recommendations.
"""

from typing import Dict, Any, List
from configs.config import PCU_WEIGHTS, DENSITY_LEVELS, SIGNAL_TIMING, EMISSION_FACTORS
from utils.logger import setup_logger

logger = setup_logger("Analytics")

class TrafficAnalytics:
    """Calculates traffic metrics, signal timing splits, emissions, and corridor diversion recommendations."""
    def __init__(self):
        # Precise road load weights
        self.road_load_weights = {
            "car": 1.0,
            "motorcycle": 0.5,
            "bicycle": 0.3,
            "rider": 0.5,
            "pedestrian": 0.2,
            "bus": 3.0,
            "truck": 4.0,
            "train": 5.0
        }
        self.emission_factors = EMISSION_FACTORS

    def analyze_frame(
        self,
        tracking_output: Dict[str, Any],
        frame_width: int = 1920,
        frame_height: int = 1080
    ) -> Dict[str, Any]:
        """Calculates detailed analytics, signal optimization, and route diversion for a single frame."""
        tracks = tracking_output.get("tracks", [])
        directions = tracking_output.get("directions", {})
        frame_area = max(1, frame_width * frame_height)

        class_distribution: Dict[str, int] = {}
        road_load = 0.0
        total_box_area = 0.0
        heavy_vehicle_count = 0

        for track in tracks:
            cls_name = track.get("class", "car")
            class_distribution[cls_name] = class_distribution.get(cls_name, 0) + 1

            # Step 1: Compute Weighted Road Load
            weight = self.road_load_weights.get(cls_name, 1.0)
            road_load += weight

            # Bounding box area for occupancy ratio calculation
            bbox = track.get("bbox", [0, 0, 0, 0])
            w = max(0, bbox[2] - bbox[0])
            h = max(0, bbox[3] - bbox[1])
            total_box_area += (w * h)

            if cls_name in ["bus", "truck", "train"]:
                heavy_vehicle_count += 1

        num_vehicles = len(tracks)
        heavy_ratio = round(heavy_vehicle_count / num_vehicles, 2) if num_vehicles > 0 else 0.0
        occupancy_ratio = round(min(1.0, total_box_area / frame_area), 3)

        # Determine Traffic Classification (Free Flow, Moderate Traffic, Heavy Traffic, Severe Congestion)
        if num_vehicles > 25 or occupancy_ratio > 0.40 or road_load > 80:
            density_label = "Severe Congestion"
        elif num_vehicles > 15 or occupancy_ratio > 0.25 or road_load > 50:
            density_label = "Heavy Traffic"
        elif num_vehicles > 5 or occupancy_ratio > 0.10 or road_load > 20:
            density_label = "Moderate Traffic"
        else:
            density_label = "Free Flow"

        # Step 2: Compute Congestion Index (0 to 100)
        pcu_score = min(60.0, (road_load / 100.0) * 60.0)
        occupancy_score = min(30.0, (occupancy_ratio / 0.40) * 30.0)
        heavy_score = heavy_ratio * 10.0
        congestion_score = round(min(100.0, pcu_score + occupancy_score + heavy_score), 1)

        # Step 3: Signal Timing Optimization (Current Fixed Green vs AI Recommended Green)
        current_fixed_green = 30  # Standard static signal duration (seconds)

        if road_load < 40:
            rec_green = 20
        elif 40 <= road_load < 80:
            rec_green = 30
        elif 80 <= road_load < 120:
            rec_green = 40
        else:
            rec_green = 55

        green_improvement = rec_green - current_fixed_green

        # Step 4: Route Optimization & Traffic Diversion Engine
        # Assign dynamic costs to 4 monitored corridor approaches based on real-time directional movement & load
        ns_count = directions.get("North -> South", 0)
        sn_count = directions.get("South -> North", 0)
        we_count = directions.get("West -> East", 0)
        ew_count = directions.get("East -> West", 0)

        # Compute corridor congestion scores
        corridors = {
            "North Corridor": min(95.0, round(congestion_score * 1.1 + ns_count * 2.0, 1)),
            "South Corridor": min(90.0, round(congestion_score * 0.9 + sn_count * 1.5, 1)),
            "East Corridor": min(85.0, round(congestion_score * 0.6 + ew_count * 1.0, 1)),
            "West Corridor": min(80.0, round(congestion_score * 0.4 + we_count * 0.8, 1))
        }

        # Identify highest congestion corridor & best alternate corridor
        sorted_corridors = sorted(corridors.items(), key=lambda x: x[1])
        best_corridor, min_cost = sorted_corridors[0]
        worst_corridor, max_cost = sorted_corridors[-1]

        congestion_reduction_pct = round(max(0.0, (max_cost - min_cost) / (max_cost or 1.0)) * 100, 1)

        if max_cost > 60.0 and congestion_reduction_pct > 15.0:
            diversion_recommendation = f"AVOID {worst_corridor.upper()} ({max_cost:.0f}% Congested) → DIVERT TO {best_corridor.upper()} ({min_cost:.0f}% Cost, {congestion_reduction_pct:.0f}% Lower Congestion)"
            diversion_priority = "HIGH"
        elif max_cost > 35.0:
            diversion_recommendation = f"MODERATE CONGESTION: Recommend shifting traffic from {worst_corridor} to {best_corridor} ({congestion_reduction_pct:.0f}% improvement)"
            diversion_priority = "MEDIUM"
        else:
            diversion_recommendation = f"ALL CORRIDORS CLEAR: Optimal flow maintained across all approaches (Best Exit: {best_corridor})"
            diversion_priority = "LOW"

        # Step 5: Vehicle Emission Estimation (grams per minute)
        emissions = {"CO2": 0.0, "NOx": 0.0, "PM": 0.0}
        for cls_name, count in class_distribution.items():
            factors = self.emission_factors.get(cls_name, self.emission_factors["default"])
            emissions["CO2"] += factors["CO2"] * count
            emissions["NOx"] += factors["NOx"] * count
            emissions["PM"] += factors["PM"] * count

        return {
            "vehicles": num_vehicles,
            "class_distribution": class_distribution,
            "road_load": round(road_load, 1),
            "occupancy_ratio": occupancy_ratio,
            "density": density_label,
            "congestion_score": congestion_score,
            "heavy_vehicle_ratio": heavy_ratio,
            "signal_optimization": {
                "current_green_sec": current_fixed_green,
                "recommended_green_sec": rec_green,
                "improvement_sec": green_improvement
            },
            "route_optimization": {
                "corridor_scores": corridors,
                "best_corridor": best_corridor,
                "worst_corridor": worst_corridor,
                "congestion_reduction_pct": congestion_reduction_pct,
                "recommendation": diversion_recommendation,
                "priority": diversion_priority
            },
            "emissions_g_per_min": {k: round(v, 2) for k, v in emissions.items()}
        }
