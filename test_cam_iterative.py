#!/usr/bin/env python3
"""
Test script to verify the iterative CAM processing works correctly.
This simulates the iterative JSON merging functionality.
"""

import json
from utils.helpers import update_result_json

def test_iterative_cam_processing():
    """Test the iterative CAM processing with sample data"""
    
    print("=" * 80)
    print("Testing Iterative CAM Processing")
    print("=" * 80)
    
    # Initialize empty result dictionary
    cam_result = {}
    
    # Simulate first chunk response (CAM charges from page 1)
    chunk_1_response = json.dumps({
        "camCharges": [
            {
                "chargeCode": {
                    "value": "CAM-001",
                    "citation": "Page 1, Section 3.1"
                },
                "description": {
                    "value": "Common Area Maintenance - Year 1",
                    "citation": "Page 1, Section 3.1"
                },
                "monthlyAmount": {
                    "value": "$500",
                    "citation": "Page 1, Section 3.1"
                },
                "annualAmount": {
                    "value": "$6,000",
                    "citation": "Page 1, Section 3.1"
                }
            }
        ]
    })
    
    print("Processing Chunk 1 - CAM charges from page 1")
    cam_result = update_result_json(cam_result, chunk_1_response)
    print(f"After chunk 1: {len(cam_result.get('camCharges', []))} CAM charges")
    
    # Simulate second chunk response (additional CAM charges from page 2)
    chunk_2_response = json.dumps({
        "camCharges": [
            {
                "chargeCode": {
                    "value": "CAM-002",
                    "citation": "Page 2, Section 3.2"
                },
                "description": {
                    "value": "Common Area Maintenance - Year 2",
                    "citation": "Page 2, Section 3.2"
                },
                "monthlyAmount": {
                    "value": "$550",
                    "citation": "Page 2, Section 3.2"
                },
                "annualAmount": {
                    "value": "$6,600",
                    "citation": "Page 2, Section 3.2"
                }
            }
        ]
    })
    
    print("Processing Chunk 2 - Additional CAM charges from page 2")
    cam_result = update_result_json(cam_result, chunk_2_response)
    print(f"After chunk 2: {len(cam_result.get('camCharges', []))} CAM charges")
    
    # Simulate third chunk response (CAM definitions and rules from page 3)
    chunk_3_response = json.dumps({
        "camDefinitions": {
            "commonAreas": {
                "value": "Lobbies, hallways, elevators, parking areas, and landscaping",
                "citation": "Page 3, Section 4.1"
            },
            "calculationMethod": {
                "value": "Pro-rata share based on rentable square footage",
                "citation": "Page 3, Section 4.2"
            }
        },
        "camRules": {
            "billingFrequency": {
                "value": "Monthly",
                "citation": "Page 3, Section 4.3"
            },
            "capAmount": {
                "value": "5% annual increase",
                "citation": "Page 3, Section 4.4"
            }
        }
    })
    
    print("Processing Chunk 3 - CAM definitions and rules from page 3")
    cam_result = update_result_json(cam_result, chunk_3_response)
    print(f"After chunk 3: CAM definitions and rules added")
    
    # Simulate fourth chunk response (duplicate charge - should not be added)
    chunk_4_response = json.dumps({
        "camCharges": [
            {
                "chargeCode": {
                    "value": "CAM-001",
                    "citation": "Page 1, Section 3.1"
                },
                "description": {
                    "value": "Common Area Maintenance - Year 1",
                    "citation": "Page 1, Section 3.1"
                },
                "monthlyAmount": {
                    "value": "$500",
                    "citation": "Page 1, Section 3.1"
                },
                "annualAmount": {
                    "value": "$6,000",
                    "citation": "Page 1, Section 3.1"
                }
            }
        ]
    })
    
    print("Processing Chunk 4 - Duplicate charge (should not be added)")
    cam_result = update_result_json(cam_result, chunk_4_response)
    print(f"After chunk 4: {len(cam_result.get('camCharges', []))} CAM charges (should still be 2)")
    
    # Display final result
    print("\n" + "=" * 80)
    print("Final CAM Result:")
    print("=" * 80)
    print(json.dumps(cam_result, indent=2))
    
    # Verify results
    assert len(cam_result.get('camCharges', [])) == 2, f"Expected 2 CAM charges, got {len(cam_result.get('camCharges', []))}"
    assert 'camDefinitions' in cam_result, "CAM definitions should be present"
    assert 'camRules' in cam_result, "CAM rules should be present"
    
    print("\n✅ All tests passed! Iterative CAM processing works correctly.")
    return cam_result

if __name__ == "__main__":
    test_iterative_cam_processing()
