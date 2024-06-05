const Express = require("express")

const app = Express()

app.use(Express.json())

app.listen(8000, () => {
    console.log("ouvindo porta 8000")
})

module.exports = app