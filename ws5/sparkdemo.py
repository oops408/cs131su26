import sys

from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession


def main():
    # Making sure dataset path is provided
    if len(sys.argv) < 2:
        print("Usage: sparkdemo.py <gs://bucket/path/tips.csv>")
        sys.exit(1)

    input_path = sys.argv[1]

    # A1. Create a SparkSession named ws5-regression.
    spark = (
        SparkSession.builder
        .appName("ws5-regression")
        .getOrCreate()
    )

    try:
        # A2. Read the dataset from your bucket into a DataFrame 
        # with the header row as column names and column types 
        # inferred, then .show() it. 
        tips_df = (
            spark.read
            .option("header", "true")
            .option("inferSchema", "true")
            .csv(input_path)
        )

        print("Tips dataset:")
        tips_df.show()

        # A3. Combine the two predictor columns total_bill and size 
        # into a single vector column called features.
        assembler = VectorAssembler(
            inputCols=["total_bill", "size"],
            outputCol="features"
        )

        # A4. Split the data into 80% train / 20% test. Pass a fixed 
        # seed so the split is reproducible. (Hint: .randomSplit().)
        train_df, test_df = tips_df.randomSplit(
            [0.8, 0.2],
            seed=42
        )

        print(f"Training rows: {train_df.count()}")
        print(f"Testing rows: {test_df.count()}")

        # A5. Define a LinearRegression with featuresCol="features" and 
        # labelCol="tip", and fit the model. Chain the assembler (A3) 
        # and the regressor into a Pipeline and call .fit() on the training set.
        linear_regression = LinearRegression(
            featuresCol="features",
            labelCol="tip"
        )

        pipeline = Pipeline(
            stages=[assembler, linear_regression]
        )

        pipeline_model = pipeline.fit(train_df)

        # A6. Apply the fitted pipeline to the 
        # test set to produce predictions.
        predictions = pipeline_model.transform(test_df)

        print("Predictions:")
        predictions.select(
            "total_bill",
            "size",
            "tip",
            "prediction"
        ).show()

        # A7. Evaluate the predictions on two metrics: RMSE and R². 
        # Use one evaluator with the label column tip, changing metricName.
        evaluator = RegressionEvaluator(
            labelCol="tip",
            predictionCol="prediction"
        )

        rmse = evaluator.setMetricName("rmse").evaluate(predictions)
        r2 = evaluator.setMetricName("r2").evaluate(predictions)

        # A8. Pull the fitted LinearRegression model out of the 
        # pipeline (pipelineModel.stages[-1]) and print its coefficients 
        # and intercept, plus the RMSE and R² from A7. 
        # Use clear labels (e.g. print(f"RMSE: {rmse}")) so the numbers 
        # stand out in the job log.
        fitted_lr_model = pipeline_model.stages[-1]

        print("----- Linear Regression Results -----")
        print(f"Coefficients: {fitted_lr_model.coefficients}")
        print(f"Total bill coefficient: {fitted_lr_model.coefficients[0]}")
        print(f"Party size coefficient: {fitted_lr_model.coefficients[1]}")
        print(f"Intercept: {fitted_lr_model.intercept}")
        print(f"RMSE: {rmse}")
        print(f"R²: {r2}")
        print("-------------------------------------")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()

"""
References:
https://www.microsoft.com/en-us/research/articles/getting-deterministic-results-from-sparks-randomsplit-function/
https://spark.apache.org/docs/latest/ml-guide.html
https://stackoverflow.com/questions/50979024/spark-randomsplit-inconsistent-results-for-every-run
https://stackoverflow.com/questions/36995214/pyspark-logistic-regression-how-to-get-coefficient-of-respective-features
https://stackoverflow.com/questions/36697304/how-to-extract-model-hyper-parameters-from-spark-ml-in-pyspark
Github Copilot/ChatGPT for debugging/testing
"""
