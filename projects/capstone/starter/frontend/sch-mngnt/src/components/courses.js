import React from "react";
import { withAuth0 } from "@auth0/auth0-react";
import CourseView from "./courseView";
import { Link } from "react-router-dom";

class Course extends React.Component {
  constructor(props) {
    super();
    this.state = {
      page: 1,
      courses: [],
      total: "",
    };
  }

  getJson(url) {
    return new Promise(async (resolve, reject) => {
      try {
        const { getAccessTokenSilently } = this.props.auth0;
        const response = await getAccessTokenSilently({
          audience: "courses",
        });
        const token = await response;
        let data = await fetch(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        let result = await data.json();
        resolve(result);
      } catch (error) {
        reject(error);
      }
    });
  }

  getCourses = () => {
    this.getJson("/courses")
      .then((data) => {
        let { courses, total } = data;
        this.setState({
          courses,
          total,
        });
      })
      .catch((error) => {
        console.log(error);
        throw error;
      });
  };

  componentDidMount() {
    this.getCourses();
  }

  render() {
    return (
      <div>
        <div className="container">
          <Link to="/addCourse">
            <button className="btn-primary">Add Course</button>
          </Link>
          <div className="row row-cols-1 row-cols-md-3 g-4">
            {this.state.courses.map((course) => (
              <CourseView key={course.course_id} {...course} />
            ))}
          </div>
        </div>
      </div>
    );
  }
}

export default withAuth0(Course);
