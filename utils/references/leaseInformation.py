structure = {
    "leaseInformation": {
      "lease": {
        "value": "", # value of the lease
        "citation": "", # page at which in the pdf is reasoning present
        "amendments": [] # 
      },
      "property": {
        "value": "",
        "citation": "",
        "amendments": []
      },
      "leaseFrom": {
        "value": "",
        "citation": "",
        "amendments": []
      },
      "leaseTo": {
        "value": "",
        "citation": "",
        "amendments": []
      }
    }
}

field_description = """
## leaseInformation
The main container object that holds all the extracted details related to a specific lease agreement.

### lease
This object contains details about the lease agreement's identifier.
* **value**: The name, title, or unique identifier of the lease document (e.g., "Commercial Lease Agreement").
* **citation**: The page number in the PDF where the lease's name or title is found.
* **amendments**: A list of any changes or modifications made specifically to the lease identifier over time.

### property
This object describes the physical property being leased.
* **value**: The address or legal description of the property (e.g., "123 Maple Street, Anytown, USA").
* **citation**: The page number where the property's address or description is located.
* **amendments**: A list containing details of any changes to the property description, such as adding or removing space.

### leaseFrom (Lessor)
This object identifies the party granting the lease (the landlord or owner).
* **value**: The full legal name of the lessor (e.g., "City Properties LLC").
* **citation**: The page number where the lessor is identified.
* **amendments**: A list of any recorded changes to the lessor's identity, such as a change in ownership.

### leaseTo (Lessee)
This object identifies the party receiving the lease (the tenant).
* **value**: The full legal name of the lessee (e.g., "Global Tech Inc.").
* **citation**: The page number where the lessee is identified.
* **amendments**: A list of any changes to the lessee's identity, such as a company name change.

"""