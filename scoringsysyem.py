from difflib import SequenceMatcher
from typing import Optional

# --- Sample car dataset ---
cars = [
    {"id": 1, "name": "Maruti Swift", "fuel": "Petrol", "mileage": 20, "year": 2018, "transmission": "Manual"},
    {"id": 2, "name": "Hyundai Creta", "fuel": "Diesel", "mileage": 17, "year": 2020, "transmission": "Automatic"},
    {"id": 3, "name": "Tata Nexon EV", "fuel": "Electric", "mileage": 0, "year": 2022, "transmission": "Automatic"},
    {"id": 4, "name": "Honda City", "fuel": "Petrol", "mileage": 18, "year": 2019, "transmission": "Manual"},
    {"id": 5, "name": "Mahindra XUV700", "fuel": "Diesel", "mileage": 15, "year": 2023, "transmission": "Automatic"},
    {"id": 6, "name": "Hyundai i20", "fuel": "Petrol", "mileage": 21, "year": 2021, "transmission": "Manual"},
]

# --- Utility: Similarity scoring ---
def similarity(a: str, b: str) -> float:
    """Returns a similarity ratio between two strings (0.0–1.0)"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# --- Main search function ---
def search_cars(
    query: str,
    fuel: Optional[str] = None,
    min_mileage: Optional[int] = None,
    max_mileage: Optional[int] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    transmission: Optional[str] = None
):
    query = query.lower().strip()

    # Step 1️⃣: Auto-suggestions (predictive typing)
    suggestions = [car["name"] for car in cars if query in car["name"].lower()]

    # Step 2️⃣: Compute similarity score for fuzzy-like matching
    results = []
    for car in cars:
        score = similarity(query, car["name"])
        
        # Step 3️⃣: Apply filters
        if fuel and car["fuel"].lower() != fuel.lower():
            continue
        if min_mileage and car["mileage"] < min_mileage:
            continue
        if max_mileage and car["mileage"] > max_mileage:
            continue
        if min_year and car["year"] < min_year:
            continue
        if max_year and car["year"] > max_year:
            continue
        if transmission and car["transmission"].lower() != transmission.lower():
            continue

        car_copy = car.copy()
        car_copy["relevance_score"] = round(score, 2)
        results.append(car_copy)

    # Step 4️⃣: Sort by similarity (relevance)
    results.sort(key=lambda x: x["relevance_score"], reverse=True)

    return {
        "query": query,
        "suggestions": suggestions,
        "results": results
    }


# --- Example executions ---
print("🔍 Example 1: Simple fuzzy search")
print(search_cars("swift"))

print("\n🔍 Example 2: Filtered search (diesel cars after 2019)")
print(search_cars("creta", fuel="Diesel", min_year=2019))

print("\n🔍 Example 3: Predictive typing (query='hyu')")
print(search_cars("hyu"))
