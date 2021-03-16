import React from 'react';
import './App.css';
import TableItem from './TableItem.js';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {courses: [], coursesLoaded: false}
    }

    componentDidMount() {
        fetch("https://api.umd.io/v1/courses?semester=202008")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({courses: result, coursesLoaded: true});
                }
            )
    }
  
    render () {
        console.log(this.state.courses)
        var table = []
        var tr = []
        for (let i = 0; i < 10; i++) {
            tr = []
            for (let j = 0; j < 8; j++) {
                tr.push(<TableItem findClasses={this.findClasses}/>)
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

    findClasses = (letters) => {
        let re = new RegExp("^" + letters)
        console.log(re.toString())
        let temp = this.state.courses.filter((course) => re.test(course["course_id"]))
        console.log(temp);
        return temp.length <= 3 ? temp : temp.slice(3);
    }
}

export default App;
