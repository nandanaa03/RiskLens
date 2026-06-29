from backend.etl.pipeline import ETLPipeline

df, summary = ETLPipeline.run("data/raw/NFHS-5-States.csv")

print(df.head())

print()

print(df.columns)

print()

print(df.shape)