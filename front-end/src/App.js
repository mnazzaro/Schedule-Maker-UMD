import './App.css';
import TableItem from './TableItem.js';

function App() {
  var table = []
  var tr = []
  for (let i = 0; i < 10; i++) {
    tr = []
    for (let j = 0; j < 8; j++) {
      tr.push(<TableItem/>)
    }
    table.push(<tr>{tr}</tr>)
  }
  return (
    <table>
      <tr>
        <th>Fall Semester 1</th>
        <th>Spring Semester 1</th>
        <th>Fall Semester 2</th>
        <th>Spring Semester 2</th>
        <th>Fall Semester 3</th>
        <th>Spring Semester 3</th>
        <th>Fall Semester 4</th>
        <th>Spring Semester 4</th>
      </tr>
      {table}
    </table>
  );
}

export default App;
