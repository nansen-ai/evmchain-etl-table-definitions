-- MIT License
-- Copyright (c) 2020 Balancer Labs, markus@balancer.finance

-- Transfers of Liquidity Mining Power
-- On Arbitrum, Liquidity Mining Power is derived from V2 BPTs plus:
--   1. Vesta's staking contract

select 
  contract_address as token_address,
  `from` as from_address,
  `to` as to_address,
  value,
  block_number,
  block_timestamp
FROM `blockchain-etl.arbitrum_balancer.V2_BalancerPoolToken_event_Transfer`

union all

-- Vesta's staking contract deposits
-- are handled as transfers back to the user
-- so that the token transfer and the deposit cancel each other out
select
  '0xc61ff48f94d801c1ceface0289085197b5ec44f0' as token_address,
  '0x65207da01293c692a37f59d1d9b1624f0f21177c' as from_address,
  user as to_address,
  amount as value,
  block_number,
  block_timestamp
FROM `blockchain-etl.arbitrum_vesta_finance.VestaFarming_event_Staked` 

union all

-- Vesta's staking contract withdrawals
-- are handled as transfers back to the staking contract
-- so that the token transfer and the withdraw cancel each other out
select
  '0xc61ff48f94d801c1ceface0289085197b5ec44f0' as token_address,
  user as from_address,
  '0x65207da01293c692a37f59d1d9b1624f0f21177c' as to_address,
  amount as value,
  block_number,
  block_timestamp
FROM `blockchain-etl.arbitrum_vesta_finance.VestaFarming_event_Withdrawn`