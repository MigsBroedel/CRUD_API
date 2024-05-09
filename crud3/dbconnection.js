const { Pool } = require("pg")
require('dotenv').config()

const pool = new Pool ({
    connectionString: process.env.POSTGRES_LINK
})

pool.connect().then(() => {
    console.log("db conectado")
})

module.exports = pool