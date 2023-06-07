document.addEventListener("DOMContentLoaded", () => {

      const form = document.querySelector('.log-in-form');
      const signupBtn = document.querySelector('#login-btn');
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        const username = document.querySelector('#username').value;
        const password = document.querySelector('#password').value;

        const data = {
          username: username,
          password: password,
        };

        const headers = new Headers();
        headers.set('Content-Type', 'application/json')

        fetch('http://127.0.0.1:63341/user/login', {
          method: 'POST',
          body: JSON.stringify(data),
          headers: headers
        })
        .then((response) => {
        console.log(response);
            if (response.ok) {
                return response.json()
            }
            
            throw new Error(response.statusText);
        })
        .then(response => {
          console.log('my access token = ' + response.AccessToken);
          const access_token = response.AccessToken;
          localStorage.setItem("access_token", access_token);
          window.location.href = "main.html";
        })
        .catch((error) => {
            console.log("ERRRRRRRRRRROOOOOORRRR: "+error);
        })



      });

});














