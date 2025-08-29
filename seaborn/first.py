# Step 0: Install libraries
# pip install seaborn matplotlib pandas

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Load dataset
df = sns.load_dataset('tips')
print("Dataset Head:\n", df.head())

# ==========================
# Step 2: Basic Plots
# ==========================

# 2.1 Scatter Plot
sns.scatterplot(x='total_bill', y='tip', data=df)
plt.title("Scatter Plot: Total Bill vs Tip")
plt.show()

# 2.2 Line Plot
sns.lineplot(x='size', y='tip', data=df)
plt.title("Line Plot: Group Size vs Tip")
plt.show()

# 2.3 Bar Plot
sns.barplot(x='day', y='total_bill', data=df)
plt.title("Bar Plot: Average Total Bill per Day")
plt.show()

# 2.4 Histogram / Distribution Plot
sns.histplot(df['total_bill'], kde=True)
plt.title("Histogram: Total Bill Distribution")
plt.show()

# 2.5 Box Plot
sns.boxplot(x='day', y='total_bill', data=df, hue='sex')
plt.title("Box Plot: Total Bill by Day and Gender")
plt.show()

# 2.6 Violin Plot
sns.violinplot(x='day', y='total_bill', data=df, hue='sex', split=True)
plt.title("Violin Plot: Total Bill Distribution by Day and Gender")
plt.show()

# ==========================
# Step 3: Advanced Plots
# ==========================

# 3.1 Pairplot
sns.pairplot(df, hue='sex')
plt.show()

# 3.2 Heatmap (Correlation)
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Heatmap: Correlation")
plt.show()

# 3.3 Countplot
sns.countplot(x='day', data=df, hue='sex')
plt.title("Count Plot: Number of Bills by Day and Gender")
plt.show()

# 3.4 Regression Plot
sns.regplot(x='total_bill', y='tip', data=df)
plt.title("Regression Plot: Total Bill vs Tip")
plt.show()

# 3.5 FacetGrid
g = sns.FacetGrid(df, col="sex", row="time")
g.map(sns.scatterplot, "total_bill", "tip")
plt.show()

# ==========================
# Step 4: Customization
# ==========================

sns.set_style('whitegrid')   # styles: whitegrid, darkgrid, ticks, white, dark
sns.set_palette('Set2')       # color palettes
sns.scatterplot(x='total_bill', y='tip', hue='day', style='sex', data=df, s=100)
plt.title('Customized Scatter Plot')
plt.xlabel('Total Bill')
plt.ylabel('Tip')
plt.show()

# ==========================
# Step 5: Real-world Examples
# ==========================

# Example 1: Sales Data
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
