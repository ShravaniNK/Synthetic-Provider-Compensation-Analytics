from pathlib import Path
import numpy as np
import pandas as pd
from faker import Faker

# ============================================================
# 1. CONFIGURATION
# ============================================================

SEED = 42

rng = np.random.default_rng(SEED)
fake = Faker()
Faker.seed(SEED)

# Project root:
# provider-productivity-compensation-analytics/
ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

N_PROVIDERS = 80
N_PATIENTS = 2500

START_DATE = "2025-01-01"
END_DATE = "2026-12-31"

# ============================================================
# 2. SPECIALTY CONFIGURATION
# ============================================================

specialty_config = {
    "Primary Care": {
        "clinics": [
            "ClinicA",
            "Clinic B",
            "Clinic C",
            "Clinic D",
        ],  
        "salary_range": (190000, 250000),
        "monthly_wrvu_target_per_fte": 350,
    },

    "Cardiology": {
        "clinics": [
            "ClinicA",
            "Clinic B",
        ],
        "salary_range": (280000, 400000),
        "monthly_wrvu_target_per_fte": 450,
    },

    "Orthopedics": {
        "clinics": [
            "ClinicA",
            "Clinic B",
        ],
        "salary_range": (300000, 450000),
        "monthly_wrvu_target_per_fte": 475,
    },

    "Pediatrics": {
        "clinics": [
            "ClinicA",
            "Clinic B",
        ],
        "salary_range": (180000, 240000),
        "monthly_wrvu_target_per_fte": 300,
    },

    "General Surgery": {
        "clinics": [
            "ClinicA",
            "Clinic B",
        ],
        "salary_range": (300000, 450000),
        "monthly_wrvu_target_per_fte": 425,
    },

    "OBGYN": {
        "clinics": [
            "ClinicA",
            "Clinic B",
            "Clinic C",
        ],
        "salary_range": (240000, 350000),
        "monthly_wrvu_target_per_fte": 375,
    },

    "Dermatology": {
        "clinics": [
            "ClinicA",
            "Clinic B",
        ],
        "salary_range": (250000, 350000),
        "monthly_wrvu_target_per_fte": 325,
    },
}


# ============================================================
# 3. CPT / SERVICE MASTER DATA
# ============================================================
#
# IMPORTANT: These are synthetic educational values.

cpt_records = [
    # Primary Care
    [
        "99213",
        "Established Patient Visit - Low Complexity",
        "Primary Care",
        0.97,
        140,
        110,
    ],
    [
        "99214",
        "Established Patient Visit - Moderate Complexity",
        "Primary Care",
        1.50,
        185,
        145,
    ],
    [
        "99215",
        "Established Patient Visit - High Complexity",
        "Primary Care",
        2.11,
        240,
        190,
    ],
    [
        "99203",
        "New Patient Visit - Low Complexity",
        "Primary Care",
        1.60,
        200,
        160,
    ],
    [
        "99204",
        "New Patient Visit - Moderate Complexity",
        "Primary Care",
        2.60,
        275,
        220,
    ],
    [
        "99205",
        "New Patient Visit - High Complexity",
        "Primary Care",
        3.50,
        350,
        280,
    ],

    # Cardiology
    [
        "93000",
        "Electrocardiogram",
        "Cardiology",
        0.17,
        75,
        55,
    ],
    [
        "93306",
        "Echocardiography",
        "Cardiology",
        1.50,
        500,
        390,
    ],

    # Orthopedics
    [
        "20610",
        "Large Joint Injection",
        "Orthopedics",
        0.80,
        250,
        195,
    ],
    [
        "27447",
        "Total Knee Arthroplasty",
        "Orthopedics",
        20.00,
        4500,
        3500,
    ],

    # Pediatrics
    [
        "87880",
        "Rapid Strep Test",
        "Pediatrics",
        0.00,
        35,
        25,
    ],
    [
        "99213",
        "Established Patient Visit",
        "Pediatrics",
        0.97,
        120,
        85,
        ],
    [
        "99214",
        "Established Patient Visit",
        "Pediatrics",
        1.50,
        180,
        125
    ],
    [
        "99391",
        "Preventive Medicine - Infant",
        "Pediatrics",
        1.50,
        180,
        125
    ],
    [
        "99392",
        "Preventive Medicine - Early Childhood",
        "Pediatrics",
        1.50,
        180,
        125
        ],
    # Dermatology
    [
        "11102",
        "Skin Biopsy",
        "Dermatology",
        0.70,
        180,
        140,
    ],
    [
        "17000",
        "Destruction of Skin Lesion",
        "Dermatology",
        0.50,
        125,
        95,
    ],

    # General Surgery
    [
        "99243",
        "Surgical Consultation",
        "General Surgery",
        2.43,
        300,
        240,
    ],
    [
        "47562",
        "Laparoscopic Surgical Procedure",
        "General Surgery",
        11.00,
        2500,
        2000,
    ],

    # OBGYN
    [
        "59400",
        "Obstetric Delivery",
        "OBGYN",
        9.00,
        2200,
        1750,
    ],
    [
        "99213",
        "Established Patient Visit - Low Complexity",
        "OBGYN",
        0.97,
        140,
        110,
    ],
]

cpt_df = pd.DataFrame(
    cpt_records,
    columns=[
        "cpt_code",
        "service_name",
        "specialty",
        "wrvu",
        "charge_amount",
        "allowed_amount",
    ],
)

# A CPT code can appear in multiple specialties in this synthetic dataset.
# Therefore the combination of CPT + specialty is the unique key.
cpt_df = cpt_df.drop_duplicates(
    subset=["cpt_code", "specialty"]
).reset_index(drop=True)


# ============================================================
# 4. PAYER DISTRIBUTION
# ============================================================

payer_names = [
    "Commercial",
    "Medicare",
    "Medicaid",
    "Self-Pay",
]

payer_probabilities = [
    0.40,
    0.30,
    0.20,
    0.10,
]


# ============================================================
# 5. GENERATE PROVIDERS
# ============================================================

providers = []

specialties = list(specialty_config.keys())

for i in range(1, N_PROVIDERS + 1):

    specialty = rng.choice(specialties)

    config = specialty_config[specialty]

    clinic = rng.choice(config["clinics"])

    fte = rng.choice(
        [0.50, 0.75, 1.00],
        p=[0.10, 0.20, 0.70],
    )

    salary_low, salary_high = config["salary_range"]

    base_salary = rng.uniform(
        salary_low,
        salary_high,
    )

    # Round synthetic salary to nearest $1,000.
    base_salary = round(base_salary / 1000) * 1000

    providers.append(
        {
            "provider_id": f"P{i:04d}",
            "provider_name": f"Provider {i:03d}",
            "specialty": specialty,
            "clinic": clinic,
            "fte": fte,
            "base_salary": base_salary,
            "employment_type": (
                "Full-Time"
                if fte == 1.0
                else "Part-Time"
            ),
        }
    )

providers_df = pd.DataFrame(providers)


# ============================================================
# 6. GENERATE SYNTHETIC PATIENTS
# ============================================================

patients_df = pd.DataFrame(
    {
        "patient_id": [
            f"PAT{i:05d}"
            for i in range(1, N_PATIENTS + 1)
        ],

        "birth_year": rng.integers(
            1940,
            2016,
            N_PATIENTS,
        ),

        "gender": rng.choice(
            [
                "Female",
                "Male",
                "Other/Unknown",
            ],
            N_PATIENTS,
            p=[0.51, 0.47, 0.02],
        ),
    }
)


# ============================================================
# 7. GENERATE ENCOUNTER-LEVEL DATA
# ============================================================

dates = pd.date_range(
    START_DATE,
    END_DATE,
    freq="D",
)

encounters = []

encounter_counter = 1


for _, provider in providers_df.iterrows():

    provider_id = provider["provider_id"]
    specialty = provider["specialty"]
    clinic = provider["clinic"]
    fte = provider["fte"]

    # --------------------------------------------------------
    # Select services appropriate for specialty
    # --------------------------------------------------------

    if specialty == "Primary Care":

        eligible = cpt_df[
            cpt_df["specialty"] == "Primary Care"
        ].copy()

        service_weights = np.array(
            [0.25, 0.35, 0.12, 0.12, 0.10, 0.06]
        )

    elif specialty == "Cardiology":

        eligible = cpt_df[
            cpt_df["specialty"] == "Cardiology"
        ].copy()

        service_weights = np.array(
            [0.55, 0.45]
        )

    elif specialty == "Orthopedics":

        eligible = cpt_df[
            cpt_df["specialty"] == "Orthopedics"
        ].copy()

        service_weights = np.array(
            [0.70, 0.30]
        )

    elif specialty == "Pediatrics":

        eligible = cpt_df[
            cpt_df["specialty"] == "Pediatrics"
        ].copy()

        service_weights = np.array(
            #[1.0]
            [0.35, 0.25, 0.15, 0.15, 0.10]
        )

    elif specialty == "General Surgery":

        eligible = cpt_df[
            cpt_df["specialty"] == "General Surgery"
        ].copy()

        service_weights = np.array(
            [0.70, 0.30]
        )

    elif specialty == "OBGYN":

        eligible = cpt_df[
            cpt_df["specialty"] == "OBGYN"
        ].copy()

        service_weights = np.array(
            [0.70, 0.30]
        )

    elif specialty == "Dermatology":

        eligible = cpt_df[
            cpt_df["specialty"] == "Dermatology"
        ].copy()

        service_weights = np.array(
            [0.65, 0.35]
        )

    else:

        raise ValueError(
            f"Unsupported specialty: {specialty}"
        )

    service_weights = (
        service_weights /
        service_weights.sum()
    )

    # --------------------------------------------------------
    # Generate encounters by working day
    # --------------------------------------------------------

    # Average encounters per working day.
    # Adjusted by FTE.
    daily_mean = 15 * fte

    for date in dates:

        # No encounters on weekends.
        if date.weekday() >= 5:
            continue

        number_of_encounters = max(
            0,
            int(
                rng.poisson(
                    daily_mean
                )
            ),
        )

        for _ in range(number_of_encounters):
            # --------------------------------------------------------
            # Select a service safely
            # --------------------------------------------------------

            if eligible.empty:
                 raise ValueError(             
                     f"No eligible services found for specialty: {specialty}"
                )

            # Make sure weights are numeric and aligned with eligible rows.
            service_weights = np.asarray(
                service_weights,
                dtype=float
            )
            if len(service_weights) != len(eligible):
                raise ValueError(
                    f"Service weight mismatch for {specialty}: "
                    f"{len(eligible)} services but "
                    f"{len(service_weights)} weights."
                )
            
            # Normalize weights so they sum exactly to 1.
            weight_total = service_weights.sum()
            if weight_total <= 0:
                service_weights = np.ones(len(eligible)) / len(eligible)
            else:
                service_weights = service_weights / weight_total

            service_index = rng.choice(
                len(eligible),
                p=service_weights,
            )

            service = eligible.iloc[service_index]
           
            patient_index = rng.integers(
                0,
                len(patients_df),
            )

            patient = patients_df.iloc[
                patient_index
            ]

            # Small random variation in financial values.
            charge_amount = (
                service["charge_amount"]
                * rng.normal(
                    1.0,
                    0.05,
                )
            )

            allowed_amount = (
                service["allowed_amount"]
                * rng.normal(
                    1.0,
                    0.05,
                )
            )

            charge_amount = max(
                charge_amount,
                0,
            )

            allowed_amount = max(
                allowed_amount,
                0,
            )

            encounters.append(
                {
                    "encounter_id": (
                        f"E{encounter_counter:08d}"
                    ),

                    "date": date,

                    "provider_id": provider_id,

                    "patient_id": (
                        patient["patient_id"]
                    ),

                    "clinic": clinic,

                    "specialty": specialty,

                    "payer": rng.choice(
                        payer_names,
                        p=payer_probabilities,
                    ),

                    "cpt_code": service["cpt_code"],

                    "units": 1,

                    "wrvu": round(
                        float(service["wrvu"]),
                        2,
                    ),

                    "charges": round(
                        charge_amount,
                        2,
                    ),

                    "allowed_amount": round(
                        allowed_amount,
                        2,
                    ),
                }
            )

            encounter_counter += 1


encounters_df = pd.DataFrame(encounters)


# ============================================================
# 8. ADD MONTH FIELD
# ============================================================

encounters_df["date"] = pd.to_datetime(
    encounters_df["date"]
)

encounters_df["month"] = (
    encounters_df["date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)


# ============================================================
# 9. CREATE MONTHLY PROVIDER PRODUCTIVITY
# ============================================================

monthly_df = (
    encounters_df
    .groupby(
        [
            "month",
            "provider_id",
            "clinic",
            "specialty",
        ],
        as_index=False,
    )
    .agg(
        encounters=(
            "encounter_id",
            "count",
        ),

        wrvus=(
            "wrvu",
            "sum",
        ),

        revenue=(
            "allowed_amount",
            "sum",
        ),
    )
)


# Add provider attributes.
monthly_df = monthly_df.merge(
    providers_df[
        [
            "provider_id",
            "fte",
            "base_salary",
        ]
    ],
    on="provider_id",
    how="left",
)


# ============================================================
# 10. PRODUCTIVITY METRICS
# ============================================================

monthly_df["wrvus_per_fte"] = (
    monthly_df["wrvus"]
    / monthly_df["fte"]
)

monthly_df["revenue_per_wrvu"] = (
    monthly_df["revenue"]
    / monthly_df["wrvus"].replace(
        0,
        np.nan,
    )
)


# ============================================================
# 11. SYNTHETIC QUALITY METRICS
# ============================================================

monthly_df["quality_score"] = np.clip(
    rng.normal(
        84,
        8,
        len(monthly_df),
    ),
    55,
    99,
).round(1)


monthly_df["patient_satisfaction"] = np.clip(
    rng.normal(
        87,
        6,
        len(monthly_df),
    ),
    60,
    99,
).round(1)


monthly_df["preventive_care_rate"] = np.clip(
    rng.normal(
        78,
        10,
        len(monthly_df),
    ),
    40,
    99,
).round(1)


monthly_df["follow_up_compliance"] = np.clip(
    rng.normal(
        82,
        9,
        len(monthly_df),
    ),
    45,
    99,
).round(1)


# ============================================================
# 12. SYNTHETIC COMPENSATION PLAN
# ============================================================

compensation_plan = []

for specialty, config in specialty_config.items():

    compensation_plan.append(
        {
            "specialty": specialty,

            "monthly_wrvu_target_per_fte": (
                config[
                    "monthly_wrvu_target_per_fte"
                ]
            ),

            # Synthetic assumption.
            "threshold_pct": 0.90,

            # Synthetic assumption.
            "dollars_per_excess_wrvu": 50.00,

            "quality_multiplier_low": 0.75,

            "quality_multiplier_mid": 0.90,

            "quality_multiplier_standard": 1.00,

            "quality_multiplier_high": 1.10,
        }
    )


compensation_plan_df = pd.DataFrame(
    compensation_plan
)


# ============================================================
# 13. CALCULATE SYNTHETIC COMPENSATION
# ============================================================

monthly_df = monthly_df.merge(
    compensation_plan_df,
    on="specialty",
    how="left",
)


# Target based on specialty and FTE.
monthly_df["monthly_target_wrvus"] = (
    monthly_df[
        "monthly_wrvu_target_per_fte"
    ]
    * monthly_df["fte"]
)


# Incentive threshold.
monthly_df["incentive_threshold_wrvus"] = (
    monthly_df[
        "monthly_target_wrvus"
    ]
    * monthly_df["threshold_pct"]
)


# Difference from target.
monthly_df["productivity_variance_wrvus"] = (
    monthly_df["wrvus"]
    - monthly_df["monthly_target_wrvus"]
)


# wRVUs eligible for incentive.
monthly_df["excess_wrvus"] = np.maximum(
    monthly_df["wrvus"]
    - monthly_df[
        "incentive_threshold_wrvus"
    ],
    0,
)


# Gross incentive.
monthly_df["gross_incentive"] = (
    monthly_df["excess_wrvus"]
    * monthly_df[
        "dollars_per_excess_wrvu"
    ]
)


# ============================================================
# 14. QUALITY MULTIPLIER
# ============================================================

def calculate_quality_multiplier(
    quality_score,
):
    """
    Synthetic educational assumption.

    >= 90 -> 1.10
    >= 80 -> 1.00
    >= 70 -> 0.90
    < 70  -> 0.75
    """

    if quality_score >= 90:
        return 1.10

    if quality_score >= 80:
        return 1.00

    if quality_score >= 70:
        return 0.90

    return 0.75


monthly_df["quality_multiplier"] = (
    monthly_df["quality_score"]
    .apply(
        calculate_quality_multiplier
    )
)


# ============================================================
# 15. FINAL PRODUCTIVITY AND COMPENSATION METRICS
# ============================================================

monthly_df["productivity_pct"] = (
    monthly_df["wrvus"]
    / monthly_df[
        "monthly_target_wrvus"
    ]
)


monthly_df["final_incentive"] = (
    monthly_df["gross_incentive"]
    * monthly_df["quality_multiplier"]
)


monthly_df[
    "estimated_total_compensation"
] = (
    monthly_df["base_salary"] / 12
    + monthly_df["final_incentive"]
)


# ============================================================
# 16. ADD STATUS FLAGS
# ============================================================

monthly_df["productivity_status"] = np.select(
    [
        monthly_df["productivity_pct"] >= 1.00,

        monthly_df["productivity_pct"] >= 0.90,

        monthly_df["productivity_pct"] < 0.90,
    ],

    [
        "Above Target",
        "At / Near Target",
        "Below Threshold",
    ],

    default="Unknown",
)


monthly_df["incentive_status"] = np.where(
    monthly_df["wrvus"]
    >= monthly_df[
        "incentive_threshold_wrvus"
    ],

    "Eligible",

    "Below Threshold",
)


# ============================================================
# 17. SELECT FINAL COLUMNS
# ============================================================

monthly_columns = [
    "month",
    "provider_id",
    "clinic",
    "specialty",
    "fte",
    "base_salary",
    "encounters",
    "wrvus",
    "revenue",
    "wrvus_per_fte",
    "revenue_per_wrvu",
    "quality_score",
    "patient_satisfaction",
    "preventive_care_rate",
    "follow_up_compliance",
    "monthly_target_wrvus",
    "incentive_threshold_wrvus",
    "productivity_variance_wrvus",
    "excess_wrvus",
    "gross_incentive",
    "quality_multiplier",
    "productivity_pct",
    "final_incentive",
    "estimated_total_compensation",
    "productivity_status",
    "incentive_status",
]

monthly_df = monthly_df[
    monthly_columns
]


# ============================================================
# 18. SAVE CSV FILES
# ============================================================

providers_path = (
    RAW_DIR / "providers.csv"
)

patients_path = (
    RAW_DIR / "patients.csv"
)

cpt_path = (
    RAW_DIR / "dim_cpt.csv"
)

encounters_path = (
    RAW_DIR / "fact_encounter.csv"
)

monthly_path = (
    RAW_DIR / "fact_provider_monthly.csv"
)

compensation_path = (
    RAW_DIR / "compensation_plan.csv"
)


providers_df.to_csv(
    providers_path,
    index=False,
)

patients_df.to_csv(
    patients_path,
    index=False,
)

cpt_df.to_csv(
    cpt_path,
    index=False,
)

encounters_df.to_csv(
    encounters_path,
    index=False,
)

monthly_df.to_csv(
    monthly_path,
    index=False,
)

compensation_plan_df.to_csv(
    compensation_path,
    index=False,
)


# ============================================================
# 19. BASIC VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("SYNTHETIC DATA GENERATION COMPLETE")
print("=" * 60)

print(
    f"\nProviders:          {len(providers_df):,}"
)

print(
    f"Patients:           {len(patients_df):,}"
)

print(
    f"CPT/service rows:   {len(cpt_df):,}"
)

print(
    f"Encounters:         {len(encounters_df):,}"
)

print(
    f"Provider-months:    {len(monthly_df):,}"
)


print("\nFiles created:")

for file_path in [
    providers_path,
    patients_path,
    cpt_path,
    encounters_path,
    monthly_path,
    compensation_path,
]:

    print(
        f"  {file_path.relative_to(ROOT)}"
    )


print("\nBasic checks:")

print(
    "  Unique provider IDs:",
    providers_df["provider_id"].is_unique,
)

print(
    "  Unique encounter IDs:",
    encounters_df[
        "encounter_id"
    ].is_unique,
)

print(
    "  Missing provider IDs:",
    encounters_df[
        "provider_id"
    ].isna().sum(),
)

print(
    "  Missing CPT codes:",
    encounters_df[
        "cpt_code"
    ].isna().sum(),
)

print(
    "  Invalid quality scores:",
    (
        (
            monthly_df["quality_score"] < 0
        )
        |
        (
            monthly_df["quality_score"] > 100
        )
    ).sum(),
)


# ============================================================
# 20. SAMPLE OUTPUT
# ============================================================

print("\nProvider sample:")
print(
    providers_df.head(5).to_string(
        index=False
    )
)

print("\nEncounter sample:")
print(
    encounters_df.head(5).to_string(
        index=False
    )
)

print("\nMonthly productivity sample:")
print(
    monthly_df.head(5).to_string(
        index=False
    )
)

print("\nDone.")