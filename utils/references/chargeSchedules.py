structure = {
    "chargeSchedules": {
      "baseRent": [
        {
          "chargeCode": {
            "value": "",
            "citation": ""
          },
          "description": {
            "value": "",
            "citation": ""
          },
          "dateFrom": {
            "value": "",
            "citation": ""
          },
          "dateTo": {
            "value": "",
            "citation": ""
          },
          "monthlyAmount": {
            "value": "",
            "citation": ""
          },
          "annualAmount": {
            "value": "",
            "citation": ""
          },
          "areaRentable": {
            "value": "",
            "citation": ""
          },
          "amountPerArea": {
            "value": "",
            "citation": ""
          },
          "managementFees": {
            "value": "",
            "citation": ""
          },
          "amendments": []
        }
      ],
      "lateFee": {
        "calculationType": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "graceDays": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "percent": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "secondFeeCalculationType": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "secondFeeGrace": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "secondFeePercent": {
          "value": "",
          "citation": "",
          "amendments": []
        },
        "perDayFee": {
          "value": "",
          "citation": "",
          "amendments": []
        }
      }
    }
}

field_descriptions = """

## chargeSchedules
The main container object that holds all information about payment schedules, including recurring charges like base rent and conditional charges like late fees.

### baseRent
An **array of objects**, where each object represents a specific period in the rent schedule. This structure allows for rent escalations over the lease term.

#### Fields within each `baseRent` object:
* **chargeCode**: An internal code used to classify this type of charge.
* **description**: A plain-text description of the rent period.
* **dateFrom**: The start date for this specific rent amount.
* **dateTo**: The end date for this specific rent amount.
* **monthlyAmount**: The total rent due each month during this period.
* **annualAmount**: The total rent for a full year during this period.
* **areaRentable**: The rentable area used for this calculation.
* **amountPerArea**: The rent calculated on a per-unit-area basis (e.g., per square foot).
* **managementFees**: Any management fees included in or associated with the base rent.
* **amendments**: A list of any modifications that apply to this specific rent period.

### lateFee
This object defines the rules and penalties for overdue payments.
* **calculationType**: The method used to determine the initial late fee (e.g., "Fixed Amount", "Percentage of Overdue Amount").
* **graceDays**: The number of days after the due date before a late fee is charged.
* **percent**: The percentage applied if `calculationType` is based on a percentage.
* **secondFeeCalculationType**: The method for calculating a subsequent or secondary late fee.
* **secondFeeGrace**: The number of additional days before the second late fee is applied.
* **secondFeePercent**: The percentage for the second late fee, if applicable.
* **perDayFee**: A fixed amount charged for each day the payment remains overdue.
"""