module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",    // Ganache runs here
      port: 7545,            // Ganache default port
      network_id: "*",       // Match any network
    },
  },
  compilers: {
    solc: {
      version: "0.8.21",     // Must match pragma in .sol file
    },
  },
};