from pathlib import Path
from sql import SparkRunner, Context
from spark.helpers import get_or_create_local_session
from spark.testing import assert_dataframes


class TestSQL:
    def test_execute_select_statement(self):
        spark_session = get_or_create_local_session("app")
        runner = SparkRunner(spark_session=spark_session)

        statement = "select 1"

        # pylint: disable=invalid-name
        df = runner.execute_template(statement)

        expected_df = spark_session.sql("select 1")
        assert_dataframes(expected_df, df)

    def test_compile_params(self):
        spark_session = get_or_create_local_session("app")
        runner = SparkRunner(spark_session=spark_session)

        context = Context(params={"logical_date": "2023-01-01"}, template_directory=".")

        statement = "SELECT '{{ params.logical_date }}' AS date"

        # pylint: disable=invalid-name
        df = runner.execute_template(statement, context=context)

        expected_df = spark_session.sql("select '2023-01-01' AS date")
        assert_dataframes(expected_df, df)

    def test_compile_template_file(self):
        spark_session = get_or_create_local_session("app")
        runner = SparkRunner(spark_session=spark_session)

        path = Path(__file__)
        template_directory = path.joinpath(
            path.parent.absolute(), "fixtures", "templates"
        )

        context = Context(
            params={"logical_date": "2023-01-01"}, template_directory=template_directory
        )

        # pylint: disable=invalid-name
        df = runner.execute_template_path("select_date.j2.sql", context=context)

        expected_df = spark_session.sql("select '2023-01-01' AS date")
        assert_dataframes(expected_df, df)
