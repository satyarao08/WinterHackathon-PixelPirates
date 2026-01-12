from ortools.linear_solver import pywraplp
ghost_df = daily_df[daily_df['ghost_demand'] == 1].copy()

print(f"Ghost-demand cases to optimize: {len(ghost_df)}")
# Business assumptions (mock but realistic)
UNIT_PRODUCTION_COST = 50      # cost per unit produced
UNIT_WASTE_PENALTY = 20        # waste / sustainability penalty per unit
MAX_REDUCTION_RATIO = 0.8      # do not cut more than 80% of excess demand
solver = pywraplp.Solver.CreateSolver('SCIP')

if solver is None:
    raise RuntimeError("Solver not available")
reduction_vars = {}

for idx, row in ghost_df.iterrows():
    max_cut = max(row['forecast_error'], 0) * MAX_REDUCTION_RATIO
    
    reduction_vars[idx] = solver.NumVar(
        0,
        max_cut,
        f"cut_{idx}"
    )
    # (cost + waste) * production_cut

UNIT_PRODUCTION_COST = 50
UNIT_WASTE_PENALTY = 20
unit_penalty = UNIT_PRODUCTION_COST + UNIT_WASTE_PENALTY
objective = solver.Objective()

unit_penalty = UNIT_PRODUCTION_COST + UNIT_WASTE_PENALTY

for var in reduction_vars.values():
    objective.SetCoefficient(var, unit_penalty)

objective.SetMaximization()
status = solver.Solve()

if status != pywraplp.Solver.OPTIMAL:
    raise RuntimeError("Optimization did not find an optimal solution")

print("Optimization solved successfully.")
status = solver.Solve()

if status != pywraplp.Solver.OPTIMAL:
    raise RuntimeError("Optimization did not find an optimal solution")

print("Optimization solved successfully.")
ghost_df['recommended_cut'] = 0.0

for idx, var in reduction_vars.items():
    ghost_df.loc[idx, 'recommended_cut'] = var.solution_value()
    ghost_df['cost_saving'] = ghost_df['recommended_cut'] * UNIT_PRODUCTION_COST
ghost_df['waste_reduction_value'] = ghost_df['recommended_cut'] * UNIT_WASTE_PENALTY
print("Total units reduced:", ghost_df['recommended_cut'].sum())
print("Total production cost saved:", ghost_df['cost_saving'].sum())
print("Total waste reduction value:", ghost_df['waste_reduction_value'].sum())
ghost_df[[
    'Date',
    'SKU',
    'daily_sales',
    'rolling_mean_7',
    'forecast_error',
    'recommended_cut',
    'cost_saving',
    'waste_reduction_value'
]].sort_values('recommended_cut', ascending=False).head(10)
ghost_df['recommended_cut'].describe()
ghost_df['cost_saving'].sum(), ghost_df['waste_reduction_value'].sum()
