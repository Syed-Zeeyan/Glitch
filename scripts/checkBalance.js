require("dotenv").config();
const { ethers } = require("hardhat");

async function main() {
  const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
  const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider); // ✅ uses env
  const balance = await provider.getBalance(wallet.address);
  const ethBalance = ethers.formatEther(balance);

  console.log("🧾 Wallet Address:", wallet.address);
  console.log("💰 Balance:", ethBalance, "ETH");
}

main().catch((error) => {
  console.error("❌ Error:", error);
  process.exitCode = 1;
});
