document.addEventListener("DOMContentLoaded", () => {
      const form = document.querySelector('.sign-up-form');
      const signupBtn = document.querySelector('#signup-btn');
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        const username = document.querySelector('#username').value;
        const password = document.querySelector('#password').value;
        const first_name = document.querySelector('#name').value;
        const last_name = document.querySelector('#surname').value;
        const email = document.querySelector('#email').value;
        const phone = document.querySelector('#phone').value;
        const drive_license = document.querySelector('#drive_license').value;

        const data = {
          username: username,
          password: password,
          first_name: first_name,
          last_name: last_name,
          email: email,
          phone: phone,
          drive_license: drive_license
        };
        fetch('http://127.0.0.1:63341/user/user', {
          method: 'POST',
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          window.location.href = "index.html";
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
        });
      });
});



















    //import { makeRequest } from "./http.js";
    //
    //document.addEventListener("DOMContentLoaded", () => {
    //  const button = document.querySelector('button[type="submit"]');
    //
    //  button.addEventListener("click", async (event) => {
    //    event.preventDefault();
    //
    //    const email = document.querySelector(
    //          'input[placeholder="Enter email"]'
    //        ).value;
    //    const phone = document.querySelector(
    //          'input[placeholder="Enter phone"]'
    //        ).value;
    //    const firstName = document.querySelector(
    //      'input[placeholder="Enter first name"]'
    //    ).value;
    //    const lastName = document.querySelector(
    //      'input[placeholder="Enter last name"]'
    //    ).value;
    //    const password = document.querySelector(
    //      'input[placeholder="Password"]'
    //    ).value;
    //
    //    const data = {
    //      email: email,
    //      phone: phone,
    //      username: firstName,
    //      first_name: lastName,
    //      password: password
    //    };
    //
    //    try {
    //      const response = await makeRequest(
    //        "http://localhost:63342/user_api",
    //        "POST",
    //        data
    //      );
    //
    //      console.log("Success:", response);
    //      // Redirect the user to the login page
    //      window.location.href = "index.html";
    //    } catch (error) {
    //      console.error("Error:", error);
    //    }
    //  });
