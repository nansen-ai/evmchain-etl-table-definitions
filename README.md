# EVM Chain ETL Table Definitions

This repo contains table definitions for certain EVM compatible blockchains.

If you want to parse certain events on these blockchains and make them cheaper to query on BigQuery, feel free to submit a PR with your new table definitions. 
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
5. Wait for it to be reviewed and merged, your BigQuery tables should show up shortly under the __ project. 
6. Now you can query your newly parsed tables more efficiently and for a smaller cost. 


## My Dataset doesn't show up? 

Certain datasets are currently private while others are public. If your blockchain is considered private, please sign up for a Nansen Developer Plan with your google cloud account. You will then be able to access theses private datasets. 

## Public vs Private 

### Public

- fantom 
- celo 

### Private

- bsc
- ronin 
- arbitrum 
