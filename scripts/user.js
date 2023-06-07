const username = document.querySelector('#user-username');
const name = document.querySelector('#user-name');
const surname = document.querySelector('#user-surname');
const email = document.querySelector('#user-email');
const phone = document.querySelector('#user-phone');
const license = document.querySelector('#user-driver-license');

fetch('http://127.0.0.1:63341/user/me', {
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        })
        .then(response => response.json())
        .then(data => {
            // Update the HTML elements with user data
            username.textContent = data.username;
            name.textContent = data.first_name;
            surname.textContent = data.last_name;
            email.textContent = data.email;
            phone.textContent = data.phone;
            license.textContent = data.drive_license;
          })
          .catch(error => console.error(error));

const deleteButton = document.querySelector('.delete-user-button');
deleteButton.addEventListener('click', () => {
  fetch('http://127.0.0.1:63341/user/deleteMe', {
            method: "DELETE",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        })
    .then(response => response.json())
    .then(data => {
        window.location.href = "index.html";
    })
    .catch(error => console.error(error));
});

