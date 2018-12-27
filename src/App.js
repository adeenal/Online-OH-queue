import React, { Component } from 'react';
import LandingPage from "./landing-page/LandingPage";
import QueueList from "./queues/QueueList";

import "bootstrap/dist/css/bootstrap.min.css";
import "./style/style.css"


class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: false,
      queues: []
    };

    this.logout = this.logout.bind(this);
  }

  componentDidMount() {
    fetch('/api/v1/queue/list/', {
      method: 'GET',
      headers: {
          "Authorization": "Token " + localStorage.getItem('credentials')
        }
    }).then((response) => {
      return response.json();
    }).then((body) => {
      if (body.detail) {
        if (body.detail.localeCompare("Invalid token.") == 0) {
          // invalid token
        }
      } else {
        this.setState({isLoggedIn: true});
        this.setState({queues: body});
      }
    });
  }

  logout() {
    localStorage.removeItem('credentials');
    this.props.history.push('/login');
  }

  render() {
    if(this.state.isLoggedIn) {
      return (
        <div>
          <p>It's lit</p>
          <button className="btn btn-primary btn-margin btn-xl" onClick={this.logout}>Log out</button>
          <QueueList queues={this.state.queues} />
        </div>
      );
    } else {
      return (
        <div id="root">
          <LandingPage/>
        </div>
      );
    }
  }
}

export default App;
