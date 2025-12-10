# Naukri.com Location Configuration with cityTypeGid mappings
# Based on Naukri's location parameter system

# Top Indian Cities (Primary Markets)
NAUKRI_INDIA_CITIES = {
    "Bangalore": "6",
    "Mumbai": "17", 
    "Pune": "51",
    "Chennai": "73",
    "Hyderabad": "97",
    "Delhi/NCR": "123",
    "Kolkata": "134",
    "Ahmedabad": "139",
    "Gurgaon": "165",
    "Noida": "173",
    "Chandigarh": "177",
    "Jaipur": "183",
    "Kochi": "220",
    "Coimbatore": "232"
}

# International Locations
NAUKRI_INTERNATIONAL = {
    "USA": "9001",
    "UK": "9003",
    "Canada": "9005",
    "Australia": "9009",
    "Singapore": "9034",
    "Dubai/UAE": "9042",
    "Saudi Arabia": "9043",
    "Germany": "9044",
    "Netherlands": "9080",
    "Ireland": "9508",
    "New Zealand": "9509"
}

# Combined all locations
NAUKRI_ALL_LOCATIONS = {**NAUKRI_INDIA_CITIES, **NAUKRI_INTERNATIONAL}

# Function to build Naukri URL with multiple cityTypeGid
def build_naukri_location_url(base_url: str, city_gids: list[str]) -> str:
    """Build Naukri URL with cityTypeGid parameters"""
    params = "&".join([f"cityTypeGid={gid}" for gid in city_gids])
    return f"{base_url}?{params}"
