import React from "react";
import "../static/css/style.css"

class LoginForm extends React.Component {
    constructor() {
      super();

      this.state = {
        email: '',
        password: ''
      }

      this.onChange = this.onChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
      document.title = "Online OH Queue";
      fetch('/api/v1/theme/', {
        method: 'GET',
      }).then((response) => {
        return response.json();
      }).then((body) => {
        document.body.style.setProperty('--primary-color', body['primary_theme_color']);
      });
    }
  
    handleSubmit(event) {
      event.preventDefault();
      const data = new FormData(event.target);
      fetch('/api/v1/users/login/', {
        method: 'POST',
        body: data,
      }).then((response) => {
        return response.json();
      }).then((body) => {
        if (body.error) {
          alert('Invalid login');
        } else {
          localStorage.setItem('credentials', body.token);
          this.props.history.push('/');
        }
      });
    }

    onChange(event) {
      this.setState({[event.target.name]: event.target.value});
    }
  
    render() {
      return (
        <div class="formBg">
          <div class="login-page">
            <div class="userForm">
              <form class="login-form" onSubmit={this.handleSubmit}>
                <h2 class="header-login"><center>Log in</center></h2>
                <label htmlFor="email">Penn Email</label>
                <input id="email" name="email" type="email" value={this.state.email} onChange={this.onChange} />  
                <label htmlFor="password">Password</label>
                <input id="password" name="password" type="password" value={this.state.password} onChange={this.onChange} />
                <button>login</button>
                <p class="message">Not registered? <a href="/signup">Create an account</a></p>
                <p class="message">Forget your password? <a href="/password_reset">Reset your password</a></p>
              </form>
            </div>
          </div>
        </div>
      );
    }
  }

  export default LoginForm;