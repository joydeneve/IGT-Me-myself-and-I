
# Assumptions:
# Student benefit (serious type): improved career earnings etc.
# Student benefit (flaky type): travel enjoyment, minor academic value
# Parent cost: financial cost of supporting year abroad
# Emotional payoffs: included as estimates
# Effort cost: time/energy of making a high-effort plan

# Costs and conversions
parent_cost_gbp = 7000  # Total parent cost to support a year abroad
student_serious_benefit_gbp = 30000  # Estimated lifetime benefit from year abroad for serious student
student_flaky_benefit_gbp = 5000     # Estimated benefit for flaky student
effort_cost_serious = 500            # Cost of preparing a high-effort plan for serious
effort_cost_flaky = 1500             # Cost of preparing a high-effort plan for flaky

# Parent emotional values (can be adjusted)
parent_happiness_if_serious_supported = 8000  # Value from seeing child succeed
parent_disappointment_if_flaky_supported = -5000
parent_regret_if_serious_not_supported = -6000
parent_relief_if_flaky_not_supported = 2000

# Define function to calculate net payoffs
def compute_payoffs():
    outcomes = []

    # Format: (Student Type, Signal, Parent Action)
    types = ['Serious', 'Flaky']
    signals = ['H', 'L']
    actions = ['S', 'N']

    for stype in types:
        for signal in signals:
            for action in actions:
                if stype == 'Serious':
                    benefit = student_serious_benefit_gbp if action == 'S' else 0
                    effort_cost = effort_cost_serious if signal == 'H' else 0
                else:
                    benefit = student_flaky_benefit_gbp if action == 'S' else 0
                    effort_cost = effort_cost_flaky if signal == 'H' else 0

                student_net = benefit - effort_cost

                if action == 'S':
                    parent_net = -parent_cost_gbp
                    if stype == 'Serious':
                        parent_net += parent_happiness_if_serious_supported
                    else:
                        parent_net += parent_disappointment_if_flaky_supported
                else:
                    if stype == 'Serious':
                        parent_net = parent_regret_if_serious_not_supported
                    else:
                        parent_net = parent_relief_if_flaky_not_supported

                outcomes.append({
                    'Student Type': stype,
                    'Signal': signal,
                    'Parent Action': action,
                    'Student Payoff (GBP)': student_net,
                    'Parent Payoff (GBP)': parent_net
                })

    return outcomes

import pandas as pd

payoffs_df = pd.DataFrame(compute_payoffs())
payoffs_df['Student Payoff (GBP)'] = payoffs_df['Student Payoff (GBP)'] / 1000
payoffs_df['Parent Payoff (GBP)'] = payoffs_df['Parent Payoff (GBP)'] / 1000

# Rename columns
payoffs_df.rename(columns={
    'Student Payoff (GBP)': 'Student Payoff (k GBP)',
    'Parent Payoff (GBP)': 'Parent Payoff (k GBP)'
}, inplace=True)

print(payoffs_df)
payoffs_df.to_csv("payoff_results.csv", index=False)
print("Results saved to payoff_results.csv ✅")
