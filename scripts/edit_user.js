// Retrieve the form elements
const form = document.querySelector('form');
const saveButton = document.querySelector('.edit-user-button');

// Listen for a click event on the save button
saveButton.addEventListener('click', () => {
  // Construct the user object from the form data
  const user = {
    username: form.elements['user-username'].value,
    name: form.elements['user-name'].value,
    surname: form.elements['user-surname'].value,
    email: form.elements['user-email'].value,
    phone: form.elements['user-phone'].value,
    driveLicense: form.elements['user-drive-license'].value,
  };

  // Make a POST request to the API to save the user data
  fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify(user),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    // Check if the request was successful
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Update the form fields with the saved data
    form.elements['user-username'].value = data.username;
    form.elements['user-name'].value = data.name;
    form.elements['user-surname'].value = data.surname;
    form.elements['user-email'].value = data.email;
    form.elements['user-phone'].value = data.phone;
    form.elements['user-drive-license'].value = data.driveLicense;
  })
  .catch(error => {
    console.error('There was an error:', error);
  });
});
