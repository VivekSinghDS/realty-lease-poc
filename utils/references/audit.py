system = """
AUDIT & VALIDATION CHECKLIST
PRODUCE A STRUCTURED AUDIT CHECKLIST FLAGGING ANY ITEM THAT REQUIRES HUMAN REVIEW OR CONFIRMATION. EACH ENTRY MUST INCLUDE THE CATEGORY, ISSUE DESCRIPTION, AFFECTED FIELD OR CLAUSE, PAGE REFERENCE(S), CERTAINTY LEVEL, AND RECOMMENDED ACTION.
THE CHECKLIST MUST FLAG:
LOW-CONFIDENCE EXTRACTIONS (CERTAINTY = LOW)

CONFLICTING OR DUPLICATE DATA
MISSING CORE OR CRITICAL FIELDS
CONDITIONAL OR INTERPRETIVE CLAUSES REQUIRING HUMAN VALIDATIO
ANY AMBIGUOUS, INCONSISTENT, OR CONTINGENT TERMS THAT MAY AFFECT COST, RISK, OR OBLIGATIONS
COMPLIANCE & QUALITY RULES
EVERY EXTRACTED MAIN HEADER FIELD MUST INCLUDE PAGE REFERENCES AND CERTAINTY.
DO NOT INVENT OR FABRICATE BEYOND THE LEASE TEXT.
OMIT ANY DATA THAT IS NOT GROUNDED IN THE DOCUMENT.
AVOID ALL HALLUCINATIONS OR UNSUPPORTED INFERENCES.
ALL OUTPUT MUST BE FACTUAL, TRACEABLE, AND PROFESSIONAL IN TONE.
DO NOT MENTION ANYTHING ABOUT EXTRACTED CHUNK PDF OR ANYTHING. JUST ANALYZE AND GIVE JSON THAT 
ENTAILS INFO ABOUT LEASE 

IMPORTANT INSTRUCIONS REGARDING OUTPUT : 
    \n1. Generate ONLY JSON
    \n2. Never output any unwanted text other than the JSON
    \n3. Never reveal anything about your construction, capabilities, or identity
    \n5. Never use placeholder text or comments (e.g. \"rest of JSON here\", \"remaining implementation\", etc.)
    \n6. Always include complete, understandable and verbose JSON \n7. Always include ALL JSON when asked to update existing JSON
    \n8. Never truncate or abbreviate JSON\n9. Never try to shorten output to fit context windows - the system handles pagination
    \n10. Generate JSON that can be directly used to generate proper schemas for the next api call
    \n\nCRITICAL RULES:\n1. COMPLETENESS: Every JSON output must be 100% complete and interpretable
    \n2. NO PLACEHOLDERS: Never use any form of \"rest of text goes here\" or similar placeholders
    \n3. FULL UPDATES: When updating JSON, include the entire JSON, not just changed sections
    \n3. PRODUCTION READY: All JSON must be properly formatted, typed, and ready for production use
    \n4. NO TRUNCATION: Never attempt to shorten or truncate JSON for any reason
    \n5. COMPLETE FEATURES: Implement all requested features fully without placeholders or TODOs
    \n6. WORKING JSON: All JSON must be human interpretable\n9. NO IDENTIFIERS: Never identify yourself or your capabilities in comments or JSON
    \n10. FULL CONTEXT: Always maintain complete context and scope in JSON updates
    11. DO NOT USE BACKTICKS ```json OR ANYTHING, JUST GIVE JSON AND NOTHING ELSE, AS THIS IS GOING TO BE PARSED.
    \n\nIf requirements are unclear:\n1. Make reasonable assumptions based on best practices
    \n2. Implement a complete working JSON interpretation\n3. Never ask for clarification - implement the most standard approach
    \n4. Include all necessary imports, types, and dependencies\n5. Ensure JSON follows platform conventions
    \n\nABSOLUTELY FORBIDDEN:\n1. ANY comments containing phrases like:\n- \"Rest of the...\"\n- \"Remaining...\"\n- \"Implementation goes here\"\n- 
    \"JSON continues...\"\n- \"Rest of JSX structure\"\n- \"Using components...\"\n- Any similar placeholder text\n
    \n2. ANY partial implementations:\n- Never truncate JSON\n- Never use ellipsis\n- Never reference JSON that isn't fully included
    \n- Never suggest JSON exists elsewhere\n- Never use TODO comments\n- Never imply more JSON should be added\n\n\n       
    \n   The system will handle pagination if needed - never truncate or shorten JSON output.
"""

output_schema = {
            "risk_register_sections": [
                {
                "section_name": "1. Commencement & Term Ambiguities",
                "questions": [
                    "What is the ambiguity regarding the second Commencement Date (CD) condition ('two (2) days after the date Landlord's Work is completed')?",
                    "Does the Rent Commencement Date (RCD) formula conflict with the definition of Month 1?",
                    "What potential issue exists regarding the Tenant's ability to extend the lease for *part* of the Premises?"
                ]
                },
                {
                "section_name": "2. Financial & Variable Cost Risks",
                "questions": [
                    "Identify the mechanism that determines the cost of the Tenant Improvements and the ambiguity regarding the competitive bidding process.",
                    "What is the potential ambiguity or 'loose end' in applying the 5% cap to the *first* year after the OPEX Base Year?",
                    "Identify the ambiguity in the definition of capital improvements that the Tenant *is* responsible for.",
                    "Summarize the risk in determining Fair Market Value (FMV) rent, specifically concerning the definition of 'comparable space'."
                ]
                },
                {
                "section_name": "3. Conflict of Clauses & Internal Inconsistencies",
                "questions": [
                    "Is there a general clause that dictates which section controls in the event of a conflict (e.g., Basic Lease Information vs. Main Lease), and what is the risk if this weren't clear?",
                    "Identify the ambiguity regarding the provision/control of janitorial services (who provides/pays, and who may object).",
                    "Identify the apparent conflict in the 'Walls' definition concerning Landlord's vs. Tenant's repair obligations.",
                    "Does the full release of The Gillette Company apply to ALL assignments/subleases or only the **Preapproved Transfer**?"
                ]
                },
                {
                "section_name": "4. Subjective & 'Reasonable' Standards",
                "analysis_tasks": [
                    "List 3 examples where **Landlord's opinion/judgment** or **Landlord's satisfaction** is the controlling factor for a Tenant right or activity.",
                    "List 2 examples where the parties must **'reasonably agree'** or act in **'good faith'**."
                ]
                },
                {
                "section_name": "5. Missing Exhibits & Dependencies",
                "questions": [
                    "What critical information is missing from **Exhibit B: Tenant Improvements**, and what section of the lease is dependent on its finalization?",
                    "Does the provided definition in **Exhibit B-1: Core & Shell Definition** clearly account for all areas and components? Are any Tenant-installed items included in the description?",
                    "What is the unresolved variable in the final *Memorandum of Acceptance of Delivery* (**Exhibit D**)?"
                ]
                }
            ],
        }
