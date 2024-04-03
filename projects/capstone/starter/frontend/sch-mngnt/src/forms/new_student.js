import React from "react";

class NewStudent extends React.Component {
  constructor() {
    super();
    this.state = {};
  }

  render() {
    return (
      <form class="row g-3">
        <div class="col-md-6">
          <label for="fname" class="form-label">
            First Name
          </label>
          <input type="text" class="form-control" id="fname" />
        </div>
        <div class="col-md-6">
          <label for="lname" class="form-label">
            Last Name
          </label>
          <input type="text" class="form-control" id="lname" />
        </div>
        <div class="col-12">
          <label for="email" class="form-label">
            Email
          </label>
          <input
            type="email"
            class="form-control"
            id="email"
            placeholder="abc@provider.com"
          />
        </div>
        <div class="col-12">
          <label for="regno" class="form-label">
            Registration Number
          </label>
          <input
            type="text"
            class="form-control"
            id="regno"
            placeholder="1234"
          />
        </div>
        <div class="col-md-6">
          <label for="dob" class="form-label">
            Date of Birth
          </label>
          <input type="date" class="form-control" id="dob" />
        </div>
        <div class="col-md-4">
          <label for="gender" class="form-label">
            Gender
          </label>
          <select id="gender" class="form-select">
            <option selected>Choose...</option>
            <option>Male</option>
            <option>Female</option>
          </select>
        </div>
        <div class="col-12">
          <button type="submit" class="btn btn-primary">
            Sign in
          </button>
        </div>
      </form>
    );
  }
}

export default NewStudent;
