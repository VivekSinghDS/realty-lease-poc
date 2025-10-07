structure = {
    "space": {
      "unit": {
        "value": "",
        "citation": "",
        "amendments": []
      },
      "building": {
        "value": "",
        "citation": "",
        "amendments": []
      },
      "floor": {
        "value": "",
        "citation": "",
        "amendments": []
      },
      "areaRentable": {
        "value": "",
        "citation": "",
        "amendments": []
      },
      "areaUsable": {
        "value": "",
        "citation": "",
        "amendments": []
      },
      "status": {
        "value": "",
        "citation": "",
        "amendments": []
      },
      "notes": {
        "value": "",
        "citation": "",
        "amendments": []
      }
    }
}

field_descriptions = """
## space
The main container object that holds all specific details about the physical space being leased.

### unit
This object identifies the specific suite or unit number within the building.
* **value**: The identifier for the unit (e.g., "Suite 450", "Unit 3B").
* **citation**: The page number in the PDF where this unit is mentioned.
* **amendments**: A list of any changes to the unit's designation.

### building
This object contains the name or identifier of the building where the unit is located.
* **value**: The official name or number of the building (e.g., "The Apex Tower", "Building C").
* **citation**: The page number where the building is identified.
* **amendments**: A list of any changes to the building's name or identifier.

### floor
This object specifies the floor on which the leased space is located.
* **value**: The floor level (e.g., "12th Floor", "Mezzanine").
* **citation**: The page number where the floor is mentioned.
* **amendments**: A list of any updates related to the floor designation.

### areaRentable
This object describes the rentable area, which typically includes the usable area plus a portion of the building's common spaces.
* **value**: The total rentable square footage or meters (e.g., "10,000 sq ft").
* **citation**: The page number specifying the rentable area.
* **amendments**: A list of any recalculations or changes to the rentable area.

### areaUsable
This object describes the usable area, which is the actual space exclusively occupied by the tenant.
* **value**: The total usable square footage or meters (e.g., "9,200 sq ft").
* **citation**: The page number specifying the usable area.
* **amendments**: A list of any recalculations or changes to the usable area.

### status
This object indicates the current status of the space.
* **value**: The current availability or condition (e.g., "Occupied", "Available for Lease", "Under Renovation").
* **citation**: The page number where the status is mentioned.
* **amendments**: A list of any changes to the space's status over time.

### notes
This object is for any additional, miscellaneous information about the space.
* **value**: Any relevant notes or comments (e.g., "Space includes a private balcony", "As-is condition").
* **citation**: The page number where these notes are found.
* **amendments**: A list of any updates or additions to the notes.

"""