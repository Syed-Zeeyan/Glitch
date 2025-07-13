require("dotenv").config();
const { ethers } = require("hardhat");

async function main() {
  const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
  const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider); // ✅ Connect wallet

  const LoanAgent = await ethers.getContractFactory("LoanAgent", wallet); // ✅ Use your wallet
  const loan = await LoanAgent.deploy();

  await loan.waitForDeployment(); // ✅ Modern ethers syntax
  console.log("✅ LoanAgent deployed to:", await loan.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
