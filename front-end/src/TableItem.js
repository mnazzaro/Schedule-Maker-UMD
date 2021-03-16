import React from 'React'

class TableItem extends React.Component {

    constructor (props) {
        this.state = {active: false}
    }

    render () {
        return (
            <td>
                <div className="dropdown">
                    <input onkeyup={this.state.active=true} height="100%"/>
                    <div className="dropdown-content {this.state.active ? show : ''">
                        <div className="dropdown-item">Option 1</div>
                        <div className="dropdown-item">Option 2</div>
                        <div className="dropdown-item">Option 3</div>
                    </div>
                </div>
            </td>
        )
    }
}

export default TableItem;