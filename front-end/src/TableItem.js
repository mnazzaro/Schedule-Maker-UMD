import React from 'react'

class TableItem extends React.Component {

    constructor (props) {
        super(props)
        this.state = {active: false}
        this.textRef = React.createRef();
    }

    render () {
        let courses = this.textRef.current ? this.textRef.current.value.length >= 3 ? this.props.findClasses(this.textRef.current) : null : null;
        return (
            <td>
                <div className="dropdown">
                    <input ref={this.textRef} onKeyUp={this.dropdownOn} onBlur={this.dropdownOff} height="100%"/>
                    <div className={this.state.active && courses ? "show dropdown-content" : "dropdown-content"}>
                        <div className="dropdown-item" onMouseDown={this.setText}>{courses ? courses[0]["course_id"] : ""}</div>
                        <div className="dropdown-item" onMouseDown={this.setText}>{courses ? courses[1]["course_id"] : ""}</div>
                        <div className="dropdown-item" onMouseDown={this.setText}>{courses ? courses[2]["course_id"] : ""}</div>
                    </div>
                </div>
            </td>
        )
    }

    dropdownOn = () => {
        this.setState({active: true})
    }

    dropdownOff = () => {
        this.setState({active: false})
    }

    setText = (event) => {
        this.textRef.current.value = event.target.textContent;
        this.dropdownOff();
    }
}

export default TableItem;