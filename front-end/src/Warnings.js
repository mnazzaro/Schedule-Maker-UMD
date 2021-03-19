function Warnings (props) {
    return (
        <div className="warnings-container">
            <div className={props.enough_credits ? "warning enough-credits" : "hide"}>{props.enough_credits}</div>
            <div className={props.lower_level_math ? "warning lower-level-math" : "hide"}>{props.lower_level_math}</div>
            <div className={props.lower_level_cs ? "warning lower-level-cs" : "hide"}>{props.lower_level_cs}</div>
            <div className={props.upper_level ? "warning upper-level" : "hide"}>{props.upper_level}</div>
            <div className={props.general_track ? "warning general-track" : "hide"}>{props.general_track}</div>
            <div className={props.gened ? "warning gened" : "hide"}>{props.gened}</div>
        </div>
    )
}

export default Warnings;