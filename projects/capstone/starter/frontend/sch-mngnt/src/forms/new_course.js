import React, { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";

function NewCourse() {
  const [state, setState] = useState({});

  const submitBtn = (event) => {
    event.preventDefault();
  };
  return (
    <div>
      <p>placeholder</p>
    </div>
  );
}

export default NewCourse;
