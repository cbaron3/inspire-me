import React from 'react';
import axios from 'axios';

class PhoneInput extends React.Component {
    constructor() {
      super();
      this.state = {
        number: '',
      };
    }

    onChange = (e) => {
      this.setState({ [e.target.name]: e.target.value });
    }

    onSubmit = (e) => {
      e.preventDefault();
      // get our form data out of state
      const { number } = this.state;
      console.log(number);

      const url = 'http://0.0.0.0:5000/api/v1/subscribe';
      console.log(url);

      axios.post(url, {phone_number: number, time: '12:12'})
        .then(function (response) {
            alert('Valid subscription!');
            console.log(response);
        })
        .catch(function (error) {
            alert('Error when subscribing!');
            console.log(error);
        });
    }

    render() {
      const { number } = this.state;
      return (
        <form onSubmit={this.onSubmit}>
          <input
            type="text"
            name="number"
            value={number}
            onChange={this.onChange}
          />
          <button type="submit">Submit</button>
        </form>
      );
    }
  }

export default PhoneInput;