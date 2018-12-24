import React, { Component } from 'react';
import {BrowserRouter as Router, Route, Link, Switch} from 'react-router-dom'
import './App.css';
import axios from 'axios';

class Home extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            todos: []
        };
      }
    
    componentDidMount() {
        this.getTodos();
    }

    getTodos() {
        axios
            .get('http://localhost:8000/api/articles/')
            .then(res => {
                this.setState({ todos: res.data.results });
                console.log(res);
            })
            .catch(err => {
                console.log(err);
            });
    }

    render() {
        return (
          <div>
            <h1>テスト</h1>
              {this.state.todos.map( todos => (
                <div className="article-header" key={todos.id}>
                <li>{todos.title}</li>
                <li>{todos.text}</li>
                </div>
              ))}
          </div>
        );
      }
    
}

export default Home;
