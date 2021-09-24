import "./App.css";
import { Switch, Route, BrowserRouter } from "react-router-dom";
import Course from "./components/courses";
import Header from "./common/header";
import About from "./components/about";
import Home from "./components/home";
import React from "react";
import PageNotFound from "./components/PageNotFound";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Switch>
        <Route path="/" component={Home} exact />
        <Route path="/about" component={About} />
        <Route path="/courses" component={Course} />
        <Route component={PageNotFound} />
      </Switch>
    </BrowserRouter>
  );
}
export default App;
