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
            "total_wealth": {"2023": 500_000},
            "consumption": {"2023": 60_000},
            "full_rate_vat_consumption": {"2023": 60_000 * 0.45},
            "region": {"2023": "YORKSHIRE"},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        }
    },
}

ELDERLY_MAN_WITH_CARER = {
    "people": {
        "you": {
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
            "members": ["you"],
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
            "members": ["you", "carer"],
            "BRMA": {"2023": "NORTH_DEVON"},
            "local_authority": {"2023": "NORTH_DEVON"},
            "region": {"2023": "SOUTH_WEST"},
            "tenure_type": {"2023": "RENT_FROM_COUNCIL"},
            "consumption": {"2023": 15_000},
            "full_rate_vat_consumption": {"2023": 15_000 * 0.65},
            "total_wealth": {"2023": 10_000},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
            "winter_fuel_allowance": {"2023": 300},
        }
    },
}

SINGLE_WOMAN_LONDON_HOUSE_SHARE = {
    "people": {
        "you": {
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
            "members": ["you"],
            "benunit_rent": {
                # ~60% of income
                "2023": 18_000
                * 0.6,
            },
        },
    },
    "households": {
        "household": {
            "members": ["you"],
            "BRMA": {"2023": "INNER_NORTH_LONDON"},
            "local_authority": {"2023": "HACKNEY"},
            "region": {"2023": "LONDON"},
            "consumption": {"2023": 20_000},
            "full_rate_vat_consumption": {"2023": 20_000 * 0.6},
            "total_wealth": {"2023": 20_000},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        },
    },
}

SINGLE_MOTHER_WITH_TWO_CHILDREN = {
    "people": {
        "you": {
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
            "members": ["you", "child_1", "child_2"],
            "benunit_rent": {
                "2023": 7_000,
            },
        },
    },
    "households": {
        "household": {
            "members": ["you", "child_1", "child_2"],
            "BRMA": {"2023": "CENTRAL_GREATER_MANCHESTER"},
            "local_authority": {"2023": "MANCHESTER"},
            "region": {"2023": "NORTH_WEST"},
            "consumption": {"2023": 20_000},
            "full_rate_vat_consumption": {"2023": 20_000 * 0.6},
            "total_wealth": {"2023": 100_000},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        },
    },
}

SINGLE_ADULT_20K = {
    "people": {
        "you": {"age": {"2023": "24"}, "employment_income": {"2023": "20000"}}
    },
    "benunits": {"your immediate family": {"members": ["you"]}},
    "households": {
        "household": {
            "members": ["you"],
            "consumption": {"2023": 14_000},
            "full_rate_vat_consumption": {"2023": 14_000 * 0.6},
            "total_wealth": {"2023": 10_000},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        }
    },
}
MARRIED_COUPLE_TWO_KIDS_BOTH_30K = {
    "people": {
        "you": {"employment_income": {"2023": "30000"}},
        "your partner": {"employment_income": {"2023": "40000"}},
        "your first child": {"age": {"2023": 10}},
        "your second child": {"age": {"2023": 8}},
    },
    "benunits": {
        "your immediate family": {
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
            "consumption": {"2023": 50000},
            "full_rate_vat_consumption": {"2023": 50000 * 0.6},
            "total_wealth": {"2023": 150_000},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        }
    },
}
SINGLE_PENSIONER_25K_PENSION_INCOME = {
    "people": {
        "you": {"age": {"2023": "70"}, "pension_income": {"2023": "25000"}}
    },
    "benunits": {"your immediate family": {"members": ["you"]}},
    "households": {
        "household": {
            "members": ["you"],
            "consumption": {"2023": 13_000},
            "full_rate_vat_consumption": {"2023": 13_000 * 0.6},
            "total_wealth": {"2023": 240_000},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        }
    },
}
MARRIED_PENSIONER_COUPLE_80K_PENSION_INCOME = {
    "people": {
        "you": {"age": {"2023": "70"}, "pension_income": {"2023": "40000"}},
        "your partner": {
            "age": {"2023": "65"},
            "pension_income": {"2023": "40000"},
        },
    },
    "benunits": {
        "your immediate family": {
            "members": ["you", "your partner"],
            "is_married": {"2023": True},
        }
    },
    "households": {
        "household": {
            "members": ["you", "your partner"],
            "consumption": {"2023": 60_000},
            "full_rate_vat_consumption": {"2023": 23_000 * 0.4},
            "total_wealth": {"2023": 1_200_000},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        }
    },
}
MARRIED_COUPLE_1_KID_1_EARNER = {
    "people": {
        "you": {"employment_income": {"2023": "35000"}},
        "your partner": {},
        "your first child": {"age": {"2023": 10}},
    },
    "benunits": {
        "your immediate family": {
            "members": ["you", "your partner", "your first child"],
            "is_married": {"2023": True},
        }
    },
    "households": {
        "household": {
            "members": ["you", "your partner", "your first child"],
            "consumption": {"2023": 30_000},
            "full_rate_vat_consumption": {"2023": 30_000 * 0.7},
            "total_wealth": {"2023": 240_000},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        }
    },
}
SINGLE_ADULT_HIGH_INCOME = {
    "people": {
        "you": {"age": {"2023": "55"}, "employment_income": {"2023": "60000"}}
    },
    "benunits": {"your immediate family": {"members": ["you"]}},
    "households": {
        "household": {
            "members": ["you"],
            "consumption": {"2023": 40_000},
            "full_rate_vat_consumption": {"2023": 40_000 * 0.4},
            "total_wealth": {"2023": 1_100_000},
            "household_net_income": {"2023": None},
            "household_benefits": {"2023": None},
            "household_tax": {"2023": None},
        }
    },
}
