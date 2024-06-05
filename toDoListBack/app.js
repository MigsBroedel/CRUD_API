const app = require("./server.js")
const pool = require("./dbconnect.js")


/* Anotaçoes sobre o projeto
A ideia é fazer um sistema de usuario, que dependa de incluir seu proprio id no body da req, para executar ações como get, delete, post etc
   sobre os metodos, é legal organizar numa classe separada, para poder chamar no front mais facil, como exemplo um patch para atualizar e um patch para done = true
*/

//USER METODS

app.get("/users", async (req, res) => {
    try {
        const data = await pool.query("SELECT * FROM users")
        
        return res.status(200).send(data.rows)
    }
    catch(err) {
        console.log(err.message)
        return res.status(404).send(err)
    }

})


// TASK METODS
app.get("/tasks/:id", async (req, res) => {
    const id = req.params.id
    try {
        const data = await pool.query("SELECT * FROM tasks WHERE userid = $1", [id])
        return res.status(200).send(data.rows)
    }
    catch(err) {
        console.log(err.message)
        return res.status(404).send(err)

    }
})

app.get("/tasks/:id/:taskid", async (req, res) => {
    const userid = req.params.id
    const taskid = req.params.taskid
    try {
        const data = await pool.query("SELECT * FROM tasks WHERE userid = $1 AND taskid = $2", [userid, taskid])
        return res.status(200).send(data.rows)
    }
    catch(err) {
        console.log(err.message)
        return res.status(404).send(err)

    }
})


app.post("/tasks/:id", async (req, res) => {
    const userid = req.params.id
    try {
        const newtask = req.body
        const done = false
        const newtaskdata = await pool.query("INSERT INTO tasks(taskname, taskdescrip, done, userid) VALUES ($1, $2, $3, $4) RETURNING * ", [newtask.taskname, newtask.taskdescrip, done, userid ])
        return res.status(201).send(newtaskdata.rows)
    }
    catch (err) {
        console.log(err.message)
        return res.status(500).send(err)
    }
})

app.patch("/tasksdone/:id/:taskid", async (req, res) => { // PATCH apenas para mudar o feito
    const userid = req.params.id
    const taskid = req.params.taskid
    try {
        const done = await pool.query("SELECT done FROM tasks WHERE userid = $1 AND taskid = $2", [userid, taskid])
        const donemu = await pool.query("UPDATE tasks SET done = NOT $3 WHERE userid = $1 AND taskid = $2", [userid, taskid, done])
        return res.status(201).send("Feito!")
    }
    catch(err) {
        console.log(err.message)
        return res.status(500).send(err)
    }
})

app.patch("/tasks/:id/:taskid", async (req, res) => { // PATCH para mudar nome e desc //// erro
    const userid = req.params.id
    const taskid = req.params.taskid
    const info = req.body
    try {
        if (typeof info.taskname !== undefined && typeof info.descrip !== undefined) {
            const newtask = pool.query("UPDATE tasks SET taskname = $1 AND taskdescrip = $2 WHERE userid = $3 AND taskid = $4 RETURNING *", [info.taskname, info.taskdescrip, userid, taskid])
        }
        if (typeof info.taskname === undefined) 
            {try {
            const newtask = pool.query("UPDATE tasks SET taskdescrip = $1 WHERE userid = $2 AND taskid = $3 RETURNING *", [info.taskdescrip, userid, taskid] )
            return res.status(201).send(newtask.rows)
        }
        catch (err) {
            console.log(err)}}
        else {
            if (typeof info.descrip === undefined)
                try {
                const newtask = pool.query("UPDATE tasks SET taskname = $1 WHERE userid = $2 AND taskid = $3 RETURNING *", [info.taskname, userid, taskid] )
                return res.status(201).send(newtask.rows)
            }
            catch(err){
                console.log(err)
                
            }
        } 
    }
    catch(err) {
        console.log(err.message)
        return res.status(500).send(err)
    }
})