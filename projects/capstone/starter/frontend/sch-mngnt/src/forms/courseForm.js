import React, { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";

function Course_Form() {
  const [state, setstate] = useState({
    title: "",
    code: "",
    desc: "",
    book: "",
    lec: "",
    room: "",
  });

  const handleChange = (event) => {
    const value = event.target.value;
    setstate({
      ...state,
      [event.target.name]: value,
    });
  };

  const { getAccessTokenSilently } = useAuth0();

  const postData = (url = "", data = {}) => {
    return new Promise(async (resolve, reject) => {
      const token = await getAccessTokenSilently();
      console.log(data);
      try {
        const request = await fetch(url, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });
        let result = await request.json();
        resolve(result);
      } catch (error) {
        reject(error);
      }
    });
  };

  const newCourse = () => {
    const formdata = { ...state };
    postData("/courses/create", formdata)
      .then((response) => {
        document.querySelector("#addCourse").reset();
        console.log(response);
        console.log("data posted Successfully");
      })
      .catch((err) => console.log(err + "data not posted"));
  };
  const submitBtn = (event) => {
    event.preventDefault();
    // postFormData();
    // console.log(state.title);
    newCourse();
  };

  return (
    <div className="container center-div">
      <form id="addCourse" className="row g-3">
        <div className="col-md-8">
          <label htmlFor="title" className="form-label">
            Course title
          </label>
          <input
            type="text"
            className="form-control"
            id="title"
            name="title"
            value={state.title}
            onChange={handleChange}
          />
        </div>
        <div className="col-md-8">
          <label htmlFor="code" className="form-label">
            Course Code
          </label>
          <input
            type="text"
            className="form-control"
            id="code"
            name="code"
            value={state.code}
            onChange={handleChange}
            placeholder="MBA624"
          />
        </div>
        <div className="col-md-8">
          <label htmlFor="desc" className="form-label">
            Course description
          </label>
          <textarea
            className="form-control"
            name="desc"
            value={state.desc}
            onChange={handleChange}
            aria-label="With textarea"
          ></textarea>
        </div>
        <div className="col-md-8">
          <label htmlFor="book" className="form-label">
            Course Textbook
          </label>
          <input
            type="text"
            className="form-control"
            id="book"
            name="book"
            value={state.book}
            onChange={handleChange}
          />
        </div>
        <div className="col-md-8">
          <label htmlFor="book" className="form-label">
            Course Instructor
          </label>
          <select className="custom-select" name="lec" onChange={handleChange}>
            <option value="1">Oscar Bundi </option>
            <option value="2">Charles Gardner</option>
            <option value="3">Mary Rhodes</option>
          </select>
        </div>
        <div className="col-md-8">
          <label htmlFor="book" className="form-label">
            Course Room
          </label>
          <select className="custom-select" name="room" onChange={handleChange}>
            <option value="1">RM623</option>
            <option value="2">RM167</option>
            <option value="3">RM302</option>
          </select>
        </div>
        <div className="col-md-8" id="submitButton">
          <button type="submit" className="btn btn-primary" onClick={submitBtn}>
            Save
          </button>
        </div>
      </form>
    </div>
  );
}

export default Course_Form;
