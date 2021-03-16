import React from 'react';
import './App.css';
import TableItem from './TableItem.js';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {courses: [], coursesLoaded: false}
    }
    
    render () {
        var table = []
        var tr = []
        for (let i = 0; i < 10; i++) {
            tr = []
            for (let j = 0; j < 8; j++) {
                tr.push(<TableItem findClasses={this.findClasses} key={j}/>)
            }
            table.push(<tr key={i}>{tr}</tr>)
        }
        return (
            <table>
                <tbody>
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
                </tbody>
            </table>
        );
    }

    findClasses = async (letters) => {
        let data = await fetch ("/search_courses?letters="+letters)
            .then(res => res.json())
            .then(res => res["results"])
        return data;
    }
}

export default App;
