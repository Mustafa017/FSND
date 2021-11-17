import React from "react";

class CourseView extends React.Component {
  constructor(props) {
    super();
  }
  render() {
    return (
      <div className="col">
        <div className="card">
          {/* <img src="..." className="card-img-top" alt="..." /> */}
          <div className="card-body">
            <h5 className="card-title">{this.props.course_title}</h5>
            <p className="card-text">{this.props.course_desc}</p>
            <i className=""></i>
          </div>
        </div>
      </div>
    );
  }
}

export default CourseView;
