structure = {
    "otherLeaseProvisions": {
      "premisesAndTerm": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "keyParameters": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "narrative": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "taxes": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "definition": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "keyParameters": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "narrative": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "operatingExpenses": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "definition": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "keyParameters": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "billingTimeline": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "formulas": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "capitalRules": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "narrative": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "repairsAndMaintenance": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "narrative": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "alterations": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "signs": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "services": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "insurance": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "keyParameters": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "casualty": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "liabilityAndIndemnification": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "use": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "landlordsRightOfEntry": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "assignmentAndSubletting": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "parking": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "condemnation": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "holdover": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "quietEnjoyment": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "defaultAndRemedies": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "subordination": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "liens": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "hazardousMaterials": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "rulesAndRegulations": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "brokerage": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "estoppel": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "notices": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "rightOfFirstRefusalOffer": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "expansionAndRelocation": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      },
      "landlordDefault": {
        "synopsis": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      }
    }
}

field_descriptions = """

# Lease Data Structure Documentation

## otherLeaseProvisions
The main container object for various clauses, conditions, and special provisions detailed in the lease agreement. This section covers topics beyond the primary financial and space definitions.

---

### Common Field Definitions
Many sections below share a common structure. Here's what those fields represent:
* **synopsis**: A concise summary of the key points of the lease clause.
* **keyParameters**: Specific data points extracted from the clause, such as dates, amounts, percentages, or other critical terms.
* **narrative**: The full, verbatim text of the clause as it appears in the lease document.
* **definition**: The specific legal definition of a term as provided by the lease (e.g., what qualifies as a "Tax" or "Operating Expense").
* **citation**: The page number in the source document where the information is located.
* **amendments**: A list of any modifications or changes that apply to that specific piece of information.

---

### premisesAndTerm
Defines the leased property and the duration of the lease agreement.
* **synopsis**, **keyParameters**, **narrative**

### taxes
Details the tenant's and landlord's responsibilities regarding property taxes.
* **synopsis**, **definition**, **keyParameters**, **narrative**

### operatingExpenses
Details responsibilities for common area maintenance (CAM) and other shared building costs.
* **synopsis**, **definition**, **keyParameters**, **narrative**
* **billingTimeline**: The schedule and process for billing and reconciling operating expenses.
* **formulas**: The specific calculation used to determine the tenant's share of expenses.
* **capitalRules**: Rules defining if and how capital improvements can be included in operating expenses passed through to the tenant.

### repairsAndMaintenance
Outlines who is responsible for repairing and maintaining different parts of the premises and building.
* **synopsis**, **narrative**

### alterations
Specifies the tenant's rights and restrictions for making physical changes or improvements to the leased space.
* **synopsis**

### signs
Governs the tenant's rights to place signage on the property, including rules on size, location, and appearance.
* **synopsis**

### services
Lists the services the landlord is obligated to provide, such as HVAC, electricity, water, and janitorial services.
* **synopsis**

### insurance
Details the insurance coverage types and limits required for both the tenant and the landlord.
* **synopsis**, **keyParameters**

### casualty
Describes the procedures, rights, and obligations of both parties if the property is damaged or destroyed by events like a fire or natural disaster.
* **synopsis**

### liabilityAndIndemnification
Defines who is legally and financially responsible for injuries, damages, or lawsuits arising from incidents on the property.
* **synopsis**

### use
Specifies the permitted and prohibited uses of the leased premises by the tenant.
* **synopsis**

### landlordsRightOfEntry
Outlines the conditions under which the landlord can enter the tenant's space (e.g., for inspections, repairs, or showing the property).
* **synopsis**

### assignmentAndSubletting
Defines the tenant's ability to transfer the lease to another party (assignment) or lease a portion of their space to another entity (subletting).
* **synopsis**

### parking
Details the tenant's parking rights, including the number of spaces, location, and any associated costs.
* **synopsis**

### condemnation
Specifies the rights of the tenant and landlord if the property is acquired by a government entity through eminent domain.
* **synopsis**

### holdover
Describes the terms and financial penalties if the tenant remains in the space after the lease term has expired.
* **synopsis**

### quietEnjoyment
A covenant that grants the tenant the right to use the property without interference from the landlord.
* **synopsis**

### defaultAndRemedies
Outlines what constitutes a breach of the lease by either party and the actions the non-breaching party can take in response.
* **synopsis**

### subordination
Addresses the priority of the lease relative to the landlord's mortgage lender, often including non-disturbance and attornment provisions (SNDA).
* **synopsis**

### liens
Prohibits the tenant from allowing legal claims (liens) to be placed on the property, typically by contractors or suppliers.
* **synopsis**

### hazardousMaterials
Governs the use, storage, and disposal of hazardous materials on the premises.
* **synopsis**

### rulesAndRegulations
Refers to the general building rules and regulations that the tenant must adhere to.
* **synopsis**

### brokerage
Identifies the real estate brokers involved in the lease transaction and outlines commission agreements.
* **synopsis**

### estoppel
Describes the tenant's obligation to sign an estoppel certificate, a document that confirms the current terms of the lease for a third party, like a new owner or lender.
* **synopsis**

### notices
Specifies the official methods and addresses for sending legal notices between the tenant and landlord.
* **synopsis**

### rightOfFirstRefusalOffer
Details any right the tenant may have to match an offer to buy the property or lease additional space before it is offered to others.
* **synopsis**

### expansionAndRelocation
Outlines any rights the tenant has to expand into additional space or any obligation to relocate to a different space within the property at the landlord's request.
* **synopsis**

### landlordDefault
Specifies the tenant's remedies if the landlord fails to meet their obligations under the lease.
* **synopsis**

"""