import React from 'react';
import './App.css';
import TableItem from './TableItem.js';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {courses: (new Array(8)).fill(new Array(10).fill(""))}
    }
    
    render () {
        var table = []
        var tr = []
        for (let i = 0; i < 10; i++) {
            tr = []
            for (let j = 0; j < 8; j++) {
                tr.push(<TableItem findClasses={this.findClasses} name={j + " " + i} key={j + " " + i} update={this.updateCourses}/>)
            }
            table.push(<tr key={i}>{tr}</tr>)
        }
        return (
            <form onSubmit={this.handleSubmit}>
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
                <input type="submit" value="Check Schedule"/> 
            </form>
        );
    }

    handleSubmit = async (event) => {
        event.preventDefault();
        let json = await this.runScheduleCheck();
        console.log(json);
    }

    runScheduleCheck = async () => {
        console.log(JSON.stringify(this.state.courses));
        let data = await fetch ("/run_schedule", {
            method: "POST",
            body: JSON.stringify(this.state.courses),
        }).then(res => res.json())
        return data;
    }

    findClasses = async (letters) => {
        let data = await fetch ("/search_courses?letters="+letters)
            .then(res => res.json())
        return data;
    }

    //  Slot will come as as a string containing two integers separated by a space like so: "2 9". 
    //  Where 2 would represent the third semester , and 9 would represent the tenth slot 
    updateCourses = (course_id, slot) => {
        let temp = this.state.courses;
        let semester, space;
        [semester, space] = slot.split(" ")
        temp[semester][space] = course_id;
        this.setState({courses: temp})
    }
}

export default App;
