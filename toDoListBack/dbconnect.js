require("dotenv").config()
const { Pool } = require("pg")

const pool = new Pool ({
    connectionString: process.env.POSTGRE_URL
})

pool.connect().then(() => {
    console.log("Conectado a db")
}) 

module.exports = pool