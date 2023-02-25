HIGH_EARNING_NUCLEAR_FAMILY = {
    "people": {
        "you": {"age": {"2023": 39}, "employment_income": {"2023": 60_000}},
        "your partner": {
            "age": {"2023": 37},
            "employment_income": {"2023": 40_000},
        },
        "your first child": {"age": {"2023": 4}},
        "your second child": {"age": {"2023": 2}},
    },
    "benunits": {
        "benunit": {
            "members": [
                "you",
                "your partner",
                "your first child",
                "your second child",
            ],
            "is_married": {"2023": True},
        }
    },
    "households": {
        "household": {
            "members": [
                "you",
                "your partner",
                "your first child",
                "your second child",
            ],
            "BRMA": {"2023": "YORK"},
            "local_authority": {"2023": "YORK"},
            "main_residence_value": {"2023": 400_000},
            "region": {"2023": "YORKSHIRE"},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        }
    },
}

ELDERLY_MAN_WITH_CARER = {
    "people": {
        "elderly_man": {
            "age": {
                "2023": 74,
            },
            "state_pension": {
                "2023": 185.15 * 52,
            },
            "is_disabled_for_benefits": {
                "2023": True,
            },
        },
        "carer": {
            "age": {
                "2023": 50,
            },
            "is_carer_for_benefits": {
                "2023": True,
            },
        },
    },
    "benunits": {
        "benunit_1": {
            "members": ["elderly_man"],
            "benunit_rent": {
                "2023": 4_500,
            },
        },
        "benunit_2": {
            "members": ["carer"],
        },
    },
    "households": {
        "household": {
            "members": ["elderly_man", "carer"],
            "BRMA": {"2023": "NORTH_DEVON"},
            "local_authority": {"2023": "NORTH_DEVON"},
            "region": {"2023": "SOUTH_WEST"},
            "tenure_type": {"2023": "RENT_FROM_COUNCIL"},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        }
    },
}

SINGLE_WOMAN_LONDON_HOUSE_SHARE = {
    "people": {
        "single_woman": {
            "age": {
                "2023": 27,
            },
            "employment_income": {
                "2023": 30_000,
            },
        }
    },
    "benunits": {
        "benunit": {
            "members": ["single_woman"],
            "benunit_rent": {
                # ~60% of income
                "2023": 18_000
                * 0.6,
            },
        },
    },
    "households": {
        "household": {
            "members": ["single_woman"],
            "BRMA": {"2023": "INNER_NORTH_LONDON"},
            "local_authority": {"2023": "HACKNEY"},
            "region": {"2023": "LONDON"},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        },
    },
}

SINGLE_MOTHER_WITH_TWO_CHILDREN = {
    "people": {
        "single_mother": {
            "age": {
                "2023": 40,
            },
            "employment_income": {
                "2023": 35_000,
            },
        },
        "child_1": {
            "age": {
                "2023": 14,
            },
        },
        "child_2": {
            "age": {
                "2023": 4,
            },
        },
    },
    "benunits": {
        "benunit": {
            "members": ["single_mother", "child_1", "child_2"],
            "benunit_rent": {
                "2023": 7_000,
            },
        },
    },
    "households": {
        "household": {
            "members": ["single_mother", "child_1", "child_2"],
            "BRMA": {"2023": "CENTRAL_GREATER_MANCHESTER"},
            "local_authority": {"2023": "MANCHESTER"},
            "region": {"2023": "NORTH_WEST"},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        },
    },
}
