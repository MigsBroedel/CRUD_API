const Express = require("express")

const app = Express()
app.use(Express.json())

app.listen(3333, () => {
    console.log("server up")
})

module.exports = app