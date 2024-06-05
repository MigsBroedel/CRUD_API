
import Header from "./components/header/header.js"
import Input from "./components/input/input.js";
import { useState } from "react";
//import Task from "./components/Task/task.js";


// Proximo passo: refinar o codigo e funcionalidades, para onde vai as tarefas concluidas, api integrada, e verificações, além de melhorar o site em si, como fontes


function App() {
  let [value, setValue] = useState("") // setando o use state para o valor da task, a string, nome
  let [tasks, setTask] = useState([]) // setando o array de tasks

  const setValueInput = (e) => { // função que, pega o evento, pega o valor e faz um setvalue com ela
      setValue(e.target.value);
      console.log("evento: ", e.target.value)
  }

  const addTask = () => { // evento que verifica se value1 é vazia, e coloca num array diferente, tasks, depois, defini de volta o value para vazio
      if (value !== "" || value !== "  ") {
          console.log("valuebi = ", value)
          setTask((tasks) => [...tasks, value])
          console.log("Add task", tasks)
          setValue("")
      }
      else {
          console.log("Espaço em branco")
      }
  }

  return (
    
    <body color='#eeeeee'>
      <Header/>
      <Input tasks={tasks} value ={value} addTask={addTask} setValueInput={setValueInput}/>
      
    </body>)}

export default App;
