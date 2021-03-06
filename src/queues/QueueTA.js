import React from "react";
import $ from 'jquery'
import "../static/css/style.css"

class Queue extends React.Component {

    constructor() {
      super();
      this.answerQuestion = this.answerQuestion.bind(this);
      this.deleteQuestion = this.deleteQuestion.bind(this);
      this.extendQueue = this.extendQueue.bind(this);
      this.closeQueue = this.closeQueue.bind(this);
      this.state = {
        csrftoken: ""
      };
    }

    componentDidMount() {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = $.trim(cookies[i]);
              if (cookie.substring(0, 'csrftoken'.length + 1) === ('csrftoken' + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
                  break;
              }
          }
      }
      this.setState({csrftoken: cookieValue});
      fetch('/api/v1/theme/', {
        method: 'GET',
      }).then((response) => {
        return response.json();
      }).then((body) => {
        document.body.style.setProperty('--primary-color', body['primary_theme_color']);
      });
    }

    extendQueue(queueName) {
      var post_name = "/api/v1/queue/open/";
      fetch(post_name, {
        method: 'POST',
        body: JSON.stringify({
          "queue": this.props.queue.name
        }),
        headers: {
          "Authorization": "Token " + localStorage.getItem('credentials'),
          "X-CSRFToken": this.state.csrftoken
        }
      }).then((response) => {
        return response.json();
      }).then((body) => {
        if (!body["success"]) {
          // handle non success
        } 
      });
    }

    closeQueue(queueName) {
      var post_name = "/api/v1/queue/close/";
      fetch(post_name, {
        method: 'POST',
        body: JSON.stringify({
          "queue": this.props.queue.name
        }),
        headers: {
          "Authorization": "Token " + localStorage.getItem('credentials'),
          "X-CSRFToken": this.state.csrftoken
        }
      }).then((response) => {
        return response.json();
      }).then((body) => {
        if (!body["success"]) {
          // handle non success
        } 
      });
    }
    
  
    answerQuestion(questionId) {
      var post_name = "/api/v1/questions/answer/";
      fetch(post_name, {
        method: 'POST',
        body: JSON.stringify({
          "queue": this.props.queue.name,
          "question_id": questionId
        }),
        headers: {
          "Authorization": "Token " + localStorage.getItem('credentials'),
          "X-CSRFToken": this.state.csrftoken
        }
      }).then((response) => {
        return response.json();
      }).then((body) => {
        if (!body["success"]) {
          // handle non success
        }
      });
    }

    deleteQuestion(question_id) {
      var post_name = "/api/v1/questions/delete/";
      fetch(post_name, {
        method: 'POST',
        body: JSON.stringify({
          "question_id": question_id
        }),
        headers: {
          "Authorization": "Token " + localStorage.getItem('credentials'),
          "X-CSRFToken": this.state.csrftoken
        }
      }).then((response) => {
        return response.json();
      }).then((body) => {
        if (!body["success"]) {
          // handle non success
        }
      });
    }

    render() {
      var answerQuestionFunc = this.answerQuestion;
      var deleteQuestionFunc = this.deleteQuestion;
      var extendQueueFunc = this.extendQueue;
      var closeQueueFunc = this.closeQueue;
      var classNames = require('classnames');
    
      var btnGroupClassOpen = classNames(
        {
          'answer-link': !this.props.queue.is_open_extended,
          'answer-link-selected': this.props.queue.is_open_extended,
        }
      );

      var btnGroupClassClose = classNames(
        {
          'answer-link': !this.props.queue.is_closed,
          'answer-link-selected': this.props.queue.is_closed,
        }
      );

      var closed_message;
      if (this.props.queue.is_closed) {
        closed_message =  <p class="queue-status">Queue Closed Manually</p>;
      } else if (this.props.queue.is_open_extended) {
        closed_message = <p class="queue-status">Queue Opened Manually</p>;
      } else if (!this.props.queue.is_in_time) {
        closed_message =  <p class="queue-status">Queue Closed Because of Schedule</p>;
      } else {
        closed_message = <p class="queue-status">Queue Open</p>;
      }
    
      return (
        <div>
          <center><h2 class="queue-title">{this.props.queue.name}</h2>
          <p>{this.props.queue.description}</p>
          {closed_message}
          <p class="wait-time">Estimated Wait Time: <br />
           {this.props.queue.wait_time.toFixed(1)} Minutes</p>
           <button onClick={() => extendQueueFunc(this.props.queue.name)}
                 className={btnGroupClassOpen}>Keep Queue Open</button>
           <button onClick={() => closeQueueFunc(this.props.queue.name)}
                 className={btnGroupClassClose}>Close Queue Manually</button>
          <table class="queue">
          <tr>
            <th>Student</th>
          </tr>

          {this.props.queue.question_contents.map(function(question, index){
                return <tr><td><p class="queue-text">
                {index+1} - {question.first_name} {question.last_name} ({question.student_id})
                <br/> Question: {question.question_content}
                <br/> Time Asked: {question.time_asked}
                <br/></p><center><button onClick={() => answerQuestionFunc(question.id)}
                 class="answer-link">Answer</button>  <button onClick={() => deleteQuestionFunc(question.id)}
                 class="delete-link">Delete</button> </center> 
                </td></tr>
            })}
          </table></center>
        </div>
      );
    }
  }

  export default Queue;