# Roe Markets

The project is a fork of Aave V2 Lending Markets.

The Aave V2 Lending Market protocol is a battle-tested lending market protocol, with over 10B locked over a few years.

We will follow Aave V2 at a snapshot of their development ([https://github.com/aave/protocol-v2/releases/tag/Deployment%23001](https://github.com/aave/protocol-v2/releases/tag/Deployment%23001)  - Aave Avax Deployment).

If any critical bugs are raised in the Aave Deployment, the protocol will strive to immediately pause and upgrade in accordance to the Aave V2 bugfix.

# Main changes
Only the LendingPool file itself has been changed; a quick visual diff of the original versus the Roe Markets' can be found here: https://www.diffchecker.com/WadsbSwH

We can break down the main changes into the following: 
1. Adding of the role of a PositionManager, which must be a contract: L61, L426-L493
2. Making the PositionManager not enable collateral usage by default on transfer to save gas: L132
3. Flashloan fees were reduced to 0: L98

# Code Safety Considerations
## For depositors
Roe Markets primarily aim to help liquidity pool depositors earn extra supply yield with minimal additional technical risk. This is achieved by ensuring minimal changes to battle-tested code, and to ensure the new code added cannot be wielded to remove depositor's money.

PositionManagers have the flexibility to transfer ATokens to themselves; this is needed to help the user manage their positions. 

The added code has checks that protect users assets, as long as a user does not:
1) Initiate a call to any PositionManager, and only interact through the Lending Pool Proxy (listed below in Deployment)
2) Reduce their health factor to near liquidation (< 1.02) by borrowing,

Roe Markets borrowers will always need to be sufficiently overcollateralised to keep their positions. However there is a possibility that in averse market conditions, the lending protocol may take on bad debt when the value of the borrowers' assets do not sufficiently cover the debt. This may lead to a haircut to all depositors.

## For borrowers
The code base of PositionManagers will be separately audited, to ensure that the code flow doesn't compromise the borrowers' funds unexpectedly.

## For all users
As the logic of the Lending Market can be upgraded, it is imperative that users verify every update to the logic, as what was previously safe could be updated to include code that may be unsafe for the users' assets.

To allow users time to react, the PoolAdmin is gated behind a timelock (https://etherscan.io/address/0xA10feBCE203086d7A0f6E9A2FA46268Bec7E199F), which is verified and requires a minimum delay of 2 days. 

Users may read more details here (https://www.certik.com/resources/blog/Timelock) about timelocks, and also how to monitor changes to timelocks so that any unexpected changes can raise alerts to react upon.

# Deployment 
## Mainnet

### Lending Pool Proxy  (depositors should check they only interact with this address)
|Markets | Address |
|--|--|
|WETH/USDC|0xD14a7c302051A0F1e9cE8e9a8C4845a45F41B46f
|WBTC/USDC|0x5F360c6b7B25DfBfA4F10039ea0F7ecfB9B02E60
|FXS/FRAX|0x01b69EB0393006E56a372B23524F7AD5Db7f2166|

### Lending Market Base Code from Aave Deployment 001, and should match completely

|Code  | Address |
|--|--|
|LendingPoolAddressesProviderRegistry  |0x0029B254d039d8C5C88512a44EAa6FF999296009  |
|AToken | 0x78b787C1533Acfb84b8C76B7e5CFdfe80231Ea2D |
|VariableDebtToken | 0xB19Dd5DAD35af36CF2D80D1A9060f1949b11fCb0|
|StableDebtToken | 0x8B6Ab2f071b27AC1eEbFfA973D957A767b15b2DB |
|InterestRateStrategy| 0xfAdB757A7BC3031285417d7114EFD58598E21d79 |
| AaveOracle | 0x8A4236F5eF6158546C34Bd7BC2908B8106Ab1Ea1 |
| WalletBalanceProvider | 0xCb61F16f37b3c7d70e736A62bB8529074b23326c |
| ReserveLogic | 0xE61cC7482db2cd6dF02423BBCbc797526D03Dd12 |
| GenericLogic.deploy | 0x8beb832bb307179Bb2bA06Fc87e9bdd08E4eE60b
| ValidationLogic | 0x553eBA010DDBB75C39311b8083C33529ad3825f4
| LendingPoolCollateralManager |0xcb57103e8a568BDA8826846Ab8B280C754441304
| LendingPoolConfigurator | 0x751aAdF96CA9427514dd816A227881E5B6cE87ce
| WETHGateway | 0x9B6E954207FF1E5d6C791C99E22D5e8D170361cc
| LendingRateOracle	| 0x090E950666D3F2c5cf7fc98135D94287c83E0a85

### The following files have changes made to them:

| Code | Address | Diff with base code|
| -- | -- | -- |
| LendingPool | 0x59A51F4f3ECe3D24A5EaE424ebcFB7551af411b4 | https://www.diffchecker.com/WadsbSwH


### Key Addresses  to monitor
| Contract Type | Address |
| -- |--|
| Timelock | 0xA10feBCE203086d7A0f6E9A2FA46268Bec7E199F |


# Code Verification
All contracts are verified on Blockscan where possible; the team is working to ensure all files are verified, but currently the following files are unverifiable: GenericLogic, ReserveLogic, LendingPool, InitializableImmutableAdminUpgradeabilityProxy
