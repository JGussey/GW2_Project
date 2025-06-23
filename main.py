import base64
import json
import requests
import struct
import os

# --- Configuration ---
# Base URL for the Guild Wars 2 API
GW2_API_BASE_URL = "https://api.guildwars2.com/v2/"
# Directory to save builds. Will be created if it doesn't exist.
BUILDS_DIR = "saved_builds"

# --- Utility Functions ---


def fetch_api_data(endpoint, params=None):
    """
    Fetches data from the Guild Wars 2 API.
    Args:
        endpoint (str): The API endpoint (e.g., "professions", "skills/123").
        params (dict, optional): Dictionary of query parameters. Defaults to None.
    Returns:
        dict or list: JSON response from the API, or None on error.
    """
    url = f"{GW2_API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GW2 API ({url}): {e}")
        return None


def ensure_builds_directory_exists():
    """Ensures the directory for saving builds exists."""
    os.makedirs(
        BUILDS_DIR, exist_ok=True)  # exist_ok=True prevents error if dir already exists
    print(f"Ensured '{BUILDS_DIR}' directory exists.")

# --- Build Link Encoding/Decoding (Core Logic - This is complex!) ---

# Placeholder for build code version, profession, specializations, traits, skills, etc.
# The actual structure of GW2 build links is quite specific and involves byte packing.
# This part will require careful research into GW2 build code specification.
# Example specification (search for something similar):
# https://wiki.guildwars2.com/wiki/Chat_link_format#Build_links


def decode_build_link(link_string):
    """
    Decodes an in-game Guild Wars 2 build link string.
    This is a simplified example and will need to be much more robust.
    Args:
        link_string (str): The base64-encoded build link (e.g., "[&DQYAAAA...=]").
    Returns:
        dict: A dictionary representing the decoded build, or None if invalid.
    """
    if not link_string.startswith("[&") or not link_string.endswith("]"):
        print(
            "Invalid build link format. Must start with '[&' and end with ']'.")
        return None

    # Remove "[&" and "]" and decode base64
    base64_part = link_string[2:-1]
    try:
        decoded_bytes = base64.b64decode(base64_part)
    except base64.binascii.Error as e:
        print(f"Error decoding base64 part of the link: {e}")
        return None

    # The actual parsing of decoded_bytes is highly specific to GW2 build links.
    # It involves reading specific bytes for version, profession, specializations,
    # traits, skills, equipment, etc. This is where you'll spend significant time
    # researching and implementing based on community specifications.

    # For now, a very basic demonstration:
    if not decoded_bytes:
        return None

    print(f"Decoded bytes (raw): {decoded_bytes.hex()}")

    # Example: If the first byte indicates version, second indicates profession (highly simplified)
    # This is NOT the real GW2 build code structure, just for illustration!
    try:
        # Link type is often the first byte (e.g., 0x0A for build links)
        link_type = decoded_bytes[0]
        # Version is often the second byte
        version = decoded_bytes[1]
        # Profession ID is often the third byte
        profession_id = decoded_bytes[2]

        print(f"Link Type: {hex(link_type)}")
        print(f"Version: {version}")
        print(f"Profession ID (simplified): {profession_id}")

        # You would then map profession_id back to a name using the GW2 API
        # professions = fetch_api_data("professions", params={"ids": "all"})
        # profession_name = next((p["name"] for p in professions if p["id"] == profession_id), "Unknown")

        return {
            "link_type": hex(link_type),
            "version": version,
            # You'd get the actual profession here
            "profession_id_simplified": profession_id,
            "raw_bytes_hex": decoded_bytes.hex(),
            "note": "Decoding is complex and requires full GW2 build code spec."
        }
    except IndexError:
        print("Decoded bytes too short for basic parsing. Invalid build code structure.")
        return None


def encode_build_link(build_data):
    """
    Encodes a build_data dictionary into an in-game Guild Wars 2 build link string.
    This will be the most complex part of the project.
    Args:
        build_data (dict): A dictionary representing the build (profession, skills, traits, etc.).
    Returns:
        str: The base64-encoded build link string (e.g., "[&DQYAAAA...=]"), or None on error.
    """
    print("Encoding build link is a complex task and requires precise byte packing.")
    print("You'll need to map all build data (profession, skills, traits) to their GW2 IDs,")
    print("then pack them into a specific byte array, and finally base64 encode.")

    # Example: A very, very simplified byte array for a theoretical build link
    # This does NOT represent a real GW2 build link.
    # A real link has many more bytes for spec lines, traits, skills, equipment, etc.
    # For a guardian using Firebrand, for example:
    # First byte: 0x0A (build link type)
    # Second byte: Version (e.g., 1 for initial version)
    # Third byte: Profession ID (e.g., Guardian ID)
    # ... much more data for specs, traits, skills, equipment ...

    # This is a placeholder for the actual binary data that gets base64 encoded.
    # For a very basic example of struct.pack (not real GW2 data):
    # binary_data = struct.pack("<BBH", 0x0A, 1, 3) # Link type, version, some ID

    # A real build link encoding involves:
    # 1. Fetching all necessary IDs (profession, specialization, trait, skill, item).
    # 2. Converting build choices into bitfields and packed bytes.
    # 3. Using `struct.pack` or manual byte arrays for precise layout.

    # Example of what real GW2 build code bytes might look like (from wiki/parsers):
    # - Link type (0x0A for build)
    # - Version
    # - Profession ID (e.g., 2 for Guardian)
    # - Terrestrial/Aquatic spec lines (3 bytes each for specialization IDs + bitmask for traits)
    # - Healing, Utility, Elite skill IDs (3 bytes total + bitmask for underwater)
    # - Weapon set data (item IDs, infusions, runes)
    # - Etc.

    # For now, let's just return a dummy string.
    # You will implement the complex logic here.
    dummy_binary_data = b'\x0A\x01\x02\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C'
    encoded_string = base64.b64encode(dummy_binary_data).decode('utf-8')
    return f"[{encoded_string}]"  # GW2 links are wrapped in [&...=]

# --- Build Management (Saving/Loading) ---


def save_build(build_name, build_data):
    """
    Saves a build to a JSON file.
    Args:
        build_name (str): The name of the build (used as filename).
        build_data (dict): The build data to save.
    """
    ensure_builds_directory_exists()
    filepath = os.path.join(BUILDS_DIR, f"{build_name}.json")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(build_data, f, indent=4)
        print(f"Build '{build_name}' saved to {filepath}")
    except IOError as e:
        print(f"Error saving build '{build_name}': {e}")


def load_build(build_name):
    """
    Loads a build from a JSON file.
    Args:
        build_name (str): The name of the build to load.
    Returns:
        dict: The loaded build data, or None if not found/error.
    """
    filepath = os.path.join(BUILDS_DIR, f"{build_name}.json")
    if not os.path.exists(filepath):
        print(f"Build '{build_name}' not found at {filepath}")
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            build_data = json.load(f)
        print(f"Build '{build_name}' loaded successfully.")
        return build_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for build '{build_name}': {e}")
        return None
    except IOError as e:
        print(f"Error loading build '{build_name}': {e}")
        return None


def list_saved_builds():
    """Lists all saved build names."""
    ensure_builds_directory_exists()
    build_files = [f for f in os.listdir(BUILDS_DIR) if f.endswith(".json")]
    if not build_files:
        print("No builds saved yet.")
        return []
    print("\n--- Saved Builds ---")
    build_names = [os.path.splitext(f)[0] for f in build_files]
    for i, name in enumerate(build_names):
        print(f"{i+1}. {name}")
    print("--------------------")
    return build_names


# --- Main Application Logic (CLI) ---

def create_new_build_cli():
    """Guides the user through creating a new build via CLI."""
    print("\n--- Create New Build ---")
    build = {}

    # 1. Get Profession (Class)
    professions = fetch_api_data("professions", params={"ids": "all"})
    if not professions:
        print("Could not fetch professions from GW2 API. Cannot create build.")
        return

    print("Available Professions:")
    for i, p in enumerate(sorted(professions, key=lambda x: x['name'])):
        print(f"{i+1}. {p['name']} ({p['id']})")

    while True:
        try:
            choice = input("Enter number for your profession: ")
            chosen_profession_name = sorted(professions, key=lambda x: x['name'])[
                int(choice)-1]['name']
            chosen_profession_id = sorted(professions, key=lambda x: x['name'])[
                int(choice)-1]['id']
            build["profession"] = {
                "name": chosen_profession_name, "id": chosen_profession_id}
            print(f"Selected Profession: {chosen_profession_name}")
            break
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")

    # 2. Get Specializations and Traits (Simplified for now)
    build["specializations"] = []
    print("\n--- Specializations (Choose 3) ---")
    for i in range(3):
        # Fetch specializations for the chosen profession
        # This is a simplification; a full implementation would filter by profession and type (e.g., core vs elite)
        all_specs = fetch_api_data("specializations", params={"ids": "all"})
        if not all_specs:
            print("Could not fetch specializations. Skipping.")
            break

        print(f"Choose Specialization {i+1}:")
        # Filter specializations that belong to the chosen profession
        # GW2 API /v2/specializations doesn't directly link to professions in its initial response,
        # you'd need to map based on 'professions' array in spec data or know common ones.
        # For simplicity, we'll just show some names.
        available_specs = [s for s in all_specs if s.get(
            # Simplified filter
            'profession') == chosen_profession_name or not s.get('profession')]

        if not available_specs:
            print(
                f"No specializations found for {chosen_profession_name} or general. Skipping specialization selection.")
            break

        for j, spec_item in enumerate(sorted(available_specs, key=lambda x: x['name'])):
            print(f"{j+1}. {spec_item['name']}")

        while True:
            try:
                spec_choice_idx = int(
                    input(f"Enter number for Specialization {i+1}: ")) - 1
                chosen_spec = sorted(available_specs, key=lambda x: x['name'])[
                    spec_choice_idx]

                # Now select traits for this specialization (simplified)
                chosen_traits = []
                print(
                    f"Choosing Traits for {chosen_spec['name']} (Select 3, or type 's' to skip remaining):")
                # Basic, adept, master, grandmaster tiers
                # Simplified for display
                tier_names = ['minor_traits', 'major_traits']
                major_trait_ids = []
                for t_id in chosen_spec.get('major_traits', []):
                    major_trait_ids.append(t_id)

                all_traits = fetch_api_data(
                    "traits", params={"ids": ",".join(map(str, major_trait_ids))})

                if not all_traits:
                    print(
                        f"No major traits found for {chosen_spec['name']} or API error. Skipping traits.")
                else:
                    selected_major_traits = []
                    for k in range(3):  # For adept, master, grandmaster major traits
                        print(
                            f"Select Major Trait {k+1} for {chosen_spec['name']}:")

                        # Group traits by tier. GW2 traits have "tier" property (0,1,2 for adept, master, grandmaster)
                        # We need to present choices from each tier.

                        # Fetch and display traits for the current tier
                        current_tier_traits = [
                            t for t in all_traits
                            if t.get('tier') == k and t.get('id') not in [st['id'] for st in selected_major_traits]
                        ]

                        if not current_tier_traits:
                            print(
                                f"No more traits for tier {k} or all selected.")
                            continue

                        for l, trait_item in enumerate(sorted(current_tier_traits, key=lambda x: x['name'])):
                            print(f"{l+1}. {trait_item['name']}")

                        trait_input = input(
                            "Enter number for trait or 's' to skip: ").lower()
                        if trait_input == 's':
                            break
                        try:
                            trait_choice_idx = int(trait_input) - 1
                            chosen_trait = sorted(current_tier_traits, key=lambda x: x['name'])[
                                trait_choice_idx]
                            selected_major_traits.append(
                                {"name": chosen_trait['name'], "id": chosen_trait['id']})
                            print(f"Selected Trait: {chosen_trait['name']}")
                        except (ValueError, IndexError):
                            print(
                                "Invalid input for trait. Skipping trait selection for this tier.")

                build["specializations"].append({
                    "name": chosen_spec["name"],
                    "id": chosen_spec["id"],
                    "traits": selected_major_traits  # Store selected major traits
                })
                break
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid number for specialization.")

    # 3. Skills (Simplified for now)
    build["skills"] = {}
    print("\n--- Skills (Heal, Utility x3, Elite) ---")
    # This part would involve fetching skills and allowing selection.
    # GW2 skill IDs are tied to profession and specific slots.
    # You'd need to know the profession's skill IDs from the API.

    # Example: Just asking for names for now, you'll replace with ID lookup
    build["skills"]["heal"] = input("Enter Heal Skill Name: ")
    build["skills"]["utility1"] = input("Enter Utility Skill 1 Name: ")
    build["skills"]["utility2"] = input("Enter Utility Skill 2 Name: ")
    build["skills"]["utility3"] = input("Enter Utility Skill 3 Name: ")
    build["skills"]["elite"] = input("Enter Elite Skill Name: ")

    # For now, let's just make sure we have equipment keys
    # This will be the last and most complex part to implement fully
    build["equipment"] = {}

    print("\n--- Build Created ---")
    print(json.dumps(build, indent=2))

    build_name = input("\nEnter a name to save this build: ")
    if build_name:
        save_build(build_name, build)

    # After creating and saving, attempt to encode (will be a dummy link for now)
    encoded_link = encode_build_link(build)
    if encoded_link:
        print(f"\nGenerated (Dummy) In-Game Build Link: {encoded_link}")
        print("Copy this link and paste it in-game to test when encoding is fully implemented!")


def main_menu():
    """Displays the main menu and handles user choices."""
    ensure_builds_directory_exists()  # Make sure the directory exists on startup
    print("\nWelcome to your GW2 Build Manager!")
    while True:
        print("\n--- Main Menu ---")
        print("1. Create New Build")
        print("2. View/Load Saved Builds")
        print("3. Decode an Existing In-Game Build Link")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_new_build_cli()
        elif choice == '2':
            build_names = list_saved_builds()
            if build_names:
                while True:
                    view_choice = input(
                        "Enter build name to load (or 'b' to go back): ").strip()
                    if view_choice.lower() == 'b':
                        break
                    loaded_build = load_build(view_choice)
                    if loaded_build:
                        print("\n--- Loaded Build Details ---")
                        print(json.dumps(loaded_build, indent=2))
                        # Here you could offer to encode it again, edit it, etc.
                        break
        elif choice == '3':
            link_to_decode = input(
                "Enter the in-game build link (e.g., '[&DQYAAAA...=]'): ")
            decoded_info = decode_build_link(link_to_decode)
            if decoded_info:
                print("\n--- Decoded Link Information ---")
                print(json.dumps(decoded_info, indent=2))
        elif choice == '4':
            print("Exiting GW2 Build Manager. Happy adventuring!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
