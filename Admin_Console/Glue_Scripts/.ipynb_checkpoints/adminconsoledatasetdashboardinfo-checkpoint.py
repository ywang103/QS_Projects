import json
import boto3
import logging
import csv
import io
import os
import tempfile
from typing import Any, Callable, Dict, List, Optional, Union
import sys
from awsglue.utils import getResolvedOptions
import botocore

def default_botocore_config() -> botocore.config.Config:
    """Botocore configuration."""
    retries_config: Dict[str, Union[str, int]] = {
        "max_attempts": int(os.getenv("AWS_MAX_ATTEMPTS", "5")),
    }
    mode: Optional[str] = os.getenv("AWS_RETRY_MODE")
    if mode:
        retries_config["mode"] = mode
    return botocore.config.Config(
        retries=retries_config,
        connect_timeout=10,
        max_pool_connections=10,
        user_agent_extra=f"qs_sdk_admin_console",
    )

sts_client = boto3.client("sts", config=default_botocore_config())
account_id = sts_client.get_caller_identity()["Account"]
aws_region = 'us-east-1'
args = getResolvedOptions(sys.argv, ['AWS_REGION'])
print('region', args['AWS_REGION'])
glue_aws_region = args['AWS_REGION']
qs_client = boto3.client('quicksight', config=default_botocore_config())
qs_local_client = boto3.client('quicksight', region_name=glue_aws_region, config=default_botocore_config())

def _list(
        func_name: str,
        attr_name: str,
        account_id: str,
        aws_region: str,
        **kwargs, ) -> List[Dict[str, Any]]:
    qs_client = boto3.client('quicksight', region_name=aws_region, config=default_botocore_config())
    func: Callable = getattr(qs_client, func_name)
    response = func(AwsAccountId=account_id, **kwargs)
    next_token: str = response.get("NextToken", None)
    result: List[Dict[str, Any]] = response[attr_name]
    while next_token is not None:
        response = func(AwsAccountId=account_id, NextToken=next_token, **kwargs)
        next_token = response.get("NextToken", None)
        result += response[attr_name]
    return result


def list_dashboards(
        account_id,
        aws_region
) -> List[Dict[str, Any]]:
    return _list(
        func_name="list_dashboards",
        attr_name="DashboardSummaryList",
        account_id=account_id,
        aws_region=aws_region
    )


def list_analyses(
        account_id,
        aws_region
) -> List[Dict[str, Any]]:
    return _list(
        func_name="list_analyses",
        attr_name="AnalysisSummaryList",
        account_id=account_id,
        aws_region=aws_region
    )


def list_themes(
        account_id,
        aws_region
) -> List[Dict[str, Any]]:
    return _list(
        func_name="list_themes",
        attr_name="ThemeSummaryList",
        account_id=account_id,
        aws_region=aws_region
    )

def list_datasets(
        account_id,
        aws_region
) -> List[Dict[str, Any]]:
    return _list(
        func_name="list_data_sets",
        attr_name="DataSetSummaries",
        account_id=account_id,
        aws_region=aws_region
    )


def list_datasources(
        account_id,
        aws_region
) -> List[Dict[str, Any]]:
    return _list(
        func_name="list_data_sources",
        attr_name="DataSources",
        account_id=account_id,
        aws_region=aws_region
    )


def list_ingestions(
        account_id,
        aws_region,
        DataSetId
) -> List[Dict[str, Any]]:
    return _list(
        func_name="list_ingestions",
        attr_name="Ingestions",
        account_id=account_id,
        aws_region=aws_region,
        DataSetId=DataSetId
    )


def describe_dashboard(account_id, dashboardid, aws_region):
    qs_client = boto3.client('quicksight', region_name=aws_region, config=default_botocore_config())
    res = qs_client.describe_dashboard(
        AwsAccountId=account_id,
        DashboardId=dashboardid
    )
    return res


def describe_analysis(account_id, id, aws_region):
    qs_client = boto3.client('quicksight', region_name=aws_region, config=default_botocore_config())
    res = qs_client.describe_analysis(
        AwsAccountId=account_id,
        AnalysisId=id
    )
    return res


def describe_data_set(account_id, id, aws_region):
    qs_client = boto3.client('quicksight', region_name=aws_region, config=default_botocore_config())
    res = qs_client.describe_data_set(
        AwsAccountId=account_id,
        DataSetId=id
    )
    return res


def describe_data_source(account_id, id, aws_region):
    qs_client = boto3.client('quicksight', region_name=aws_region, config=default_botocore_config())
    res = qs_client.describe_data_source(
        AwsAccountId=account_id,
        DataSourceId=id
    )
    return res


def describe_dashboard_permissions(account_id, dashboardid, aws_region):
    qs_client = boto3.client('quicksight', region_name=aws_region, config=default_botocore_config())
    res = qs_client.describe_dashboard_permissions(
        AwsAccountId=account_id,
        DashboardId=dashboardid
    )
    return res


def describe_analysis_permissions(account_id, aid, aws_region):
    qs_client = boto3.client('quicksight', region_name=aws_region, config=default_botocore_config())
    res = qs_client.describe_analysis_permissions(
        AwsAccountId=account_id,
        AnalysisId=aid
    )
    return res


def describe_theme_permissions(account_id, aid, aws_region):
    qs_client = boto3.client('quicksight', region_name=aws_region, config=default_botocore_config())
    res = qs_client.describe_theme_permissions(
        AwsAccountId=account_id,
        ThemeId=aid
    )
    return res


def describe_data_set_permissions(account_id, datasetid, aws_region):
    qs_client = boto3.client('quicksight', region_name=aws_region, config=default_botocore_config())
    res = qs_client.describe_data_set_permissions(
        AwsAccountId=account_id,
        DataSetId=datasetid
    )
    return res


def describe_data_source_permissions(account_id, DataSourceId, aws_region):
    qs_client = boto3.client('quicksight', region_name=aws_region, config=default_botocore_config())
    res = qs_client.describe_data_source_permissions(
        AwsAccountId=account_id,
        DataSourceId=DataSourceId
    )
    return res

if __name__ == "__main__":
    sts_client = boto3.client("sts", region_name=aws_region, config=default_botocore_config())
    account_id = sts_client.get_caller_identity()["Account"]

    # call s3 bucket
    s3 = boto3.resource('s3')
    bucketname = 'admin-console-new-' + account_id
    bucket = s3.Bucket(bucketname)

    key = 'monitoring/quicksight/datsets_info/datsets_info.csv'
    key2 = 'monitoring/quicksight/datsets_ingestion/datsets_ingestion.csv'
    key3 = 'monitoring/quicksight/data_dictionary/data_dictionary.csv'
    tmpdir = tempfile.mkdtemp()
    local_file_name = 'datsets_info.csv'
    local_file_name2 = 'datsets_ingestion.csv'
    local_file_name3 = 'data_dictionary.csv'
    path = os.path.join(tmpdir, local_file_name)
    path2 = os.path.join(tmpdir, local_file_name2)
    path3 = os.path.join(tmpdir, local_file_name3)

    access = []

    data_dictionary = []

    dashboards = list_dashboards(account_id, glue_aws_region)

    for dashboard in dashboards:
        dashboardid = dashboard['DashboardId']

        response = describe_dashboard(account_id, dashboardid, glue_aws_region)
        Dashboard = response['Dashboard']
        Name = Dashboard['Name']
        
        print(Dashboard)
        if 'SourceEntityArn' in Dashboard['Version']:
            SourceEntityArn = Dashboard['Version']['SourceEntityArn']
            SourceType = SourceEntityArn.split(":")[-1].split("/")[0]
            print(SourceType)
            if SourceType == 'analysis':
                Sourceid = SourceEntityArn.split("/")[-1]
                try:
                    Source = describe_analysis(account_id, Sourceid, glue_aws_region)
                    SourceName = Source['Analysis']['Name']
                except botocore.exceptions.ClientError as error:
                    if error.response['Error']['Code'] == 'ResourceNotFoundException':
                        print("Analysis ID: " + Sourceid + " not found/does not exist in your account. So, not able to retrieve the Source ID and Source Name.")
                        Sourceid = 'N/A'
                        SourceName = 'N/A'
                    else:
                        raise error
            else:
                print("Source Type is not in analysis. So, not able to retrieve the Source ID and Source Name.")
                Sourceid = 'N/A'
                SourceName = 'N/A'
        else:
            print("SourceEntityArn does not exists in Dashboard: " + Name +". So, not able to retrieve the Source ID and Source Name.")
            Sourceid = 'N/A'
            SourceName = 'N/A'

        DataSetArns = Dashboard['Version']['DataSetArns']
        for ds in DataSetArns:
            dsid = ds.split("/")
            dsid = dsid[-1]
            try:
                dataset = describe_data_set(account_id, dsid, glue_aws_region)
                dsname = dataset['DataSet']['Name']
                LastUpdatedTime = dataset['DataSet']['LastUpdatedTime']
                PhysicalTableMap = dataset['DataSet']['PhysicalTableMap']
                for sql in PhysicalTableMap:
                    sql = PhysicalTableMap[sql]
                    if 'RelationalTable' in sql:
                        DataSourceArn = sql['RelationalTable']['DataSourceArn']
                        DataSourceid = DataSourceArn.split("/")
                        DataSourceid = DataSourceid[-1]
                        try:
                            datasource = describe_data_source(account_id, DataSourceid, glue_aws_region)
                            datasourcename = datasource['DataSource']['Name']
                        except botocore.exceptions.ClientError as error:
                            if error.response['Error']['Code'] == 'ResourceNotFoundException':
                                print(f"Data source ID: " + DataSourceid + " not found/does not exist in your account. Setting datasourcename and DataSourceid to 'N/A'.")
                                DataSourceid = 'N/A'
                                datasourcename = 'N/A'
                            else:
                                raise error
                        if 'Catalog' in sql['RelationalTable']:
                            Catalog = sql['RelationalTable']['Catalog']
                        else:
                            Catalog = 'N/A'

                        if 'Schema' in sql['RelationalTable']:
                            Schema = sql['RelationalTable']['Schema']
                        else:
                            Schema = 'N/A'
                        #Schema = sql['RelationalTable']['Schema']

                        if 'Name' in sql['RelationalTable']:
                            Name = sql['RelationalTable']['Name']
                        else:
                            Name = 'N/A'

                        #sqlName = sql['RelationalTable']['Name']

                        access.append(
                            [glue_aws_region, Name, dashboardid, SourceName, Sourceid, dsname, dsid, LastUpdatedTime,
                             datasourcename, DataSourceid, Catalog, Schema, sqlName])

                    if 'CustomSql' in sql:
                        DataSourceArn = sql['CustomSql']['DataSourceArn']
                        DataSourceid = DataSourceArn.split("/")
                        DataSourceid = DataSourceid[-1]
                        try:
                            datasource = describe_data_source(account_id, DataSourceid, glue_aws_region)
                            datasourcename = datasource['DataSource']['Name']
                        except botocore.exceptions.ClientError as error:
                            if error.response['Error']['Code'] == 'ResourceNotFoundException':
                                print(f"Data source ID: " + DataSourceid + " not found/does not exist in your account. Setting datasourcename and DataSourceid to 'N/A'.")
                                DataSourceid = 'N/A'
                                datasourcename = 'N/A'
                            else:
                                raise error                        
                        SqlQuery = sql['CustomSql']['SqlQuery'].replace("\n", "").replace("\r", "").replace("\t", "")
                        sqlName = sql['CustomSql']['Name']

                        access.append(
                            [glue_aws_region, Name, dashboardid, SourceName, Sourceid, dsname, dsid, LastUpdatedTime,
                             datasourcename, DataSourceid, 'N/A', sqlName, SqlQuery])

            except botocore.exceptions.ClientError as error:
                if error.response['Error']['Code'] == 'ResourceNotFoundException':
                    print(f"Dataset ID: " + dsid + " not found/does not exist in your account. Skipping this dataset.")
                    continue     

            except Exception as e:
                if (str(e).find('flat file') != -1):
                    pass
                else:
                    raise e


    with open(path, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='|')
        for line in access:
            writer.writerow(line)
    outfile.close()
    # upload file from tmp to s3 key

    bucket.upload_file(path, key)

    datasets = list_datasets(account_id, glue_aws_region)
    for item in datasets:
        try:
            dsid = item['DataSetId']
            datasetname = item['Name']
            dataset_details = describe_data_set(account_id, dsid, glue_aws_region)
            OutputColumns = dataset_details['DataSet']['OutputColumns']
            for column in OutputColumns:
                columnname = column['Name']
                columntype = column['Type']
                if 'Description' in column.keys():
                    columndesc = column['Description']
                else:
                    columndesc = None
                data_dictionary.append(
                    [datasetname, dsid, columnname, columntype, columndesc]
                )
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"Dataset ID: " + dsid + " not found/does not exist in your account. Skipping this dataset.")
                continue
        
        except Exception as e:
            if (str(e).find('data set type is not supported') != -1):
                pass
            else:
                raise e

    print(data_dictionary)
    with open(path3, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        for line in data_dictionary:
            writer.writerow(line)
    outfile.close()
    # upload file from tmp to s3 key
    bucket.upload_file(path3, key3)
