# Step 0: Install libraries
# pip install seaborn matplotlib pandas

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Optional: Better style
sns.set_style('whitegrid')
sns.set_palette('Set2')

# ==========================
# STEP 1: LOAD DATASETS
# ==========================
df_tips = sns.load_dataset('tips')       # Restaurant tips
df_iris = sns.load_dataset('iris')       # Iris flower dataset
df_flights = sns.load_dataset('flights') # Flights data
df_penguins = sns.load_dataset('penguins') # Penguins dataset

print("Tips Dataset Head:\n", df_tips.head())

# ==========================
# STEP 2: BASIC PLOTS
# ==========================

# 2.1 Scatter Plot (Relationship between 2 numeric variables)
sns.scatterplot(x='total_bill', y='tip', data=df_tips)
plt.title("Scatter Plot: Total Bill vs Tip")
plt.show()

# 2.2 Line Plot (Trend over numeric variable)
sns.lineplot(x='size', y='tip', data=df_tips)
plt.title("Line Plot: Group Size vs Tip")
plt.show()

# 2.3 Bar Plot (Categorical data)
sns.barplot(x='day', y='total_bill', data=df_tips)
plt.title("Bar Plot: Average Total Bill per Day")
plt.show()

# 2.4 Histogram / Distribution Plot
sns.histplot(df_tips['total_bill'], kde=True)
plt.title("Histogram: Total Bill Distribution")
plt.show()

# 2.5 Box Plot (Outliers and distribution)
sns.boxplot(x='day', y='total_bill', data=df_tips, hue='sex')
plt.title("Box Plot: Total Bill by Day & Gender")
plt.show()

# 2.6 Violin Plot (Distribution + Density)
sns.violinplot(x='day', y='total_bill', data=df_tips, hue='sex', split=True)
plt.title("Violin Plot: Total Bill Distribution by Day & Gender")
plt.show()

# ==========================
# STEP 3: INTERMEDIATE PLOTS
# ==========================

# 3.1 Pairplot (All numeric features comparison)
sns.pairplot(df_iris, hue='species')
plt.show()

# 3.2 Countplot (Frequency of categorical variable)
sns.countplot(x='day', data=df_tips, hue='sex')
plt.title("Count Plot: Bills by Day & Gender")
plt.show()

# 3.3 Regression Plot (Numeric trend with regression line)
sns.regplot(x='total_bill', y='tip', data=df_tips)
plt.title("Regression Plot: Total Bill vs Tip")
plt.show()

# 3.4 Heatmap (Correlation)
corr = df_tips.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Heatmap: Correlation")
plt.show()

# 3.5 FacetGrid (Multiple plots by category)
g = sns.FacetGrid(df_tips, col="sex", row="time")
g.map(sns.scatterplot, "total_bill", "tip")
plt.show()

# ==========================
# STEP 4: ADVANCED PLOTS
# ==========================

# 4.1 Catplot (Flexible categorical plot)
sns.catplot(x='day', y='total_bill', hue='sex', kind='box', data=df_tips)
plt.title("Catplot: Box Plot per Day & Gender")
plt.show()

# 4.2 PairGrid (Custom pairwise plots)
g = sns.PairGrid(df_iris, hue='species')
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.map_diag(sns.histplot)
g.add_legend()
plt.show()

# 4.3 Heatmap with pivot table (Flights example)
pivot = df_flights.pivot("month","year","passengers")
sns.heatmap(pivot, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Flights Heatmap: Passengers by Month & Year")
plt.show()

# 4.4 Advanced scatter with size & style
sns.scatterplot(
    x='total_bill', y='tip', hue='day', style='sex', size='size',
    data=df_tips, sizes=(20,200), palette='coolwarm'
)
plt.title("Advanced Scatter Plot")
plt.show()

# ==========================
# STEP 5: REAL-WORLD EXAMPLES
# ==========================

# Example 1: Monthly Revenue Barplot
sales_df = pd.DataFrame({
    'Month':['Jan','Feb','Mar','Apr'],
    'Revenue':[2000, 3000, 4000, 3500]
})
sns.barplot(x='Month', y='Revenue', data=sales_df)
plt.title("Monthly Revenue")
plt.show()

# Example 2: Student Scores Heatmap
students_df = pd.DataFrame({
    'Student':['A','B','C','D'],
    'Math':[80,90,70,85],
    'Science':[75,85,80,90]
})
sns.heatmap(students_df.set_index('Student'), annot=True, cmap='YlGnBu')
plt.title("Student Scores Heatmap")
plt.show()

# Example 3: Penguins dataset - scatterplot by species
sns.scatterplot(
    x='flipper_length_mm', y='body_mass_g', hue='species', style='sex', size='bill_length_mm',
    data=df_penguins, sizes=(50,300), palette='Set1'
)
plt.title("Penguins: Flipper vs Body Mass")
plt.show()

# Example 4: Time series line plot (Flights dataset)
sns.lineplot(x='year', y='passengers', hue='month', data=df_flights)
plt.title("Passengers Over Years by Month")
plt.show()
