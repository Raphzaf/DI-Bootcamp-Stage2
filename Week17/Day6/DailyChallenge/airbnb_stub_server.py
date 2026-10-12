import json, logging, sys
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="[airbnb-stub] %(message)s")
mcp = FastMCP("airbnb-stub")

LISTINGS = {
    "lisbon": [("Sunny loft in Alfama", 96, 4.91), ("Bairro Alto studio with balcony", 82, 4.78), ("Belém riverside flat", 120, 4.88)],
    "paris": [("Montmartre artist studio", 135, 4.86), ("Marais 1-bedroom", 168, 4.93), ("Canal Saint-Martin flat", 118, 4.71)],
    "barcelona": [("Gràcia terrace apartment", 110, 4.84), ("Eixample design flat", 142, 4.9), ("Barceloneta beach studio", 99, 4.65)],
    "tel aviv": [("Neve Tzedek boutique loft", 155, 4.89), ("Rothschild Blvd apartment", 140, 4.8), ("Jaffa sea-view studio", 112, 4.75)],
}


@mcp.tool()
def airbnb_search(location: str, adults: int = 1, checkin: str = "", checkout: str = "") -> str:
    """Search Airbnb listings for a location (stub: fixed sample data). Returns JSON text like the real server."""
    city = next((c for c in LISTINGS if c in location.lower()), None)
    logging.info("search %r -> %s", location, city)
    if city is None:
        return json.dumps({"searchResults": [], "message": f"No stub data for {location!r}; try {list(LISTINGS)}"})
    results = [{"id": f"stub-{city[:3]}-{i}", "url": f"https://www.airbnb.com/rooms/stub-{city[:3]}-{i}",
                "name": name, "price_per_night_usd": price, "rating": rating, "guests": adults}
               for i, (name, price, rating) in enumerate(LISTINGS[city], 1)]
    return json.dumps({"searchResults": results, "checkin": checkin, "checkout": checkout})


@mcp.tool()
def airbnb_listing_details(id: str) -> str:
    """Details for one listing id (stub)."""
    return json.dumps({"id": id, "details": "Stub listing: wifi, kitchen, self check-in."})


if __name__ == "__main__":
    mcp.run()
