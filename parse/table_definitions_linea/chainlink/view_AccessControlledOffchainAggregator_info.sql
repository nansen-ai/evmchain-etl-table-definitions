SELECT * FROM UNNEST([STRUCT('0x462f8eea5cf35df6a7df89c12107262bf134b380' as contract_address, 8 as decimals, '0x09b0a8afd9185500d7c64fc68338b4c50db6df1d' as proxy_address, 'AAVE / USD' as description, 4 as version),
STRUCT('0x854d46002b2524239b81ef783ab47cabd5b9ad4e' as contract_address, 8 as decimals, '0x28606f10277cc2e99e57ae2c55d26860e13a1bbd' as proxy_address, 'ARB / USD' as description, 4 as version),
STRUCT('0xd71cd2e38b7f65421bb59a872cca021e685647cc' as contract_address, 8 as decimals, '0x7a99092816c8bd5ec8ba229e3a6e6da1e628e1f9' as proxy_address, 'BTC / USD' as description, 4 as version),
STRUCT('0xe6ebca31b844175bf4d8d19685982d1d5b535093' as contract_address, 8 as decimals, '0x5133d67c38afbdd02997c14abd8d83676b4e309a' as proxy_address, 'DAI / USD' as description, 4 as version),
STRUCT('0x0635163285c6ef5692167f18b799fb339df064f8' as contract_address, 8 as decimals, '0x3c6cd9cc7c7a4c2cf5a82734cd249d7d593354da' as proxy_address, 'ETH / USD' as description, 4 as version),
STRUCT('0xda7ed0f2df6af4efc3539d91d47fa7d7ce32ee2a' as contract_address, 8 as decimals, '0x637cf12017219dd3a758818ed63185f7acf7d935' as proxy_address, 'EURO / USD' as description, 4 as version),
STRUCT('0x11c47ec06f771d0e3bb148301b416d79ea04cdf0' as contract_address, 8 as decimals, '0x8df01c2efed1404872b54a69f40a57fec1545998' as proxy_address, 'LINK / USD' as description, 4 as version),
STRUCT('0xfcc63cd02a9c763a6f0f91260c1d8b8bcd263fbe' as contract_address, 8 as decimals, '0x9ce4473b42a639d010ed741df3ca829e6e480803' as proxy_address, 'MATIC / USD' as description, 4 as version),
STRUCT('0xa6f72813b20758f08923b48926df1ba54782f9ff' as contract_address, 8 as decimals, '0xaadaa473c1bdf7317ec07c915680af29debfdcb5' as proxy_address, 'USDC / USD' as description, 4 as version),
STRUCT('0xa901c5741fad401dff8a750218aeb72527f86ed3' as contract_address, 8 as decimals, '0xaadaa473c1bdf7317ec07c915680af29debfdcb5' as proxy_address, 'USDT / USD' as description, 4 as version),
STRUCT('0x1bd1d8f94111ca0666fa58c9f3a271ad79512ba6' as contract_address, 8 as decimals, '0x8ece1aba32716fdde8d6482bfd88e9a0ee01f565' as proxy_address, 'wstETH / USD' as description, 4 as version)
])
