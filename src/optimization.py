from ortools.linear_solver import pywraplp
import pandas as pd

# -------------------------------
# Business configuration
# -------------------------------
MAX_REDUCTION_RATIO = 0.8
UNIT_PRODUCTION_COST = 50.0
UNIT_WASTE_PENALTY = 20.0

def optimize_production(daily_df: pd.DataFrame) -> pd.DataFrame:

    full_df = daily_df.copy()

    # Initialize output columns
    full_df["recommended_cut"] = 0.0
    full_df["cost_saving"] = 0.0
    full_df["waste_reduction_value"] = 0.0

    # Select ghost-demand rows
    ghost_df = full_df[
        (full_df["ghost_demand"] == 1) &
        (full_df["rolling_mean_7"] > full_df["daily_sales"])
    ].copy()

    if ghost_df.empty:
        return full_df

    solver = pywraplp.Solver.CreateSolver("GLOP")
    if solver is None:
        raise RuntimeError("OR-Tools solver could not be created")

    reduction_vars = {}

    # Decision variables
    for idx, row in ghost_df.iterrows():
        excess = row["rolling_mean_7"] - row["daily_sales"]
        max_cut = max(0.0, excess * MAX_REDUCTION_RATIO)

        reduction_vars[idx] = solver.NumVar(0.0, max_cut, f"cut_{idx}")

    # Objective: MAXIMIZE SAVINGS
    objective = solver.Objective()
    unit_saving = UNIT_PRODUCTION_COST + UNIT_WASTE_PENALTY

    for var in reduction_vars.values():
        objective.SetCoefficient(var, unit_saving)

    objective.SetMaximization()

    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        return full_df

    # Apply results
    for idx, var in reduction_vars.items():
        cut = var.solution_value()
        full_df.loc[idx, "recommended_cut"] = cut
        full_df.loc[idx, "cost_saving"] = cut * UNIT_PRODUCTION_COST
        full_df.loc[idx, "waste_reduction_value"] = cut * UNIT_WASTE_PENALTY

    return full_df
