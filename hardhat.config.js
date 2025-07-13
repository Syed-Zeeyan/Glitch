require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.20",
  networks: {
    ganache: {
      url: "http://127.0.0.1:8545",
      accounts: [
        "0x41f84dc5ed06eb782e3178ca96cb12e77c4530d153269858071b6f7fcfcd6f86"
      ]
    }
  }
};
