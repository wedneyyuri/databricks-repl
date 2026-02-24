import time
from pyspark.sql import functions as F

NUM_SAMPLES = 100_000_000

start = time.time()

df = (
    spark.range(0, NUM_SAMPLES)
    .withColumn("x", F.rand(seed=42))
    .withColumn("y", F.rand(seed=123))
    .withColumn("inside", (F.col("x") ** 2 + F.col("y") ** 2 <= 1).cast("int"))
)

count_inside = df.agg(F.sum("inside")).collect()[0][0]
elapsed = time.time() - start

pi_estimate = 4.0 * count_inside / NUM_SAMPLES
error = abs(pi_estimate - 3.141592653589793)

print(f"Samples:     {NUM_SAMPLES:,}")
print(f"Inside:      {count_inside:,}")
print(f"Pi estimate: {pi_estimate:.10f}")
print(f"Actual Pi:   3.1415926536")
print(f"Error:       {error:.10f}")
print(f"Elapsed:     {elapsed:.1f}s")