from matplotlib import pyplot as plt
from SRS.models import *

pie_values = [0, 0]

ratings = SRS.objects.all()
graph_values = []
for rating in ratings:
	graph_values.append(rating.feedbackScore)

for i in graph_values:
	if float(i) > 0:
		pie_values[0] += 1
	else:
		pie_values[1] += 1

print graph_values
dt=['Number of Reviews','Rating']
plt.plot(graph_values, data=dt)
plt.savefig("graph.png")

lbl=["Positive","Negative"]
plt.pie(pie_values,labels=lbl)
plt.savefig("pie.png")