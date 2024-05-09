const app = require("./server")
const pool = require("./dbconnection")



/* Notas sobre o funcionamento do sistema:
   
*/

// get all
app.get("/", async (req, res) => {
    try {
        const dados = await pool.query("SELECT * FROM exemplo")
        return res.status(200).send(dados.rows)}
    catch(err) {
        return res.status(400).send(err)
    }
})

// get by id
app.get("/:id", async (req, res) => { // get com defeito
    const id = req.params.id
    try {
        const achado = await pool.query("SELECT * FROM exemplo WHERE gameid = $1", [parseInt(id)])
        if (achado.rowCount == 0) {
            return res.status(400).send("O id não é compativel")
        }
        else{
        return res.status(200).send(achado.rows)}}
    catch(err) {
        console.log(err.message)
        return res.status(400).send(err)
        
    }
})


// post
app.post("/", async (req, res) => {
    try{
    const titulo  = req.body.titulo
    const responsavel = req.body.responsavel
    const newgame = await pool.query("INSERT INTO exemplo (titulo, responsavel) VALUES($1, $2) RETURNING *", [titulo, responsavel])
    return res.status(201).send(newgame.rows)}

    catch(err) {
        console.log(typeof titulo)
        console.log(titulo[0])
        console.log(err.message)
        console.log(err)
        return res.status(400).send(err)

    }
})

// update/patch
app.patch("/:id", async (req, res) => {
    try {
        const gameid = req.params.id
        const updatedti = req.body.titulo
        const updatedre = req.body.responsavel
        const dados = await pool.query("SELECT * FROM exemplo WHERE gameid = $1", [gameid])
        if(dados.rows.titulo == updatedti || dados.rows.responsavel == updatedre) {
            const updatedquery = await pool.query("UPDATE exemplo SET titulo = $1 WHERE gameid = $2 RETURNING *", [updatedti, gameid])
            return res.status(200).send(updatedquery.rows)}


            else {
                if(dados.rows.responsavel == updatedre) {
                    const updatedquery = await pool.query("UPDATE exemplo SET responsavel = $1 WHERE gameid = $2 RETURNING *", [updatedre, gameid])
                    return res.status(200).send(updatedquery.rows)
                }
                else {
                const updatedquery = await pool.query("UPDATE exemplo SET titulo = $1, responsavel = $2 WHERE gameid = $3 RETURNING *", [updatedti, updatedre, gameid])
                return res.status(200).send(updatedquery.rows)}}
    }
    catch (err) {
        console.log(err.message)
        return res.status(400).send(err)

    }
})

// delete
app.delete("/:id", async (req, res) => {
    try {
        const gameid = req.params.id
        await pool.query("DELETE FROM exemplo WHERE gameid = $1 RETURNING *", [gameid])
        return res.status(200).send("Linha deletada com sucesso")
    }
    catch (err) {
        console.log(err.message)
        return res.status(400).send(err)

    }
})



