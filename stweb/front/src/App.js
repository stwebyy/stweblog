import React, { Component } from 'react';
import {BrowserRouter as Router, Route, Link, Switch} from 'react-router-dom'
import './App.css';
import axios from 'axios';
import Home from './Home';
import Header from './header';

class App extends Component {
  constructor(props){
    super(props);
    this.state = {

    };
  }
    render() {
    return (
      <div>
        <Home />
      </div>
    );
  }
}

export default App;
