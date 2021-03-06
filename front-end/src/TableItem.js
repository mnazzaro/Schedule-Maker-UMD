import React from 'react'

//  This Component is basically a <td> containing a text input and a drop down (which is decides whether to show or hide)
class TableItem extends React.Component {

    constructor (props) {
        super(props)
        this.state = {active: false, classes: [], value: ""}
        this.textRef = React.createRef();
    }

    //  The ternary operators in the className section serve to show or hide elements. The ones in the innerText 
    //  basically just null check to make sure there are classes. The data comes in the form of a list of tuples
    render () {
        return (
            <td>
                <div className="dropdown">
                    <input name={this.props.name} ref={this.textRef} value={this.state.value} onChange={this.handleChange} onKeyUp={this.dropdownOn} onBlur={this.dropdownOff} height="100%"/>
                    <div className={this.state.active && this.state.classes.length > 0 ? "show dropdown-content" : "dropdown-content"}>
                        <div className="dropdown-item" onMouseDown={this.setText}>{this.state.classes.length > 0 ? `${this.state.classes[0][0]} (${this.state.classes[0][1]})`  : ""}</div>
                        <div className={this.state.classes.length > 1 ? "dropdown-item" : "dropdown-item hide"} onMouseDown={this.setText}>{this.state.classes[1] ? `${this.state.classes[1][0]} (${this.state.classes[1][1]})` : ""}</div>
                        <div className={this.state.classes.length > 2 ? "dropdown-item" : "dropdown-item hide"} onMouseDown={this.setText}>{this.state.classes[2] ? `${this.state.classes[2][0]} (${this.state.classes[2][1]})` : ""}</div>
                    </div>
                </div>
            </td>
        )
    }

    //  Turns the dropdown on, async because find classes queries for classes and gives a promise
    dropdownOn = async () => {
        let classes = await this.props.findClasses(this.textRef.current.value);
        this.setState({
            active: true,
            classes: classes,
        })
    }

    dropdownOff = () => {
        this.setState({active: false})
    }

    //  Send update back up to the App component and change state here
    handleChange = (event) => {
        this.props.update(event.target.value, this.props.name)
        this.setState({value: event.target.value});
    }

    //  Send update back up to the App component and change state here
    setText = (event) => {
        this.props.update(event.target.innerText, this.props.name)
        this.setState({value: event.target.innerText, active: false});
    }
}

export default TableItem;