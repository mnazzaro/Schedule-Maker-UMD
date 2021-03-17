function Warnings (props) {
    return (
        <div className="warnings-container">
            <div className={props.enough_credits ? "warning enough-credits" : "hide"}>{props.enough_credits}</div>
            <div className={props.lower_level_math ? "warning lower_level_math" : "hide"}>{props.lower_level_math}</div>
            <div className={props.lower_level_cs ? "warning lower_level_cs" : "hide"}>{props.lower_level_cs}</div>
            <div className={props.upper_level ? "warning upper_level" : "hide"}>{props.upper_level_concentration}</div>
            <div className={props.general_track ? "warning general_track" : "hide"}>{props.general_track}</div>
            <div className={props.gened ? "warning gened" : "hide"}>{props.gened}</div>
        </div>
    )
}

export default Warnings;