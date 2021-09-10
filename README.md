# EVM Chain ETL Table Definitions

This repo contains table definitions for certain EVM compatible blockchains.

If you want to parse certain events on these blockchains and make them cheaper to query on BigQuery, feel free to submit a PR with your new table definitions. 

# How To Submit New Table Definitions 

1. Fork this repository 
2. Use [ABI PARSER](https://nansen-contract-parser-prod.web.app/) to get the table defenition json files for the contract of your interest 
3. Create a new branch and upload your new files to this branch
4. Create a PR to merge to this main repository
5. Wait for it to be reviewed and merged, your BigQuery tables should show up shortly under the __ project. 
6. Now you can query your newly parsed tables more efficiently and for a smaller cost. 


