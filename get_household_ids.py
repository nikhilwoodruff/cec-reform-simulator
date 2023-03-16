from example_households import (
    HIGH_EARNING_NUCLEAR_FAMILY,
    ELDERLY_MAN_WITH_CARER,
    SINGLE_WOMAN_LONDON_HOUSE_SHARE,
    SINGLE_MOTHER_WITH_TWO_CHILDREN,
    SINGLE_ADULT_20K,
    MARRIED_COUPLE_TWO_KIDS_BOTH_30K,
    SINGLE_PENSIONER_25K_PENSION_INCOME,
    MARRIED_PENSIONER_COUPLE_80K_PENSION_INCOME,
    MARRIED_COUPLE_1_KID_1_EARNER,
    SINGLE_ADULT_HIGH_INCOME,
)
from policyengine_uk.system import system
from policyengine_core.variables import Variable
from policyengine_core.enums import Enum
import requests

variables = system.variables
entities = system.entities_by_singular()


# Translate the above to Python

def add_yearly_variables(situation, variables, entities):
    for variable in variables.values():
        variable: Variable
        if variable.definition_period == "year":
            entity_plural = entities[variable.entity.key].plural
            if entity_plural in situation:
                possible_entities = situation[entity_plural].keys()
                for entity_name in possible_entities:
                    if variable.name not in situation[entity_plural][entity_name]:
                        if variable.is_input_variable() and variable.value_type is not Enum:
                            situation[entity_plural][entity_name][variable.name] = {
                            2023: variable.default_value
                            }
                        else:
                            situation[entity_plural][entity_name][variable.name] = {
                            2023: None
                            }
    return situation

SITUATIONS = [
    HIGH_EARNING_NUCLEAR_FAMILY,
    ELDERLY_MAN_WITH_CARER,
    SINGLE_WOMAN_LONDON_HOUSE_SHARE,
    SINGLE_MOTHER_WITH_TWO_CHILDREN,
    SINGLE_ADULT_20K,
    MARRIED_COUPLE_TWO_KIDS_BOTH_30K,
    SINGLE_PENSIONER_25K_PENSION_INCOME,
    MARRIED_PENSIONER_COUPLE_80K_PENSION_INCOME,
    MARRIED_COUPLE_1_KID_1_EARNER,
    SINGLE_ADULT_HIGH_INCOME,
]

FULL_SITUATIONS = [add_yearly_variables(situation, variables, entities) for situation in SITUATIONS]

def get_household_id(situation):
    # Send a POST request to https://api.policyengine.org/household with {data: situation}
    # Then get the json => json.result.household_id

    response = requests.post("https://api.policyengine.org/uk/household", json={"data": situation})
    return response.json()["result"]["household_id"]

HOUSEHOLD_IDS = [get_household_id(situation) for situation in FULL_SITUATIONS]
print(HOUSEHOLD_IDS)