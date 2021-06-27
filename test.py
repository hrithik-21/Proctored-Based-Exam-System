import pandas as pd
import matplotlib.pyplot as plt
csv_file='data.csv'
data = pd.read_csv(csv_file)
data1 = pd.read_csv('data1.csv')
a = data["Name"]
b = data["Score"]
x=[]
y=[]
print(a)
print(b)
x=list(a)
y=list(b)
plt.bar(x,y)
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.show()