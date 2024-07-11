import json
import sys
import argparse
from datetime import datetime
from web3 import Web3
import os

# Define BigQuery project and dataset for each chain
CHAIN_BQ_REFS = {
    'unknown': '`notfound.notfond`',
    'bsc': '`nansen-datasets-prod.crypto_bsc_v2`',
    'optimism': '`nansen-datasets-prod.crypto_optimism_v2`',
    'arbitrum': '`nansen-datasets-prod.crypto_arbitrum_v2`',
    'celo': '`nansen-datasets-prod.crypto_celo_v2`',
    'polygon': '`nansen-datasets-prod.crypto_polygon`',
    'arbitrum_nova': '`nansen-datasets-prod.crypto_arbitrum_nova`',
    'chiliz': '`nansen-datasets-prod.crypto_chiliz`',
    'ronin': '`nansen-datasets-prod.crypto_ronin_v2`',
    'avalanche': '`nansen-datasets-prod.crypto_avalanche_v2`',
    'fantom': '`nansen-datasets-prod.crypto_fantom_v2`',
    'base': '`nansen-datasets-prod.crypto_base_v2`',
    'linea': '`nansen-datasets-prod.crypto_linea_v2`',
}

def validate_and_checksum_address(address):
    if address is None:
        return None
    try:
        return Web3.toChecksumAddress(address)
    except ValueError:
        print(f"Error: Invalid contract address: {address}")
        sys.exit(1)

def calculate_signature(abi):
    if isinstance(abi, str):
        abi = json.loads(abi)
    
    if abi['type'] == 'event':
        return Web3.keccak(text=f"{abi['name']}({','.join([input['type'] for input in abi['inputs']])})").hex()
    elif abi['type'] == 'function':
        return Web3.keccak(text=f"{abi['name']}({','.join([input['type'] for input in abi['inputs']])})").hex()[:10]
    else:
        raise ValueError("ABI must be for an event or function")

def determine_chain(json_file_path):
    print(f"Determining chain for {json_file_path}")
    path_parts = json_file_path.split(os.path.sep)
    for part in path_parts:
        if part.startswith('table_definitions_'):
            print(f"Found chain: {part.replace('table_definitions_', '')}")
            return part.replace('table_definitions_', '')
    return 'ethereum'  # Default to ethereum if no match found

def generate_sql_from_json(json_file_path, date, override_contract_address=None):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Determine the chain
    chain = determine_chain(json_file_path)
    bq_ref = CHAIN_BQ_REFS.get(chain, CHAIN_BQ_REFS['unknown'])

    # Use the override_contract_address if provided, otherwise use the one from the JSON file
    contract_address = override_contract_address or data['parser'].get('contract_address')

    # Validate and convert contract address
    if contract_address:
        contract_address = validate_and_checksum_address(contract_address)
        # Update the contract_address in the data
        data['parser']['contract_address'] = contract_address
    else:
        print("Error: No valid contract address provided. Please use --contract_address argument.")
        sys.exit(1)

    json_string = json.dumps(data).replace("'", "''")
    signature = calculate_signature(data['parser']['abi'])
    parser_type = data['parser']['type']

    if parser_type == 'log':
        sql = generate_log_sql(json_string, signature, date, bq_ref)
    elif parser_type == 'trace':
        sql = generate_trace_sql(json_string, signature, date, bq_ref)
    else:
        raise ValueError(f"Unsupported parser type: {parser_type}")

    return sql

def generate_log_sql(json_string, signature, date, bq_ref):
    return f"""
WITH
abi AS 
(
SELECT
    JSON_QUERY(json_data, '$.parser.abi') AS abi,
    JSON_QUERY(json_data, '$.parser.field_mapping') AS field_mapping,
    JSON_QUERY(json_data, '$.table') AS table_details,
    JSON_EXTRACT_SCALAR(json_data, '$.parser.contract_address') AS contract_address,
    CAST(JSON_EXTRACT_SCALAR(json_data, '$.parser.type') AS STRING) AS parser_type
FROM (
    SELECT '{json_string}' AS json_data
)
),

details AS (
    SELECT 
        '{signature}' AS sig,
        abi.*
    FROM abi
),

logs AS (
  SELECT
    l.*,
    a.sig, 
    `blockchain-etl-internal.common.parse_log`(
            l.data,
            l.topics,
            REPLACE(a.abi, "'", '"')
        ) AS parsed_log
  FROM
    {bq_ref}.logs AS l
  INNER JOIN
        details AS a
    ON
        IFNULL(l.topics[SAFE_OFFSET(0)], "") = a.sig
  WHERE
    DATE(l.block_timestamp) = DATE("{date}")
    AND (a.contract_address IS NULL OR l.address = LOWER(a.contract_address))
)

SELECT * FROM logs
LIMIT 100
"""

def generate_trace_sql(json_string, signature, date, bq_ref):
    return f"""
WITH
abi AS 
(
SELECT
    JSON_QUERY(json_data, '$.parser.abi') AS abi,
    JSON_QUERY(json_data, '$.parser.field_mapping') AS field_mapping,
    JSON_QUERY(json_data, '$.table') AS table_details,
    JSON_EXTRACT_SCALAR(json_data, '$.parser.contract_address') AS contract_address,
    CAST(JSON_EXTRACT_SCALAR(json_data, '$.parser.type') AS STRING) AS parser_type
FROM (
    SELECT '{json_string}' AS json_data
)
),

details AS (
    SELECT 
        '{signature}' AS sig,
        abi.*
    FROM abi
),

traces AS (
  SELECT
    t.*,
    a.sig, 
    `blockchain-etl-internal.common.parse_trace`(
            t.input,
            REPLACE(a.abi, "'", '"')
        ) AS parsed_trace
  FROM
    {bq_ref}.traces AS t
  INNER JOIN
        details AS a
    ON
        STARTS_WITH(t.input, a.sig)
  WHERE
    DATE(t.block_timestamp) = DATE("{date}")
    AND (a.contract_address IS NULL OR t.to_address = LOWER(a.contract_address))
    AND t.status = 1  -- Only successful calls
    AND t.call_type = 'call'  -- Only direct calls
)

SELECT * FROM traces
LIMIT 100
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SQL from JSON file")
    parser.add_argument("json_file_path", help="Path to the JSON file")
    parser.add_argument("date", help="Date in YYYY-MM-DD format")
    parser.add_argument("--contract_address", help="Override contract address")
    
    args = parser.parse_args()

    try:
        # Validate the date format
        datetime.strptime(args.date, '%Y-%m-%d')
    except ValueError:
        print("Error: Date should be in the format YYYY-MM-DD")
        sys.exit(1)

    sql = generate_sql_from_json(args.json_file_path, args.date, args.contract_address)
    print(sql)