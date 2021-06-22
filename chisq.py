
import pandas as pd
import seaborn as sns
from scipy.stats import chi2_contingency

def chi_sq(cat1, cat2):
	diamonds = pd.read_csv("diamonds.csv")
	contigency= pd.crosstab(diamonds[cat1], diamonds[cat2]) 
	c, p, dof, expected = chi2_contingency(contigency)
	return("Test statistic: " + str(c) + "\n" + "P-value: "  + str(p) + "\n" + "Degrees Freedom: "  + str(dof))


if __name__ == '__main__':
    print(chi_sq("Color", "Clarity"))
