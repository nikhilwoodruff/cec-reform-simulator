import streamlit as st
import requests
import time
import plotly.express as px
import datetime
import humanize
import dateutil
import pandas as pd
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

API = "https://api.policyengine.org/uk"


def get_metadata():
    return requests.get(API + "/metadata").json()["result"]


hide_footer_style = """
<style>
header {
    display: none !important;
}
footer {
    display: none !important;
}
section > div.block-container {
    padding-top: 0px !important;
    padding-bottom: 0px !important;
}
h1,
h2,
h3,
h4,
h5,
h6,
p,
span,
div {
  font-family: "Roboto", sans-serif !important;
  font-weight: 500;
}
[data-baseweb="slider"] {
    padding-left: 10px !important;
}
#MainMenu {
    visibility: hidden;
}
footer {
    visibility: hidden;
}
.modebar{
      display: none !important;
}
</style>
"""
st.write(hide_footer_style, unsafe_allow_html=True)

metadata = get_metadata()
variables = metadata["variables"]

WHITE = "#FFF"
BLUE = "#2C6496"
GRAY = "#BDBDBD"
MEDIUM_DARK_GRAY = "#D2D2D2"
DARK_GRAY = "#616161"
LIGHT_GRAY = "#F2F2F2"
LIGHT_GREEN = "#C5E1A5"
DARK_GREEN = "#558B2F"
BLACK = "#000"

if "history" not in st.session_state:
    st.session_state.history = []

st.title("Citizens' Economic Council: reform simulator")
st.markdown(
    "This is a prototype of a tool that will allow you to explore the impact of tax-benefit reforms on your household. Enter your household details, then build a reform to see how it would affect you."
)

with st.expander("Enter your household details"):
    brma_label = st.selectbox(
        "What Broad Rental Market Area do you live in?",
        [x["label"] for x in variables["BRMA"]["possibleValues"]],
    )
    brma = [
        x["value"]
        for x in variables["BRMA"]["possibleValues"]
        if x["label"] == brma_label
    ][0]
    marital_status = st.selectbox(
        "What is your marital status?", ["Single", "Married"]
    )

    people = {}
    if marital_status == "Single":
        age = st.slider(
            "How old are you?",
            step=1,
            min_value=18,
            max_value=100,
            key="single_age",
        )
        if age < 65:
            employment_income = st.slider(
                "What is your annual employment income?",
                min_value=0,
                max_value=100_000,
                step=1000,
                key="single_employment_income",
                format="£%d",
            )
            state_pension = 0
            pension_income = 0
        else:
            employment_income = 0
            state_pension = st.slider(
                "What is your annual state pension?",
                min_value=0,
                max_value=100_000,
                step=100,
                key="single_state_pension",
                format="£%d",
            )
            pension_income = st.slider(
                "What is your annual pension income?",
                min_value=0,
                max_value=100_000,
                step=100,
                key="single_pension_income",
                format="£%d",
            )
        people["adult_1"] = {
            "age": {2023: age},
            "employment_income": {2023: employment_income},
            "state_pension": {2023: state_pension},
            "pension_income": {2023: pension_income},
        }
    else:
        age = st.slider(
            "How old are you?",
            step=1,
            min_value=18,
            max_value=100,
            key="single_age",
        )
        if age < 65:
            employment_income = st.slider(
                "What is your annual employment income?",
                min_value=0,
                max_value=100_000,
                step=1000,
                key="married_employment_income",
                format="£%d",
            )
            state_pension = 0
            pension_income = 0
        else:
            employment_income = 0
            state_pension = st.slider(
                "What is your annual state pension?",
                min_value=0,
                max_value=100_000,
                step=100,
                key="married_state_pension",
                format="£%d",
            )
            pension_income = st.slider(
                "What is your annual pension income?",
                min_value=0,
                max_value=100_000,
                step=100,
                key="married_pension_income",
                format="£%d",
            )

        people["adult_1"] = {
            "age": {2023: age},
            "employment_income": {2023: employment_income},
            "state_pension": {2023: state_pension},
            "pension_income": {2023: pension_income},
        }

        partner_age = st.slider(
            "How old is your partner?",
            step=1,
            min_value=18,
            max_value=100,
            value=people["adult_1"]["age"][2023],
            key="married_partner_age",
        )
        if partner_age < 65:
            partner_employment_income = st.slider(
                "What is your partner's annual employment income?",
                min_value=0,
                max_value=100_000,
                step=1000,
                key="married_partner_employment_income",
                format="£%d",
            )
            partner_state_pension = 0
            partner_pension_income = 0
        else:
            partner_employment_income = 0
            partner_state_pension = st.slider(
                "What is your partner's annual state pension?",
                min_value=0,
                max_value=100_000,
                step=100,
                key="married_partner_state_pension",
                format="£%d",
            )
            partner_pension_income = st.slider(
                "What is your partner's annual pension income?",
                min_value=0,
                max_value=100_000,
                step=100,
                key="married_partner_pension_income",
                format="£%d",
            )
        people["adult_2"] = {
            "age": {2023: age},
            "employment_income": {2023: partner_employment_income},
            "state_pension": {2023: partner_state_pension},
            "pension_income": {2023: partner_pension_income},
        }

    children = st.number_input(
        "How many children live in your household?", step=1
    )

    for i in range(children):
        age = st.slider(
            f"How old is child {i+1}?",
            step=1,
            min_value=0,
            max_value=18,
            value=10,
        )
        people[f"child_{i+1}"] = {
            "age": {2023: age},
        }

    full_rate_consumption = (
        st.slider(
            f"How much do you spend per year?",
            min_value=0,
            max_value=100_000,
            step=100,
            key="full_rate_consumption",
            format="£%d",
        )
        * 0.5
    )

    total_wealth = st.slider(
        f"How much wealth do you have?",
        min_value=0,
        max_value=10_000_000,
        step=1000,
        key="total_wealth",
        format="£%d",
    )
    main_residence_value = st.slider(
        f"How much is your (owned) main residence worth?",
        min_value=0,
        max_value=2_000_000,
        step=1000,
        key="main_residence_value",
        format="£%d",
    )

    situation = {
        "people": people,
        "benunits": {
            "benunit": {
                "members": list(people.keys()),
            }
        },
        "households": {
            "household": {
                "members": list(people.keys()),
                "BRMA": {2023: brma},
                "full_rate_vat_consumption": {2023: full_rate_consumption},
                "total_wealth": {2023: total_wealth},
                "main_residence_value": {2023: main_residence_value},
                "household_net_income": {2023: None},
                "household_benefits": {2023: None},
                "household_tax": {2023: None},
            },
        },
    }


def invert_dict(d):
    return {v: k for k, v in d.items()}


with st.expander("Select a tax-benefit reform"):
    st.write("Should the government...")
    basic_rate_map = {
        "lower to 18%": 0.18,
        "lower to 19%": 0.19,
        "keep the same": 0.2,
        "raise to 21%": 0.21,
        "raise to 22%": 0.22,
    }
    basic_rate = st.select_slider(
        "change the basic rate of income tax?",
        options=basic_rate_map.keys(),
        value="keep the same",
    )
    basic_rate = basic_rate_map[basic_rate]
    higher_rate_map = {
        "cut both by 5p": 0.35,
        "cut the higher rate by 5p": 0.35,
        "keep the same": 0.4,
        "raise the additional rate by 5p": 0.44,
        "raise the higher/additional rates by 5p": 0.45,
    }
    progressivity = st.select_slider(
        "change the higher and additional rates?",
        options=higher_rate_map.keys(),
        value="keep the same",
    )
    higher_rate = higher_rate_map[progressivity]
    additional_rate_map = {
        "cut both by 5p": 0.4,
        "cut the higher rate by 5p": 0.45,
        "keep the same": 0.45,
        "raise the additional rate by 5p": 0.5,
        "raise the higher/additional rates by 5p": 0.5,
    }
    additional_rate = additional_rate_map[progressivity]
    vat_map = {
        "lower to 15%": 0.15,
        "lower to 17.5%": 0.175,
        "keep the same": 0.2,
        "raise to 22.5%": 0.225,
        "raise to 25%": 0.25,
    }
    vat = st.select_slider(
        "change the VAT rate?",
        options=vat_map.keys(),
        value="keep the same",
    )
    vat = vat_map[vat]
    wealth_tax_map = {
        "no": (0, 0),
        "1% over £500k": (0.01, 500_000),
        "1% over £1m": (0.01, 1_000_000),
        "2% over £500k": (0.02, 500_000),
        "2% over £1m": (0.02, 1_000_000),
    }
    wealth_tax = st.select_slider(
        "introduce a wealth tax?",
        options=wealth_tax_map.keys(),
        value="no",
    )
    wealth_tax = wealth_tax_map[wealth_tax]
    benefits_map = {
        "decrease by 10%": -0.1,
        "decrease by 5%": -0.05,
        "no": 0,
        "increase by 5%": 0.05,
        "increase by 10%": 0.1,
    }
    benefits = st.select_slider(
        "change benefits?",
        options=[
            "decrease by 10%",
            "decrease by 5%",
            "no",
            "increase by 5%",
            "increase by 10%",
        ],
        value="no",
    )
    benefits = benefits_map[benefits]
    state_pension_map = {
        "decrease by 5%": -0.05,
        "decrease by 1%": -0.01,
        "no": 0,
        "increase by 1%": 0.01,
        "increase by 5%": 0.05,
    }
    state_pension = st.select_slider(
        "change the state pension?",
        options=[
            "decrease by 5%",
            "decrease by 1%",
            "no",
            "increase by 1%",
            "increase by 5%",
        ],
        value="no",
    )
    state_pension = state_pension_map[state_pension]
    ebr_map = {
        "no": 0,
        "£100": 100,
        "£200": 200,
        "£300": 300,
        "£400": 400,
    }
    ebr = st.select_slider(
        "discount energy bills by a flat amount, similar to the 2022 Energy Bills Credit?",
        options=["no", "£100", "£200", "£300", "£400"],
        value="no",
    )
    ebr = ebr_map[ebr]
    ubi_map = {"no": 0, "£10 per week": 10, "£30 per week": 30}
    ubi = st.select_slider(
        "introduce a universal basic income?",
        options=["no", "£10 per week", "£30 per week"],
        value="no",
    )
    ubi = ubi_map[ubi]

    reform = {
        "gov.hmrc.income_tax.rates.uk[0].rate": {
            "2023-01-01.2024-01-01": basic_rate
        },
        "gov.hmrc.income_tax.rates.uk[1].rate": {
            "2023-01-01.2024-01-01": higher_rate
        },
        "gov.hmrc.income_tax.rates.uk[2].rate": {
            "2023-01-01.2024-01-01": additional_rate
        },
        "gov.contrib.cec.non_primary_residence_wealth_tax[0].rate": {
            "2023-01-01.2024-01-01": wealth_tax[0]
        },
        "gov.contrib.cec.non_primary_residence_wealth_tax[0].threshold": {
            "2023-01-01.2024-01-01": wealth_tax[1]
        },
        "gov.contrib.ubi_center.basic_income.amount.flat": {
            "2023-01-01.2024-01-01": ubi
        },
        "gov.contrib.benefit_uprating.non_sp": {
            "2023-01-01.2024-01-01": benefits
        },
        "gov.contrib.cec.state_pension_increase": {
            "2023-01-01.2024-01-01": state_pension
        },
        "gov.treasury.energy_bills_rebate.energy_bills_credit": {
            "2023-01-01.2024-01-01": ebr
        },
        "gov.hmrc.vat.standard_rate": {"2023-01-01.2024-01-01": vat},
    }

    reform = {
        "data": reform,
    }

    reform_details = {
        "Should the government change the basic rate of income tax?": invert_dict(
            basic_rate_map
        )[
            basic_rate
        ],
        "Should the government change the higher and additional rates?": invert_dict(
            higher_rate_map
        )[
            higher_rate
        ],
        "Should the government change the VAT rate?": invert_dict(vat_map)[
            vat
        ],
        "Should the government introduce a wealth tax?": invert_dict(
            wealth_tax_map
        )[wealth_tax],
        "Should the government change benefits?": invert_dict(benefits_map)[
            benefits
        ],
        "Should the government change the state pension?": invert_dict(
            state_pension_map
        )[state_pension],
        "Should the government introduce a universal basic income?": invert_dict(
            ubi_map
        )[
            ubi
        ],
    }


def get_household_impact(household, reform):
    with st.spinner("Computing the impact on your household..."):
        baseline = requests.post(
            API + "/calculate",
            json={
                "household": household,
            },
        ).json()["result"]
        reformed = requests.post(
            API + "/calculate",
            json={
                "household": household,
                "policy": reform,
            },
        ).json()["result"]
        return baseline, reformed


st.write("## Your household's impact")
baseline, reformed = get_household_impact(situation, reform["data"])

baseline_net_income = baseline["households"]["household"][
    "household_net_income"
]["2023"]
reform_net_income = reformed["households"]["household"][
    "household_net_income"
]["2023"]

baseline_benefits = baseline["households"]["household"]["household_benefits"][
    "2023"
]
reform_benefits = reformed["households"]["household"]["household_benefits"][
    "2023"
]

baseline_tax = baseline["households"]["household"]["household_tax"]["2023"]
reform_tax = reformed["households"]["household"]["household_tax"]["2023"]

if reform_net_income > baseline_net_income:
    st.success(
        f"Your household would be £{reform_net_income - baseline_net_income:,.0f} better off under these reforms."
    )
elif reform_net_income < baseline_net_income:
    st.error(
        f"Your household would be £{baseline_net_income - reform_net_income:,.0f} worse off under these reforms."
    )
else:
    st.warning(
        f"Your household would be no better or worse off under these reforms."
    )


def get_colour(x, y):
    if y > x:
        return "normal"
    elif y == x:
        return "off"
    else:
        return "inverse"


col1, col2, col3 = st.columns(3)
col1.metric(
    "Net income",
    f"£{reform_net_income:,.0f}",
    int(reform_net_income - baseline_net_income),
)
col2.metric(
    "Benefits",
    f"£{reform_benefits:,.0f}",
    int(reform_benefits - baseline_benefits),
)
col3.metric("Tax", f"£{reform_tax:,.0f}", int(reform_tax - baseline_tax))

st.session_state["history"].append(
    {
        "timestamp": datetime.datetime.now().isoformat(),
        "net_income_change": int(reform_net_income - baseline_net_income),
        "reform_details": reform_details,
    }
)


@st.cache_resource(show_spinner=False)
def get_economic_impact(reform):
    with st.spinner("Computing the economic impact..."):
        policy_id = requests.post(API + "/policy", json=reform).json()[
            "result"
        ]["policy_id"]
        impact = requests.get(
            API + f"/economy/{policy_id}/over/1?region=uk&time_period=2023"
        ).json()
        while impact["status"] == "computing":
            time.sleep(2)
            impact = requests.get(
                API + f"/economy/{policy_id}/over/1?region=uk&time_period=2023"
            ).json()
        return impact["result"]


st.subheader("Impacts on example households")

with st.expander("See the impact on 10 example households"):
    households = {
        "High-earning couple with two children": HIGH_EARNING_NUCLEAR_FAMILY,
        "Elderly man with carer son": ELDERLY_MAN_WITH_CARER,
        "Single woman in London": SINGLE_WOMAN_LONDON_HOUSE_SHARE,
        "Single mother with two children": SINGLE_MOTHER_WITH_TWO_CHILDREN,
        "Single adult on £20k": SINGLE_ADULT_20K,
        "Married couple with two kids": MARRIED_COUPLE_TWO_KIDS_BOTH_30K,
        "Single pensioner on £25k pension income": SINGLE_PENSIONER_25K_PENSION_INCOME,
        "Married pensioner couple on £80k pension income": MARRIED_PENSIONER_COUPLE_80K_PENSION_INCOME,
        "Married couple with one kid, one earner": MARRIED_COUPLE_1_KID_1_EARNER,
        "Single adult on £60k": SINGLE_ADULT_HIGH_INCOME,
    }

    household_ids = [15564, 15663, 15650, 15651, 15568, 15685, 15570, 15571, 15572, 15573]

    @st.cache_data(show_spinner=False)
    def get_households_impact(reform):
        with st.spinner("Calculating impacts for example households..."):
            names = []
            baseline_incomes = []
            reform_incomes = []
            for name in households:
                baseline = requests.post(
                    API + "/calculate",
                    json={
                        "household": households[name],
                    },
                ).json()["result"]
                reformed = requests.post(
                    API + "/calculate",
                    json={
                        "household": households[name],
                        "policy": reform["data"],
                    },
                ).json()["result"]
                names.append(name)
                baseline_incomes.append(
                    baseline["households"]["household"][
                        "household_net_income"
                    ]["2023"]
                )
                reform_incomes.append(
                    reformed["households"]["household"][
                        "household_net_income"
                    ]["2023"]
                )

            df = pd.DataFrame(
                {
                    "Household": names,
                    "Baseline net income": baseline_incomes,
                    "Reformed net income": reform_incomes,
                }
            )

            df["Net income change"] = (
                df["Reformed net income"] - df["Baseline net income"]
            )

            for variable in [
                "Baseline net income",
                "Reformed net income",
                "Net income change",
            ]:
                df[variable] = df[variable].apply(
                    lambda x: f"{'-' if x < 0 else ''}£{abs(x):,.2f}"
                )
            return df.set_index("Household")

    df = get_households_impact(reform)
    df["PolicyEngine link"] = [
        f"https://policyengine.org/uk/household?household={household_id}&focus=householdOutput.netIncome"
        for household_id in household_ids
    ]
    st.write(df)


with st.expander("See the economic impact"):
    try:
        impact = get_economic_impact(reform)
    except:
        st.error(
            "We're having trouble computing the economic impact of your reforms. Please try again later."
        )
    else:
        budgetary_impact = impact["budget"]["budgetary_impact"]
        is_surplus = budgetary_impact < 0
        if budgetary_impact > 0:
            sentence = f"Your reforms would save £{abs(budgetary_impact/1e9):,.1f} billion per year"
        elif budgetary_impact < 0:
            sentence = f"Your reforms would cost £{abs(budgetary_impact/1e9):,.1f} billion per year"
        else:
            sentence = "Your reforms would have no impact on the budget"
        poverty_impact = (
            impact["poverty"]["poverty"]["all"]["reform"]
            / impact["poverty"]["poverty"]["all"]["baseline"]
            - 1
        )
        absolute_poverty_impact = (
            abs(
                impact["poverty"]["poverty"]["all"]["reform"]
                - impact["poverty"]["poverty"]["all"]["baseline"]
            )
            * 100
        )
        if poverty_impact > 0:
            sentence += f", raise poverty by {poverty_impact:.1%} ({absolute_poverty_impact:.1f} percentage points)"
        elif poverty_impact < 0:
            sentence += f", reduce poverty by {abs(poverty_impact):.1%} ({absolute_poverty_impact:.1f} percentage points)"
        else:
            sentence += ", have no impact on poverty"

        inequality_impact = (
            impact["inequality"]["gini"]["reform"]
            / impact["inequality"]["gini"]["baseline"]
            - 1
        )

        if inequality_impact > 0:
            sentence += f", and raise inequality by {inequality_impact:.1%}."
        elif inequality_impact < 0:
            sentence += (
                f", and reduce inequality by {abs(inequality_impact):.1%}."
            )
        else:
            sentence += ", and have no impact on inequality."

        st.write(sentence)

        decile_impact = impact["decile"]["relative"]
        decile_impact = {int(k): v for k, v in decile_impact.items()}

        def get_bar_colour(value):
            if value > 0:
                return DARK_GREEN
            elif value <= 0:
                return DARK_GRAY

        decile_chart = (
            px.bar(
                x=list(decile_impact.keys()),
                y=list(decile_impact.values()),
            )
            .update_layout(
                xaxis_title="Household income decile",
                yaxis_title="Distributional impact",
                xaxis_tickvals=list(range(1, 11)),
                xaxis_ticktext=list(range(1, 11)),
                yaxis_tickformat=".0%",
                template="plotly_white",
                title="Relative impact by decile",
            )
            .update_traces(
                marker_color=[
                    get_bar_colour(v) for v in decile_impact.values()
                ],
                text=[f"{v:+.1%}" for v in decile_impact.values()],
                textposition="inside",
            )
        )
        decile_chart.update_layout(
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            hovermode=False,
            margin=dict(r=100),
        )
        st.write(decile_chart)

        poverty_impact = impact["poverty"]["poverty"]

        labels = []
        values = []
        colour = []

        for group in ["child", "adult", "senior", "all"]:
            baseline = poverty_impact[group]["baseline"]
            reformed = poverty_impact[group]["reform"]
            labels.append(group)
            values.append(reformed / baseline - 1)
            colour.append(DARK_GREEN if reformed < baseline else DARK_GRAY)

        poverty_chart = (
            px.bar(
                x=["Children", "Working-age adults", "Seniors", "All"],
                y=values,
            )
            .update_layout(
                xaxis_title="Group",
                yaxis_title="Relative change in poverty",
                yaxis_tickformat=".0%",
                template="plotly_white",
                title="Poverty impact",
            )
            .update_traces(
                marker_color=colour,
                text=[f"{v:+.1%}" for v in values],
                textposition="inside",
            )
        )
        poverty_chart.update_layout(
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            hovermode=False,
            margin=dict(r=100),
        )
        st.write(poverty_chart)

st.subheader("Reforms you've previously simulated")

for data in sorted(st.session_state["history"], key=lambda x: x["timestamp"]):
    net_income_change = data["net_income_change"]
    if net_income_change > 0:
        message = f"increased your household's net income by £{net_income_change:,.0f}"
    elif net_income_change < 0:
        message = f"decreased your household's net income by £{-net_income_change:,.0f}"
    else:
        message = f"had no impact on your household's net income"
    time_message = humanize.naturaltime(
        datetime.datetime.now() - dateutil.parser.parse(data["timestamp"])
    )
    with st.expander(
        f"You simulated a policy that {message} ({time_message})"
    ):
        st.json(data["reform_details"], expanded=True)
