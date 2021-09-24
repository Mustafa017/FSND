import { useAuth0 } from "@auth0/auth0-react";
import { NavLink } from "react-router-dom";

const Header = () => {
  const { isAuthenticated, loginWithRedirect, logout } = useAuth0();
  const activeStyle = { color: "orange" };
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <a className="navbar-brand" href="/">
        HardKnocks School
      </a>
      {isAuthenticated && (
        <div>
          <button
            className="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#navbarNavAltMarkup"
            aria-controls="navbarNavAltMarkup"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div className="navbar-nav">
              <NavLink
                className="nav-item nav-link"
                to="/"
                activeStyle={activeStyle}
                exact
              >
                Home
              </NavLink>
              <NavLink
                to="/courses"
                className="nav-item nav-link"
                activeStyle={activeStyle}
              >
                Courses
              </NavLink>
              <NavLink
                className="nav-item nav-link"
                to="/about"
                activeStyle={activeStyle}
              >
                About
              </NavLink>
            </div>
          </div>
          <button
            className="btn btn-primary"
            onClick={() =>
              logout({
                returnTo: window.location.origin,
              })
            }
          >
            Log out
          </button>
        </div>
      )}
      {!isAuthenticated && (
        <button className="btn btn-primary" onClick={() => loginWithRedirect()}>
          Log in
        </button>
      )}
    </nav>
  );
};

export default Header;
