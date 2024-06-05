
import "./input.css"
import React, { useState } from "react"
import Task from "../Task/task.js"



// usestate -> defini uma variavel e uma função que a altera, passando como parametro o seu estado inicial, toda vez que o set### é chamada, altera o valor da variavel para o passado no parametro
// useEffect -> executa uma função toda vez que uma variavel ou elemento é atualizado

function Input(props) {

    return (
    <div className="divabsolute">
        <div className="divchil">
            <input className="input" value={props.value} onChange={props.setValueInput} placeholder="New Task">
            </input>
            <button onClick={props.addTask} className="add">+</button>
        </div>
        <div className="task-list">
            {props.tasks.map((task, index) => (
                <Task key={index} value={task} /> // o value nao pode ser o value1 pois mudaria o valor de todas as tarefas quando mexesse no input
            ))}
        </div>
    </div>
    )
}



export default Input;