from enum import Enum

from utils.references import chargeSchedules, executive_summary, leaseInformation, misc, space


CORS_CONFIG = {
    "allow_origins": ["*"],
    "allow_credentials": False,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["*"],
}

class AnalysisType(str, Enum):
    INFO = "info"
    SPACE = "space"
    CHARGE_SCHEDULES = "charge-schedules"
    MISC = "misc"
    EXECUTIVE_SUMMARY = "executive-summary"
    AUDIT = "audit"
    ALL = "all"
    
    
ANALYSIS_CONFIG = {
    AnalysisType.INFO: {
        "doc_indices": [0, 5],
        "structure": leaseInformation.structure
    },
    AnalysisType.SPACE: {
        "doc_indices": [1, 5],
        "structure": space.structure
    },
    AnalysisType.CHARGE_SCHEDULES: {
        "doc_indices": [2, 5],
        "structure": chargeSchedules.structure
    },
    AnalysisType.MISC: {
        "doc_indices": [3, 5],
        "structure": misc.structure
    },
    AnalysisType.EXECUTIVE_SUMMARY: {
        "doc_indices": [4, 5],
        "structure": executive_summary.structure
    }
}