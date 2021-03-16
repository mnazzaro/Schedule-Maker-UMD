import React from 'react'

class TableItem extends React.Component {

    constructor (props) {
        super(props)
        this.state = {active: false}
        this.textRef = React.createRef();
    }

    componentDidMount = () => {
        this.textRef.current.addEventListener("blur", this.dropdownOff)
    }

    render () {
        return (
            <td>
                <div className="dropdown">
                    <input ref={this.textRef} onKeyUp={this.dropdownOn} height="100%"/>
                    <div className={this.state.active ? "show dropdown-content" : "dropdown-content"}>
                        <div className="dropdown-item" onMouseDown={this.setText}>Option 1</div>
                        <div className="dropdown-item" onMouseDown={this.setText}>Option 2</div>
                        <div className="dropdown-item" onMouseDown={this.setText}>Option 3</div>
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