import matplotlib.pyplot as plt

daily_df[daily_df['ghost_demand'] == 1]['forecast_error'].hist(bins=30)
plt.title("Distribution of Forecast Error for Ghost Demand Cases")
plt.xlabel("Expected − Actual Sales")
plt.ylabel("Frequency")
plt.show()
