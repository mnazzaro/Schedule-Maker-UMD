import TableItem from './TableItem.js'

function TableRow (props) {
    return (
        <tr>
            {for (i in 1...8) {
                <TableItem/>
            }}
        </tr>
    )
}