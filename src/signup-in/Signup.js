import React from "react";
import "./style.css"
import swal from 'sweetalert';


class SignUpForm extends React.Component {
  
    constructor(props) {
      super(props);
      this.state = {
        validationErrors: []
      };
      this.handleSubmit = this.handleSubmit.bind(this);
    }
    
    handleValidation(data) {
      var violationExists = false;
      var violationList = [];

      var email = data.get("email");
      var first_name = data.get("first_name");
      var last_name = data.get("last_name");
      var password = data.get("password");
      if (email.indexOf("upenn.edu") == -1) {
        violationList.push("Must have a penn email");
        violationExists = true;
      }
      if (first_name.length == 0) {
        violationList.push("First name cannot be blank");
        violationExists = true;
      }
      if (last_name.length == 0) {
        violationList.push("Last name cannot be blank");
        violationExists = true;
      }
      if (password.length < 8) {
        violationList.push("Password must be at least 8 characters");
        violationExists = true;
      }

      if (violationExists) {
        this.setState({validationErrors: this.state.validationErrors.concat(violationList)});
      }
      return !violationExists;
    }
  
    handleSubmit(event) {
      event.preventDefault();
      const data = new FormData(event.target);

      if (this.handleValidation(data)) {
        fetch('/api/v1/users/register/', {
          method: 'POST',
          body: data,
        }).then((response) => {
          if (response.ok) {
            swal("Email Confirmation Sent!", "Please check your email to confirm your account", "success");
            document.getElementById("email").value = "";
            document.getElementById("first_name").value = "";
            document.getElementById("last_name").value = "";
            document.getElementById("password").value = "";
          } else {
            var violationList = ["Email is taken"];
            this.setState({validationErrors: this.state.validationErrors.concat(violationList)});
          }
        });
      }
    }
  
    render() {
      return (
        <div class="formBg">
          <div class="login-page">
            <div class="userForm">
              <form class="login-form" onSubmit={this.handleSubmit}>
                <label htmlFor="email">Enter Penn Email</label>
                <input id="email" name="email" type="email" />
        
                <label htmlFor="first_name">First Name</label>
                <input id="first_name" name="first_name" type="text" />
        
                <label htmlFor="last_name">Last Name</label>
                <input id="last_name" name="last_name" type="text" />

                <label htmlFor="password">Password</label>
                <input id="password" name="password" type="password" />
        
                <button>Sign Up</button>
              </form>
              <br />
              <ul class="validationErrorList">
                {this.state.validationErrors.map(function(validationError, index){
                  return <li>{validationError}</li>
                })}
              </ul>
            </div>
          </div>
        </div>
      );
    }
  }

  export default SignUpForm;