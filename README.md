# EVM Chain ETL Table Definitions

This repo contains table definitions for certain EVM compatible blockchains.

If you want to parse certain events on these blockchains and make them cheaper to query on [BigQuery](https://cloud.google.com/bigquery), feel free to submit a PR with your new table definitions.

## What

All EVM chains have smart contracts that broadcast events and also contain functions.

These events and functions can tell us useful information. An example of a common event is the Transfer event broadcasted by an ERC20 token, when a token is successfully transferred from one wallet to another.

EVM chain etl aims to parse these events and build a big query table with just the events of interest.

## Why

To make it super efficient to query the data you are looking for instead of having to go through all logs (super expensive to query, also takes a lot of time)

## How To Submit New Table Definitions

1. Fork this repository
2. Use [ABI PARSER](https://nansen-contract-parser-prod.web.app/) to get the table defenition json files for the contract of your interest
3. Create a new branch and upload your new files to this branch
4. Create a PR to merge to this main repository
5. Make sure the `pyTest / Validate Json Files in parse Directory (pull_request)` Github Action runs Successfuly, if not you may need to fix your json files.
6. Wait for it to be reviewed and merged, your BigQuery tables should show up shortly under the \_\_ project.
7. Now you can query your newly parsed tables more efficiently and for a smaller cost.


## Debugging Table Defenition Files

A utility script for debugging and verifying contract parsing in EVM chains data processing pipelines is available. You can simply run 

```
python3 generate_parse_sql.py <path_to_table_definition_file> <date>
```

This will output some example SQL that can be used to debug if the generated json files from the contract parser are correct. 

NOTE: certain files may not have the `contract_address` field specified as a valid address [AToken_v3_event_Approval](parse/table_definitions_arbitrum/aave/AToken_v3_event_Approval.json) but use a select statement on another table instead. For these you can simply pass the contract address yourself like below:

```
python3 generate_parse_sql.py <path_to_table_definition_file> <date> --contract_address <contract_address>
```

## My Dataset doesn't show up?

Certain datasets are currently private while others are public.
If your blockchain is considered private, please sign up for a Nansen Query Plan with your google cloud account.
You will then be able to access theses private datasets.

## Public vs Private

### Public

- celo

### Private

- bsc
- ronin
- arbitrum
- fantom
