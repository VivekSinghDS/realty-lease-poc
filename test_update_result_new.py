"""
Example demonstrating how update_result_json works with the actual lease structure.

This shows how the function merges LLM responses into a cumulative lease JSON object.
"""
import json
from utils.helpers import update_result_json

# Example 1: Starting with empty lease, first iteration adds lease information
print("=" * 80)
print("Example 1: First iteration - Adding lease information")
print("=" * 80)

lease = {}

# Simulated first LLM response (partial data from first chunk)
llm_response_1 = json.dumps({
    "leaseInformation": {
        "lease": {
            "value": "Commercial Lease Agreement",
            "citation": "Page 1, Header",
            "amendments": []
        },
        "property": {
            "value": "123 Main Street, Building A",
            "citation": "Page 1, Section 1",
            "amendments": []
        }
    }
})

lease = update_result_json(lease, llm_response_1)
print("After iteration 1:")
print(json.dumps(lease, indent=2)[:500] + "...")
print(f"\nLeaseInformation filled: {bool(lease.get('leaseInformation', {}).get('lease', {}).get('value'))}")

# Example 2: Second iteration adds space information
print("\n" + "=" * 80)
print("Example 2: Second iteration - Adding space information")
print("=" * 80)

llm_response_2 = json.dumps({
    "space": {
        "unit": {
            "value": "Suite 200",
            "citation": "Page 2, Section 2.1",
            "amendments": []
        },
        "building": {
            "value": "Building A",
            "citation": "Page 2, Section 2.1",
            "amendments": []
        },
        "areaRentable": {
            "value": "5,000 sq ft",
            "citation": "Page 2, Section 2.2",
            "amendments": []
        }
    }
})

lease = update_result_json(lease, llm_response_2)
print("After iteration 2:")
print(f"Space unit: {lease.get('space', {}).get('unit', {}).get('value')}")
print(f"Space building: {lease.get('space', {}).get('building', {}).get('value')}")
print(f"Area rentable: {lease.get('space', {}).get('areaRentable', {}).get('value')}")

# Example 3: Third iteration adds base rent charges
print("\n" + "=" * 80)
print("Example 3: Third iteration - Adding base rent to charge schedules")
print("=" * 80)

llm_response_3 = json.dumps({
    "chargeSchedules": {
        "baseRent": [
            {
                "chargeCode": {
                    "value": "BR-001",
                    "citation": "Page 3, Section 3.1"
                },
                "description": {
                    "value": "Monthly Base Rent - Year 1",
                    "citation": "Page 3, Section 3.1"
                },
                "dateFrom": {
                    "value": "2024-01-01",
                    "citation": "Page 3, Section 3.1"
                },
                "dateTo": {
                    "value": "2024-12-31",
                    "citation": "Page 3, Section 3.1"
                },
                "monthlyAmount": {
                    "value": "$10,000",
                    "citation": "Page 3, Section 3.1"
                },
                "annualAmount": {
                    "value": "$120,000",
                    "citation": "Page 3, Section 3.1"
                },
                "amendments": []
            }
        ]
    }
})

lease = update_result_json(lease, llm_response_3)
print("After iteration 3:")
print(f"Base rent entries: {len(lease.get('chargeSchedules', {}).get('baseRent', []))}")
if lease.get('chargeSchedules', {}).get('baseRent'):
    print(f"First base rent monthly amount: {lease['chargeSchedules']['baseRent'][0]['monthlyAmount']['value']}")

# Example 4: Fourth iteration adds another base rent entry (Year 2)
print("\n" + "=" * 80)
print("Example 4: Fourth iteration - Adding Year 2 base rent")
print("=" * 80)

llm_response_4 = json.dumps({
    "chargeSchedules": {
        "baseRent": [
            {
                "chargeCode": {
                    "value": "BR-002",
                    "citation": "Page 3, Section 3.2"
                },
                "description": {
                    "value": "Monthly Base Rent - Year 2",
                    "citation": "Page 3, Section 3.2"
                },
                "dateFrom": {
                    "value": "2025-01-01",
                    "citation": "Page 3, Section 3.2"
                },
                "dateTo": {
                    "value": "2025-12-31",
                    "citation": "Page 3, Section 3.2"
                },
                "monthlyAmount": {
                    "value": "$10,500",
                    "citation": "Page 3, Section 3.2"
                },
                "annualAmount": {
                    "value": "$126,000",
                    "citation": "Page 3, Section 3.2"
                },
                "amendments": []
            }
        ]
    }
})

lease = update_result_json(lease, llm_response_4)
print("After iteration 4:")
print(f"Base rent entries: {len(lease.get('chargeSchedules', {}).get('baseRent', []))}")
print("All base rent entries:")
for i, rent in enumerate(lease.get('chargeSchedules', {}).get('baseRent', []), 1):
    print(f"  {i}. {rent['description']['value']}: {rent['monthlyAmount']['value']}")

# Example 5: Fifth iteration adds lease provisions
print("\n" + "=" * 80)
print("Example 5: Fifth iteration - Adding lease provisions")
print("=" * 80)

llm_response_5 = json.dumps({
    "otherLeaseProvisions": {
        "alterations": {
            "synopsis": {
                "value": "Tenant must obtain landlord's written consent for any alterations",
                "citation": "Page 8, Section 8.1",
                "amendments": []
            }
        },
        "parking": {
            "synopsis": {
                "value": "Tenant entitled to 10 reserved parking spaces",
                "citation": "Page 12, Section 12.3",
                "amendments": []
            }
        }
    }
})

lease = update_result_json(lease, llm_response_5)
print("After iteration 5:")
print(f"Alterations synopsis: {lease.get('otherLeaseProvisions', {}).get('alterations', {}).get('synopsis', {}).get('value')}")
print(f"Parking synopsis: {lease.get('otherLeaseProvisions', {}).get('parking', {}).get('synopsis', {}).get('value')}")

# Example 6: Sixth iteration adds executive summary
print("\n" + "=" * 80)
print("Example 6: Sixth iteration - Adding executive summary")
print("=" * 80)

llm_response_6 = json.dumps({
    "executiveSummary": {
        "value": "5-year commercial lease for 5,000 sq ft office space at $10,000/month base rent with annual increases."
    }
})

lease = update_result_json(lease, llm_response_6)
print("After iteration 6:")
print(f"Executive summary: {lease.get('executiveSummary', {}).get('value')}")

# Example 7: Test duplicate prevention for base rent
print("\n" + "=" * 80)
print("Example 7: Seventh iteration - Testing duplicate prevention")
print("=" * 80)

llm_response_7 = json.dumps({
    "chargeSchedules": {
        "baseRent": [
            {
                "chargeCode": {
                    "value": "BR-001",
                    "citation": "Page 3, Section 3.1"
                },
                "description": {
                    "value": "Monthly Base Rent - Year 1",
                    "citation": "Page 3, Section 3.1"
                },
                "dateFrom": {
                    "value": "2024-01-01",
                    "citation": "Page 3, Section 3.1"
                },
                "dateTo": {
                    "value": "2024-12-31",
                    "citation": "Page 3, Section 3.1"
                },
                "monthlyAmount": {
                    "value": "$10,000",
                    "citation": "Page 3, Section 3.1"
                },
                "annualAmount": {
                    "value": "$120,000",
                    "citation": "Page 3, Section 3.1"
                },
                "amendments": []
            }
        ]
    }
})

lease = update_result_json(lease, llm_response_7)
print("After iteration 7 (should not add duplicate):")
print(f"Base rent entries: {len(lease.get('chargeSchedules', {}).get('baseRent', []))} (should still be 2)")

print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)
print(f"Executive Summary: {lease.get('executiveSummary', {}).get('value')}")
print(f"Property: {lease.get('leaseInformation', {}).get('property', {}).get('value')}")
print(f"Space Unit: {lease.get('space', {}).get('unit', {}).get('value')}")
print(f"Area Rentable: {lease.get('space', {}).get('areaRentable', {}).get('value')}")
print(f"Base Rent Entries: {len(lease.get('chargeSchedules', {}).get('baseRent', []))}")
print(f"Alterations Provision: {lease.get('otherLeaseProvisions', {}).get('alterations', {}).get('synopsis', {}).get('value')[:50]}...")
print(f"Parking Provision: {lease.get('otherLeaseProvisions', {}).get('parking', {}).get('synopsis', {}).get('value')}")

print("\n" + "=" * 80)
print("Full JSON Structure (first 1000 chars):")
print("=" * 80)
full_json = json.dumps(lease, indent=2)
print(full_json[:1000] + "...")

