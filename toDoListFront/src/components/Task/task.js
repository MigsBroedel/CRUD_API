import "./task.css"

// Concertar bug do value, não printa na tarefa
// pelo jeito, o value esta sendo interpretado como um objeto em algum momento, por isso, não o le como string
// talvez seja na parte de captação de um input html pra um js
function Task ({ value }) {
    return (
        <div>
        <div className="divgeral">
            <div  className="container"> 
               
                <p className="nome">{value}</p>
            </div>
            <div className="checkbox">
              <input type="checkbox"></input>
            </div>
        </div>
        </div>)
}

export default Task;