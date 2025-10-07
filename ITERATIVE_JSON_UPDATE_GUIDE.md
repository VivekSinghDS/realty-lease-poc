# Iterative JSON Update Implementation Guide

## Overview

The `update_result_json` function has been implemented to iteratively build a complete lease JSON by merging responses from multiple LLM calls as you process PDF chunks.

## How It Works

### 1. **Initialization**
When the `lease` variable starts as an empty dict `{}`, the function automatically loads the complete template structure from `utils/references/lease_structure_template.json`.

### 2. **Deep Merge Strategy**
The function performs a deep merge of each LLM response into the cumulative `lease` JSON:

- **Dictionaries**: Merged recursively, preserving existing values and adding new ones
- **Lists**: New items are appended, with duplicate detection to prevent redundant entries
- **Primitive values**: Updated only if the new value is meaningful (not empty string or default "string" value)

### 3. **Duplicate Prevention**
For list items (like `baseRent` entries), the function checks for duplicates based on:
- Key fields: `citation`, `description`, `clause_name`, `value`
- Similarity threshold: 70% match on common fields
- This prevents the same entry from being added multiple times across iterations

## Usage in Code

### In `lease_abstraction.py`:

```python
# Initialize empty lease
lease = {}

for chunk in chunks:
    # ... process chunk ...
    
    # Get LLM response
    iterative_response = llm_adapter.get_non_streaming_response(payload)
    iterative_response_text = iterative_response.output_text
    
    # Iteratively update the lease JSON
    lease = update_result_json(lease, iterative_response_text)

# Return the complete lease
return lease
```

## JSON Structure

Your lease JSON follows this structure:

```json
{
  "executiveSummary": { "value": "" },
  "leaseInformation": {
    "lease": { "value": "", "citation": "", "amendments": [] },
    "property": { "value": "", "citation": "", "amendments": [] },
    "leaseFrom": { "value": "", "citation": "", "amendments": [] },
    "leaseTo": { "value": "", "citation": "", "amendments": [] }
  },
  "space": {
    "unit": { "value": "", "citation": "", "amendments": [] },
    "building": { "value": "", "citation": "", "amendments": [] },
    "floor": { "value": "", "citation": "", "amendments": [] },
    "areaRentable": { "value": "", "citation": "", "amendments": [] },
    "areaUsable": { "value": "", "citation": "", "amendments": [] },
    "status": { "value": "", "citation": "", "amendments": [] },
    "notes": { "value": "", "citation": "", "amendments": [] }
  },
  "chargeSchedules": {
    "baseRent": [
      {
        "chargeCode": { "value": "", "citation": "" },
        "description": { "value": "", "citation": "" },
        "dateFrom": { "value": "", "citation": "" },
        "dateTo": { "value": "", "citation": "" },
        "monthlyAmount": { "value": "", "citation": "" },
        "annualAmount": { "value": "", "citation": "" },
        "areaRentable": { "value": "", "citation": "" },
        "amountPerArea": { "value": "", "citation": "" },
        "managementFees": { "value": "", "citation": "" },
        "amendments": []
      }
    ],
    "lateFee": {
      "calculationType": { "value": "", "citation": "", "amendments": [] },
      "graceDays": { "value": "", "citation": "", "amendments": [] },
      "percent": { "value": "", "citation": "", "amendments": [] },
      "secondFeeCalculationType": { "value": "", "citation": "", "amendments": [] },
      "secondFeeGrace": { "value": "", "citation": "", "amendments": [] },
      "secondFeePercent": { "value": "", "citation": "", "amendments": [] },
      "perDayFee": { "value": "", "citation": "", "amendments": [] }
    }
  },
  "otherLeaseProvisions": {
    "premisesAndTerm": {
      "synopsis": { "value": "", "citation": "", "amendments": [] },
      "keyParameters": { "value": "", "citation": "", "amendments": [] },
      "narrative": { "value": "", "citation": "", "amendments": [] }
    },
    "taxes": { ... },
    "operatingExpenses": { ... },
    "repairsAndMaintenance": { ... },
    "alterations": { ... },
    "signs": { ... },
    "services": { ... },
    "insurance": { ... },
    "casualty": { ... },
    "liabilityAndIndemnification": { ... },
    "use": { ... },
    "landlordsRightOfEntry": { ... },
    "assignmentAndSubletting": { ... },
    "parking": { ... },
    "condemnation": { ... },
    "holdover": { ... },
    "quietEnjoyment": { ... },
    "defaultAndRemedies": { ... },
    "subordination": { ... },
    "liens": { ... },
    "hazardousMaterials": { ... },
    "rulesAndRegulations": { ... },
    "brokerage": { ... },
    "estoppel": { ... },
    "notices": { ... },
    "rightOfFirstRefusalOffer": { ... },
    "expansionAndRelocation": { ... },
    "landlordDefault": { ... }
  }
}
```

## Example Scenario

### Iteration 1 (Chunk 1 - Pages 1-2):
LLM returns:
```json
{
  "leaseInformation": {
    "lease": { "value": "Commercial Lease", "citation": "Page 1", "amendments": [] }
  }
}
```
**Result**: `lease` now has `leaseInformation.lease` populated

### Iteration 2 (Chunk 2 - Pages 3-4):
LLM returns:
```json
{
  "space": {
    "unit": { "value": "Suite 200", "citation": "Page 3", "amendments": [] }
  }
}
```
**Result**: `lease` now has both `leaseInformation.lease` AND `space.unit` populated

### Iteration 3 (Chunk 3 - Pages 5-6):
LLM returns:
```json
{
  "chargeSchedules": {
    "baseRent": [
      { "description": { "value": "Year 1 Rent", "citation": "Page 5" }, ... }
    ]
  }
}
```
**Result**: `lease` now has all previous data PLUS the new `baseRent` entry

### Iteration 4 (Chunk 4 - Pages 7-8):
LLM returns:
```json
{
  "chargeSchedules": {
    "baseRent": [
      { "description": { "value": "Year 2 Rent", "citation": "Page 7" }, ... }
    ]
  }
}
```
**Result**: `lease.chargeSchedules.baseRent` now has TWO entries (Year 1 and Year 2)

## Key Features

1. **Automatic Structure Initialization**: Empty lease automatically gets the full template
2. **Smart Merging**: Preserves all existing data while adding new information
3. **List Handling**: Appends to lists without duplicating entries
4. **Error Handling**: Gracefully handles malformed JSON from LLM responses
5. **Citation Tracking**: Maintains citation and amendment information for each field

## Testing

Run the test file to see the function in action:
```bash
python test_update_result_new.py
```

This will demonstrate:
- Starting with an empty lease
- Adding data across 7 iterations
- Merging into different parts of the structure
- Appending to lists (baseRent)
- Duplicate prevention
- Final complete JSON

## Implementation Files

- **Main function**: `utils/helpers.py` - `update_result_json()`
- **Helper functions**: `_deep_merge()`, `_item_exists_in_list()`, `_dicts_are_similar()`
- **Template**: `utils/references/lease_structure_template.json`
- **Usage**: `app/routers/lease_abstraction.py` (line 65)
- **Test**: `test_update_result_new.py`

