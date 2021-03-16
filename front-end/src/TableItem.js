import React from 'react'

class TableItem extends React.Component {

    constructor (props) {
        super(props)
        this.state = {active: false, classes: []}
        this.textRef = React.createRef();
    }

    render () {
        return (
            <td>
                <div className="dropdown">
                    <input ref={this.textRef} onKeyUp={this.dropdownOn} onBlur={this.dropdownOff} height="100%"/>
                    <div className={this.state.active && this.state.classes.length > 0 ? "show dropdown-content" : "dropdown-content"}>
                        <div className="dropdown-item" onMouseDown={this.setText}>{this.state.classes.length > 0 ? this.state.classes[0]["course_id"] : ""}</div>
                        <div className={this.state.classes.length > 1 ? "dropdown-item" : "dropdown-item hide"} onMouseDown={this.setText}>{this.state.classes[1] ? this.state.classes[1]["course_id"] : ""}</div>
                        <div className={this.state.classes.length > 2 ? "dropdown-item" : "dropdown-item hide"} onMouseDown={this.setText}>{this.state.classes[2] ? this.state.classes[2]["course_id"] : ""}</div>
                    </div>
                </div>
            </td>
        )
    }

    dropdownOn = () => {
        this.setState({
            active: true,
            classes: this.props.findClasses(this.textRef.current.value)
        })
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