from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris()
pdf = pd.DataFrame(iris.data, columns=iris.feature_names)
pdf["label"] = iris.target
pdf["species"] = pdf["label"].map(dict(enumerate(iris.target_names)))

df = spark.createDataFrame(pdf)
df.printSchema()
df.describe().show()
df.groupBy("species").count().show()
print(f"Total samples: {df.count()}")