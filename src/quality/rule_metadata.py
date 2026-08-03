from __future__ import annotations


RULE_METADATA = {
    "MISSING_DATE_OF_BIRTH": {
        "category": "Completeness",
        "source_system": "Registration System",
        "business_impact": (
            "Age-based reporting, clinical rules, and cohort selection "
            "may be inaccurate."
        ),
        "recommendation": (
            "Review the patient registration record and obtain a valid "
            "date of birth."
        ),
    },
    "FUTURE_DATE_OF_BIRTH": {
        "category": "Validity",
        "source_system": "Registration System",
        "business_impact": (
            "Patient age calculations and clinical eligibility logic "
            "may fail."
        ),
        "recommendation": (
            "Correct the date of birth and add date-range validation "
            "during registration."
        ),
    },
    "INVALID_GENDER": {
        "category": "Conformance",
        "source_system": "Registration System",
        "business_impact": (
            "Demographic reporting and downstream mappings may be inconsistent."
        ),
        "recommendation": (
            "Map the value to an approved demographic code set."
        ),
    },
    "DUPLICATE_MRN": {
        "category": "Uniqueness",
        "source_system": "Registration System",
        "business_impact": (
            "Patients may be double-counted or matched to the wrong record."
        ),
        "recommendation": (
            "Review duplicate registration workflows and implement MRN "
            "uniqueness checks."
        ),
    },
    "ORPHAN_PATIENT": {
        "category": "Referential Integrity",
        "source_system": "Upstream Source System",
        "business_impact": (
            "The record cannot be reliably connected to a valid patient."
        ),
        "recommendation": (
            "Verify the patient identifier and reload the record after "
            "the patient master is corrected."
        ),
    },
    "NEGATIVE_LAB_RESULT": {
        "category": "Clinical Plausibility",
        "source_system": "Laboratory System",
        "business_impact": (
            "Clinical analytics and patient safety reporting may be misleading."
        ),
        "recommendation": (
            "Verify the result, test code, unit, and instrument interface mapping."
        ),
    },
    "IMPLAUSIBLE_LAB_RESULT": {
        "category": "Clinical Plausibility",
        "source_system": "Laboratory System",
        "business_impact": (
            "The result may distort clinical trends and research cohorts."
        ),
        "recommendation": (
            "Review the source result, unit conversion, and reference range."
        ),
    },
    "NEGATIVE_BILLED_AMOUNT": {
        "category": "Financial Validity",
        "source_system": "Billing System",
        "business_impact": (
            "Revenue, reimbursement, and financial reporting may be incorrect."
        ),
        "recommendation": (
            "Review the claim transaction and determine whether it should "
            "be represented as an adjustment or reversal."
        ),
    },
    "PAID_EXCEEDS_BILLED": {
        "category": "Financial Consistency",
        "source_system": "Billing System",
        "business_impact": (
            "Payment and reimbursement reports may overstate revenue."
        ),
        "recommendation": (
            "Reconcile the payment with the billed amount and adjustment records."
        ),
    },
    "MISSING_MEMBER_ID": {
        "category": "Completeness",
        "source_system": "Insurance System",
        "business_impact": (
            "Eligibility verification and claim submission may fail."
        ),
        "recommendation": (
            "Obtain the valid insurance member ID and update coverage records."
        ),
    },
    "DUPLICATE_COVERAGE": {
        "category": "Uniqueness",
        "source_system": "Insurance System",
        "business_impact": (
            "Coverage selection and payer reporting may be duplicated."
        ),
        "recommendation": (
            "Merge or deactivate duplicate coverage records."
        ),
    },
}


DEFAULT_METADATA = {
    "category": "Data Quality",
    "source_system": "Unknown",
    "business_impact": "May reduce confidence in reporting.",
    "recommendation": "Review and correct the source record.",
}


def get_rule_metadata(rule_name: str) -> dict:
    """Return business metadata for a rule."""

    return RULE_METADATA.get(
        rule_name,
        DEFAULT_METADATA,
    )