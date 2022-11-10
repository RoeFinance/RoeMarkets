from brownie import *

NULL = "0x0000000000000000000000000000000000000000"
ETH_PLACEHOLDER = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"

lpRegistry      = LendingPoolAddressesProviderRegistry.deploy({"from": a[0]})
lpAddProvider   = LendingPoolAddressesProvider.deploy("Roe Market", {"from": a[0]})
collatManager   = LendingPoolCollateralManager.deploy({"from": a[0]})
reserveLogic    = ReserveLogic.deploy({"from": a[0]})
genericLogic    = GenericLogic.deploy({"from": a[0]})
validationLogic = ValidationLogic.deploy({"from": a[0]})
lendingPool     = LendingPool.deploy({"from": a[0]})
configurator    = LendingPoolConfigurator.deploy({"from": a[0]})
lendingOracle   = LendingRateOracle.deploy({"from": a[0]})

# ETH
"""
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
WETH_USD_LINK = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
USDC_USD_LINK = "0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6"
nativeGateway   = WETHGateway.deploy(WETH, {"from": a[0]})
priceOracle     = AaveOracle.deploy([WETH, USDC], [WETH_USD_LINK, USDC_USD_LINK], NULL, NULL, 1e8, {"from": a[0]})

WBTC = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
WBTC_USD_LINK = "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c"

FRAX = ""
FRAX_USD_LINK = "0xB9E1E3A9feFf48998E45Fa90847ed4D467E8BcfD"

FXS = ""
FXS_USD_LINK = "0x6Ebc52C8C1089be9eB3945C4350B68B8E4C2233f"

TRIBE = ""
TRIBE_ETH_LINK = "0x84a24deCA415Acc0c395872a9e6a63E27D6225c8" # NEED TO DEPLOY CHAINLINK MAPPER TO TRIBE_USD

FEI = "" 
FEI_USD_LINK = 0x31e0a88fecB6eC0a411DBe0e9E76391498296EE9

priceOracle.setAssetsSource([WBTC], [WBTC_USD_LINK], {"from": owner})


"""
# END ETH

# MATIC
LUNA = "0x9cd6746665D9557e1B9a775819625711d0693439"
LUNA_USD_LINK = "0x1248573D9B62AC86a3ca02aBC6Abe6d403Cd1034"
UST = "0xE6469Ba6D2fD6130788E0eA9C0a0515900563b59"
UST_USD_LINK = "0x2D455E55e8Ad3BA965E3e95e7AaB7dF1C671af19"
WMATIC = "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270"
WMATIC_USD_LINK = "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0"
nativeGateway   = WETHGateway.deploy(WMATIC, {"from": a[0]})
priceOracle     = AaveOracle.deploy([LUNA, UST, WMATIC], [LUNA_USD_LINK, UST_USD_LINK, WMATIC_USD_LINK], NULL, NULL, 1e8, {"from": a[0]})
# END MATIC

lpRegistry.registerAddressesProvider(lpAddProvider, 1, {"from": a[0]})
lpAddProvider.setLendingPoolImpl(lendingPool, {"from": a[0]})
lpAddProvider.setLendingPoolCollateralManager(collatManager, {"from": a[0]})
lpAddProvider.setLendingPoolConfiguratorImpl(configurator, {"from": a[0]})
lpAddProvider.setLendingRateOracle(lendingOracle, {"from": a[0]})
lpAddProvider.setPriceOracle(priceOracle, {"from": a[0]})

proxyLendingPool   = LendingPool.at(lpAddProvider.getLendingPool())
proxyCollatMgr     = LendingPoolCollateralManager.at(lpAddProvider.getLendingPoolCollateralManager())
proxyConfigurator  = LendingPoolConfigurator.at(lpAddProvider.getLendingPoolConfigurator())
dataProvider       = AaveProtocolDataProvider.deploy(lpAddProvider, {"from": a[0]})
walletProvider     = WalletBalanceProvider.deploy({"from": a[0]}) 
#TokenDeployer      = ATokensAndRatesHelper.deploy(proxyLendingPool, lpAddProvider, proxyConfigurator, {"from": a[0]})
#DebtDeployer       = StableAndVariableTokensHelper.deploy(proxyLendingPool, lpAddProvider, {"from": a[0]})

aToken = AToken.deploy({"from": a[0]})
varDebt = VariableDebtToken.deploy({"from": a[0]})
stbDebt = StableDebtToken.deploy({"from": a[0]})
interestStrategy = DefaultReserveInterestRateStrategy.deploy(lpAddProvider, 0.8e27, 0,0.10e27,3e27,0.1e27,3e27, {"from": a[0]})


lpAddProvider.setPoolAdmin(a[0], {"from": a[0]})
nativeGateway.authorizeLendingPool(proxyLendingPool, {"from": a[0]}) 

# Setup assets in market

# From Roe,
lpo = LPOracle.deploy("0x6e7a5FAFcec6BB1e78bAE2A1F0B612012BF14827", "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0", "0xfE4A8cc5b5B2366C1B58Bea3858e81843581b2F7", {"from": roeOwner, "priority_fee":30.1e9})

NULL = "0x0000000000000000000000000000000000000000"
WMATIC = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
WMATIC_USDC_QS = "0x6e7a5FAFcec6BB1e78bAE2A1F0B612012BF14827"
WMATIC_CL = "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0"
WMATIC_USDC_QS_CL = "0x7844589F92E342e2f7d8C828FE224F3CcEd23b21"

ao = AaveOracle.at("0xbe4e7883a893189bE8AbE949c1DA4c70462982D3")
priceOracle     = AaveOracle.deploy([WMATIC, WMATIC_USDC_QS], [WMATIC_CL, WMATIC_USDC_QS_CL], NULL, NULL, 1e8, {"from": a[0]})

## Deploy additional Aave Markets with same Addresses Provider Registry (example)
marketMapper = {2: "WBTC-USDC", 3: "FXS-FRAX", 4: "TRIBE-FEI"}
for i in range(2, 5):
    print("Deploying market: " + marketMapper[i])
    lpAddProvider   = LendingPoolAddressesProvider.deploy("Roe Market " + marketMapper[i], {"from": a[0]})
    lpRegistry.registerAddressesProvider(lpAddProvider, i, {"from": a[0]})
    lpAddProvider.setLendingPoolImpl(lendingPool, {"from": a[0]})
    lpAddProvider.setLendingPoolCollateralManager(collatManager, {"from": a[0]})
    lpAddProvider.setLendingPoolConfiguratorImpl(configurator, {"from": a[0]})
    lpAddProvider.setLendingRateOracle(lendingOracle, {"from": a[0]})
    lpAddProvider.setPriceOracle(priceOracle, {"from": a[0]})
    dataProvider = AaveProtocolDataProvider.deploy(lpAddProvider, {"from": a[0]})



def main():
  return


