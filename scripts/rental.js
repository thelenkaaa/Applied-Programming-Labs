function getCarIdFromUrlParams() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('car_id');
}

async function get_car_by_id() {
  try {
    const that_id = getCarIdFromUrlParams();
    console.log(that_id);

    const response = await fetch(`http://127.0.0.1:63341/car/${that_id}`);
    const data = await response.json();


    const instance = `
        <h3 class="text-center mb-4">${data.mark}</h3>
        <div class="car-image-wrapper-order">
          <img src="${data.image_path}" alt="Car Image">
        </div>

        <div class="car-description my-2">
          <button class="car-status-button-order">${data.status}</button>
          <ul class="car-features my-2">
            <li><strong>Category:</strong> ${data.category}</li>
            <li><strong>Price:</strong> ${data.price}$ per day, available discounts</li>
            <li><strong>Transmission:</strong> ${data.transmission}</li>
          </ul>
        </div>
    `;
    document.querySelector('#car-instance-div').innerHTML = instance;

    // Do something with the instance variable, such as append it to the DOM
  } catch (error) {
    console.log(error);
  }
}

async function create_order(){
    const form = document.querySelector('#order-form');
    form.addEventListener('submit', function(event) {
      event.preventDefault();
      alert('Order submitted successfully! Check your email for further details');
      window.location.href = 'main.html'; // replace with your own URL
    });


}

document.addEventListener("DOMContentLoaded", () => {
  get_car_by_id();
  create_order();
});
