import streamlit as st
import requests
import time
import plotly.express as px

API = "https://api.policyengine.org/uk"

@st.cache(show_spinner=False)
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
    padding-bottom: 1000px !important;
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

st.title("Citizens' Economic Council: reform simulator")
st.markdown("This is a prototype of a tool that will allow you to explore the impact of tax-benefit reforms on your household. Enter your household details, then build a reform to see how it would affect you.")

with st.expander("Enter your household details"):
    brma_label = st.selectbox("What Broad Rental Market Area do you live in?", [x["label"] for x in variables["BRMA"]["possibleValues"]])
    brma = [x["value"] for x in variables["BRMA"]["possibleValues"] if x["label"] == brma_label][0]
    marital_status = st.selectbox("What is your marital status?", ["Single", "Married"])

    people = {}
    if marital_status == "Single":
        age = st.number_input("How old are you?", step=1, value=30, key="single_age")
        if age < 65:
            employment_income = st.slider("What is your annual employment income?", min_value=0, max_value=100000, step=1000, key="single_employment_income")
            state_pension = 0
            pension_income = 0
        else:
            employment_income = 0
            state_pension = st.slider("What is your annual state pension?", min_value=0, max_value=10000, step=100, key="single_state_pension")
            pension_income = st.slider("What is your annual pension income?", min_value=0, max_value=10000, step=100, key="single_pension_income")
        people["adult_1"] = {
            "age": {2023: age},
            "employment_income": {2023: employment_income},
            "state_pension": {2023: state_pension},
            "pension_income": {2023: pension_income},
        }
    else:
        age = st.number_input("How old are you?", step=1, value=30, key="married_age")
        if age < 65:
            employment_income = st.slider("What is your annual employment income?", min_value=0, max_value=100000, step=1000, key="married_employment_income")
            state_pension = 0
            pension_income = 0
        else:
            employment_income = 0
            state_pension = st.slider("What is your annual state pension?", min_value=0, max_value=10000, step=100, key="married_state_pension")
            pension_income = st.slider("What is your annual pension income?", min_value=0, max_value=10000, step=100, key="married_pension_income")
        
        people["adult_1"] = {
            "age": {2023: age},
            "employment_income": {2023: employment_income},
            "state_pension": {2023: state_pension},
            "pension_income": {2023: pension_income},
        }

        partner_age = st.number_input("How old is your partner?", step=1, value=30, key="married_partner_age")
        if partner_age < 65:
            partner_employment_income = st.slider("What is your partner's annual employment income?", min_value=0, max_value=100000, step=1000, key="married_partner_employment_income")
            partner_state_pension = 0
            partner_pension_income = 0
        else:
            partner_employment_income = 0
            partner_state_pension = st.slider("What is your partner's annual state pension?", min_value=0, max_value=10000, step=100, key="married_partner_state_pension")
            partner_pension_income = st.slider("What is your partner's annual pension income?", min_value=0, max_value=10000, step=100, key="married_partner_pension_income")
        people["adult_2"] = {
            "age": {2023: age},
            "employment_income": {2023: partner_employment_income},
            "state_pension": {2023: partner_state_pension},
            "pension_income": {2023: partner_pension_income},
        }

    children = st.number_input("How many children live in your household?", step=1)

    for i in range(children):
        age = st.number_input(f"How old is child {i+1}?", step=1, value=10)
        people[f"child_{i+1}"] = {
            "age": {2023: age},
        }

    full_rate_consumption = st.slider(f"How much do you spend per year?", min_value=0, max_value=100000, step=100, key="full_rate_consumption") * 0.5

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
                "household_net_income": {2023: None},
                "household_benefits": {2023: None},
                "household_tax": {2023: None},
            },
        },
    }

with st.expander("Select a tax-benefit reform"):
    st.write("Should the government...")
    basic_rate = st.select_slider("change the basic rate of income tax?", options=["lower to 18%", "keep the same", "raise to 22%"], value="keep the same")
    basic_rate = {"lower to 18%": 0.18, "keep the same": 0.2, "raise to 22%": 0.22}[basic_rate]
    progressivity = st.select_slider("change the higher and additional rates?", options=["cut both by 5p", "keep the same", "raise the higher/additional rates by 5p"], value="keep the same")
    higher_rate = {"cut both by 5p": 0.35, "keep the same": 0.4, "raise the higher/additional rates by 5p": 0.45}[progressivity]
    additional_rate = {"cut both by 5p": 0.4, "keep the same": 0.45, "raise the higher/additional rates by 5p": 0.5}[progressivity]
    vat = st.select_slider("change the VAT rate?", options=["lower to 15%", "keep the same", "raise to 25%"], value="keep the same")
    vat = {"lower to 15%": 0.15, "keep the same": 0.2, "raise to 25%": 0.25}[vat]
    wealth_tax = st.select_slider("introduce a wealth tax?", options=["no", "1%", "5%"], value="no")
    wealth_tax = {"no": 0, "1%": 0.01, "5%": 0.05}[wealth_tax]
    benefits = st.select_slider("change benefits?", options=["decrease by 5%", "no", "increase by 5%"], value="no")
    benefits = {"no": 0, "decrease by 5%": -0.05, "increase by 5%": 0.05}[benefits]
    ubi = st.select_slider("introduce a universal basic income?", options=["no", "£10 per week", "£30 per week"], value="no")
    ubi = {"no": 0, "£10 per week": 10, "£30 per week": 30}[ubi]

    reform = {
        "gov.hmrc.income_tax.rates.uk[0].rate": {"2023-01-01.2024-01-01": basic_rate},
        "gov.hmrc.income_tax.rates.uk[1].rate": {"2023-01-01.2024-01-01": higher_rate},
        "gov.hmrc.income_tax.rates.uk[2].rate": {"2023-01-01.2024-01-01": additional_rate},
        "gov.contrib.ubi_center.wealth_tax[0].rate": {"2023-01-01.2024-01-01": wealth_tax},
        "gov.contrib.ubi_center.basic_income.amount.flat": {"2023-01-01.2024-01-01": ubi},
        "gov.contrib.benefit_uprating.non_sp": {"2023-01-01.2024-01-01": benefits},
        "gov.hmrc.vat.standard_rate": {"2023-01-01.2024-01-01": vat},
    }

    reform = {
        "data": reform,
    }

@st.cache(show_spinner=False)
def get_household_impact(household, reform):
    baseline = requests.post(API + "/calculate", json={
        "household": household,
    }).json()["result"]
    reformed = requests.post(API + "/calculate", json={
        "household": household,
        "policy": reform,
    }).json()["result"]
    return baseline, reformed

baseline, reformed = get_household_impact(situation, reform["data"])
st.write("## Your household's impact")

baseline_net_income = baseline["households"]["household"]["household_net_income"]["2023"]
reform_net_income = reformed["households"]["household"]["household_net_income"]["2023"]

baseline_benefits = baseline["households"]["household"]["household_benefits"]["2023"]
reform_benefits = reformed["households"]["household"]["household_benefits"]["2023"]

baseline_tax = baseline["households"]["household"]["household_tax"]["2023"]
reform_tax = reformed["households"]["household"]["household_tax"]["2023"]

if reform_net_income > baseline_net_income:
    st.success(f"Your household would be £{reform_net_income - baseline_net_income:,.0f} better off under these reforms.")
elif reform_net_income < baseline_net_income:
    st.error(f"Your household would be £{baseline_net_income - reform_net_income:,.0f} worse off under these reforms.")
else:
    st.warning(f"Your household would be no better or worse off under these reforms.")

def get_colour(x, y):
    if y > x:
        return "normal"
    elif y == x:
        return "off"
    else:
        return "inverse"

col1, col2, col3 = st.columns(3)
col1.metric("Net income", f"£{reform_net_income:,.0f}", int(reform_net_income - baseline_net_income))
col2.metric("Benefits", f"£{reform_benefits:,.0f}", int(reform_benefits - baseline_benefits))
col3.metric("Tax", f"£{reform_tax:,.0f}", int(reform_tax - baseline_tax))

@st.cache(show_spinner=False)
def get_economic_impact(reform):
    with st.spinner("Computing the economic impact..."):
        policy_id = requests.post(API + "/policy", json=reform).json()["result"]["policy_id"]
        impact = requests.get(API + f"/economy/{policy_id}/over/1?region=uk&time_period=2023").json()
        while impact["status"] == "computing":
            time.sleep(2)
            impact = requests.get(API + f"/economy/{policy_id}/over/1?region=uk&time_period=2023").json()
        return impact["result"]

with st.expander("See the economic impact"):
    impact = get_economic_impact(reform)
    budgetary_impact = impact["budget"]["budgetary_impact"]
    is_surplus = budgetary_impact < 0
    if budgetary_impact > 0:
        sentence = f"Your reforms would save £{abs(budgetary_impact/1e9):,.1f} billion per year"
    elif budgetary_impact < 0:
        sentence = f"Your reforms would cost £{abs(budgetary_impact/1e9):,.1f} billion per year"
    else:
        sentence = "Your reforms would have no impact on the budget"
    poverty_impact = impact["poverty"]["poverty"]["all"]["reform"] / impact["poverty"]["poverty"]["all"]["baseline"] - 1
    if poverty_impact > 0:
        sentence += f", raise poverty by {poverty_impact:.1%}"
    elif poverty_impact < 0:
        sentence += f", reduce poverty by {abs(poverty_impact):.1%}"
    else:
        sentence += ", have no impact on poverty"
    
    inequality_impact = impact["inequality"]["gini"]["reform"] / impact["inequality"]["gini"]["baseline"] - 1

    if inequality_impact > 0:
        sentence += f", and raise inequality by {inequality_impact:.1%}."
    elif inequality_impact < 0:
        sentence += f", and reduce inequality by {abs(inequality_impact):.1%}."
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


    decile_chart = px.bar(
        x=list(decile_impact.keys()),
        y=list(decile_impact.values()),
    ).update_layout(
        xaxis_title="Household income decile",
        yaxis_title="Distributional impact",
        xaxis_tickvals=list(range(1, 11)),
        xaxis_ticktext=list(range(1, 11)),
        yaxis_tickformat=".0%",
        template="plotly_white",
        title="Relative impact by decile",
    ).update_traces(
        marker_color=[get_bar_colour(v) for v in decile_impact.values()],
        text=[f"{v:+.1%}" for v in decile_impact.values()],
        textposition="inside",
    )
    decile_chart.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode=False,
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
    
    poverty_chart = px.bar(
        x=["Children", "Working-age adults", "Seniors", "All"],
        y=values,
    ).update_layout(
        xaxis_title="Group",
        yaxis_title="Relative change in poverty",
        yaxis_tickformat=".0%",
        template="plotly_white",
        title="Poverty impact",
    ).update_traces(
        marker_color=colour,
        text=[f"{v:+.1%}" for v in values],
        textposition="inside",
    )
    poverty_chart.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode=False,
    )
    st.write(poverty_chart)
    