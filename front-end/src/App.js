import React from 'react';
import './App.css';
import TableItem from './TableItem.js';
import Warnings from './Warnings.js';

//  Main component. Contains a controlled state form containing a table of TableItems
class App extends React.Component {

    //  Courses is a list of 8 lists, each with (currently) empty classes, which are strings
    constructor(props) {
        super(props);
        this.state = {
            courses: (new Array(8)).fill(new Array(10).fill("")),
            enough_credits: "",
            lower_level_math: "",
            lower_level_cs: "",
            upper_level: "",
            general_track: "",
            gened: "",
        }
    }
    
    //  The loops generate the table rows and columns. The TableItem name prop is a string identifier formatted as two integers
    //  separated by a space. The first integer is the semester/column, and the second is the slot/row. Both are 0 indexed.
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
            <div className="main-container">
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
                    <input id="submit" type="submit" value="Check Schedule"/> 
                </form>
                <Warnings enough_credits={this.state.enough_credits} 
                    lower_level_math={this.state.lower_level_math} lower_level_cs={this.state.lower_level_cs}
                    upper_level={this.state.upper_level} general_track={this.state.general_track}
                    gened={this.state.gened}/>
            </div>
        );
    }

    //  Submit the form, then do something with the data
    handleSubmit = async (event) => {
        event.preventDefault();
        let json = await this.runScheduleCheck();
        console.log(json);
        this.setState(json);
    }

    //  This method actually submits a post request to the back end with the table data (gathered from the this.state.courses)
    runScheduleCheck = async () => {
        console.log(JSON.stringify(this.state.courses));
        let data = await fetch ("/run_schedule", {
            method: "POST",
            body: JSON.stringify(this.state.courses),
        }).then(res => res.json())
        return data;
    }

    //  This method searches for the courses. It will receive at most 3
    findClasses = async (letters) => {
        let data = await fetch ("/search_courses?letters="+letters)
            .then(res => res.json())
        return data;
    }

    //  This method is used to control the form. It keeps the state of all the inputs in this.state.courses.
    //  Slot will come as as a string containing two integers separated by a space like so: "2 9". Where 
    //  2 would represent the third semester , and 9 would represent the tenth slot 
    updateCourses = (course_id, slot) => {
        let temp = this.state.courses;
        let semester, space;
        [semester, space] = slot.split(" ")
        temp[semester][space] = course_id;
        this.setState({courses: temp})
    }
}

export default App;
