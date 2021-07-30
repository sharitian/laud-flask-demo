import pandas as pd
import seaborn as sns
from scipy.stats import chi2_contingency
import sys 


def chi_sq_ind(var1, var2):
	data = pd.read_csv("results.csv")
	contingency= pd.crosstab(data[var1], data[var2])
	c, p, dof, expected = chi2_contingency(contingency)
	print(contingency)
	print("\n")
	print("Test statistic: " + str(c) + "\n" + "P-value: " + str(p) + "\n" + "Degrees Freedom: " + str(dof))

chi_sq_ind(str(sys.argv[1]), str(sys.argv[2]))
