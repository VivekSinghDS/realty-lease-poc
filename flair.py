import json
import os
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

def combine_cam_pages(folder_path: str = "./cam_result") -> Dict[str, Any]:
    """
    Combines iterative CAM rule analysis results from multiple pages into a single JSON.
    
    Args:
        folder_path: Path to folder containing page result JSON/TXT files
        
    Returns:
        Combined JSON with all pages aggregated
    """
    
    # Get all JSON/TXT files sorted by page number
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Folder '{folder_path}' not found")
    
    files = sorted(
        [f for f in folder.glob("*.txt") if f.is_file()] + 
        [f for f in folder.glob("*.json") if f.is_file()],
        key=lambda x: extract_page_number(x.name)
    )
    
    if not files:
        raise ValueError(f"No JSON or TXT files found in '{folder_path}'")
    
    # Initialize combined structure
    combined = {
        "documentAnalysis": {
            "totalPages": 0,
            "analysisTimestamp": None,
            "pageRange": {"start": None, "end": None}
        },
        "allPages": [],
        "combinedRules": {
            "newCamRules": [],
            "continuedRules": [],
            "crossPageContext": []
        },
        "aggregatedFlags": {
            "ambiguities": [],
            "conflicts": [],
            "missingProvisions": [],
            "tenantConcerns": [],
            "provisionsSpanningToNextPage": []
        },
        "finalCamRulesSummary": {
            "totalRulesExtracted": 0,
            "rulesByCategory": defaultdict(int),
            "overallTenantRiskAssessment": "Low",
            "keyTenantProtections": [],
            "keyTenantExposures": [],
            "allExtractedRules": []
        }
    }
    
    # Process each page file
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                page_data = json.load(f)
            
            # Extract page info
            page_info = page_data.get("pageAnalysis", {})
            current_page = page_info.get("currentPage", 0)
            
            # Update document-level info
            combined["documentAnalysis"]["totalPages"] = max(
                combined["documentAnalysis"]["totalPages"], 
                current_page
            )
            
            if combined["documentAnalysis"]["pageRange"]["start"] is None:
                combined["documentAnalysis"]["pageRange"]["start"] = current_page
            combined["documentAnalysis"]["pageRange"]["end"] = current_page
            
            if not combined["documentAnalysis"]["analysisTimestamp"]:
                combined["documentAnalysis"]["analysisTimestamp"] = page_info.get("analysisTimestamp")
            
            # Store individual page data
            combined["allPages"].append({
                "page": current_page,
                "data": page_data
            })
            
            # Aggregate rules
            new_rules = page_data.get("newCamRules", [])
            for rule in new_rules:
                rule["sourcePage"] = current_page
                combined["combinedRules"]["newCamRules"].append(rule)
            
            continued_rules = page_data.get("continuedRules", [])
            for rule in continued_rules:
                rule["sourcePage"] = current_page
                combined["combinedRules"]["continuedRules"].append(rule)
            
            cross_page = page_data.get("crossPageContext", [])
            for item in cross_page:
                item["sourcePage"] = current_page
                combined["combinedRules"]["crossPageContext"].append(item)
            
            # Aggregate flags
            flags = page_data.get("flagsAndObservations", {})
            for flag_type in ["ambiguities", "conflicts", "missingProvisions", 
                            "tenantConcerns", "provisionsSpanningToNextPage"]:
                items = flags.get(flag_type, [])
                for item in items:
                    if isinstance(item, dict):
                        item["page"] = current_page
                    else:
                        item = {"description": item, "page": current_page}
                    combined["aggregatedFlags"][flag_type].append(item)
            
            # Aggregate summary data
            summary = page_data.get("cumulativeCamRulesSummary", {})
            
            # Sum up rules by category
            category_counts = summary.get("rulesByCategory", {})
            for category, count in category_counts.items():
                combined["finalCamRulesSummary"]["rulesByCategory"][category] += count
            
            # Collect all extracted rules
            all_rules = page_data.get("allExtractedRules", [])
            for rule in all_rules:
                if isinstance(rule, dict):
                    rule["sourcePage"] = current_page
                combined["finalCamRulesSummary"]["allExtractedRules"].append(rule)
            
            # Collect protections and exposures (deduplicate later)
            protections = summary.get("keyTenantProtections", [])
            exposures = summary.get("keyTenantExposures", [])
            
            for item in protections:
                if isinstance(item, dict):
                    item["page"] = current_page
                else:
                    item = {"description": item, "page": current_page}
                combined["finalCamRulesSummary"]["keyTenantProtections"].append(item)
            
            for item in exposures:
                if isinstance(item, dict):
                    item["page"] = current_page
                else:
                    item = {"description": item, "page": current_page}
                combined["finalCamRulesSummary"]["keyTenantExposures"].append(item)
                
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse {file_path.name}: {e}")
            continue
        except Exception as e:
            print(f"Warning: Error processing {file_path.name}: {e}")
            continue
    
    # Calculate total rules extracted
    combined["finalCamRulesSummary"]["totalRulesExtracted"] = len(
        combined["finalCamRulesSummary"]["allExtractedRules"]
    )
    
    # Convert defaultdict to regular dict
    combined["finalCamRulesSummary"]["rulesByCategory"] = dict(
        combined["finalCamRulesSummary"]["rulesByCategory"]
    )
    
    # Deduplicate protections and exposures
    combined["finalCamRulesSummary"]["keyTenantProtections"] = deduplicate_items(
        combined["finalCamRulesSummary"]["keyTenantProtections"]
    )
    combined["finalCamRulesSummary"]["keyTenantExposures"] = deduplicate_items(
        combined["finalCamRulesSummary"]["keyTenantExposures"]
    )
    
    # Assess overall risk based on exposures vs protections
    combined["finalCamRulesSummary"]["overallTenantRiskAssessment"] = assess_risk(
        len(combined["finalCamRulesSummary"]["keyTenantExposures"]),
        len(combined["finalCamRulesSummary"]["keyTenantProtections"]),
        len(combined["aggregatedFlags"]["tenantConcerns"])
    )
    
    return combined


def extract_page_number(filename: str) -> int:
    """Extract page number from filename (e.g., 'page_1.json' -> 1)"""
    import re
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0


def deduplicate_items(items: List[Any]) -> List[Any]:
    """Deduplicate items while preserving order and page references"""
    seen = {}
    result = []
    
    for item in items:
        if isinstance(item, dict):
            key = item.get("description", str(item))
        else:
            key = str(item)
        
        if key not in seen:
            seen[key] = item
            result.append(item)
        elif isinstance(item, dict) and isinstance(seen[key], dict):
            # Merge page references
            if "page" in item and "pages" not in seen[key]:
                seen[key]["pages"] = [seen[key].get("page")]
            if "page" in item and item["page"] not in seen[key].get("pages", []):
                seen[key].setdefault("pages", []).append(item["page"])
    
    return result


def assess_risk(exposures: int, protections: int, concerns: int) -> str:
    """Assess overall tenant risk level"""
    risk_score = exposures + concerns - protections
    
    if risk_score <= 2:
        return "Low"
    elif risk_score <= 5:
        return "Moderate"
    elif risk_score <= 10:
        return "High"
    else:
        return "Very High"


def save_combined_result(combined: Dict[str, Any], output_path: str = "combined_cam_analysis.json"):
    """Save combined result to JSON file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Combined analysis saved to {output_path}")


# Example usage
if __name__ == "__main__":
    try:
        # Combine all pages
        result = combine_cam_pages("cam_result")
        
        # Save to file
        save_combined_result(result)
        
        # Print summary
        print(f"\n=== Analysis Summary ===")
        print(f"Total Pages Analyzed: {result['documentAnalysis']['totalPages']}")
        print(f"Total Rules Extracted: {result['finalCamRulesSummary']['totalRulesExtracted']}")
        print(f"Overall Risk Assessment: {result['finalCamRulesSummary']['overallTenantRiskAssessment']}")
        print(f"Total Tenant Concerns: {len(result['aggregatedFlags']['tenantConcerns'])}")
        print(f"Key Protections: {len(result['finalCamRulesSummary']['keyTenantProtections'])}")
        print(f"Key Exposures: {len(result['finalCamRulesSummary']['keyTenantExposures'])}")
        
    except Exception as e:
        print(f"Error: {e}")