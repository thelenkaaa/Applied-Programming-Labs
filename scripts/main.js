
console.log(localStorage.getItem("access_token"));

function clearList() {
        const carList = document.getElementById("car-list");
        while (carList.firstChild) {
        carList.removeChild(carList.firstChild);
        }
}

document.addEventListener("DOMContentLoaded", () => {


       // Get buttons and add event listeners
    const avlbBtn = document.querySelector('#avlb-btn');
    const unavlbBtn = document.querySelector('#unavlb-btn');

    avlbBtn.addEventListener('click', () => {
      getCarsByAvailStatus();
      avlbBtn.style.backgroundColor = '#5072A7';
       avlbBtn.style.color = 'white';// Change background color to green
      unavlbBtn.style.backgroundColor = ''; // Reset background color of other button
      unavlbBtn.style.color = '';
    });

    unavlbBtn.addEventListener('click', () => {
      getCarsByUnavailStatus();
      unavlbBtn.style.backgroundColor = '#5072A7'; // Change background color to red
      unavlbBtn.style.color = 'white';
      avlbBtn.style.backgroundColor = ''; // Reset background color of other button
      avlbBtn.style.color = '';
    });


    // Function to get cars with available status
    function getCarsByAvailStatus() {
      fetch('http://127.0.0.1:63341/car/getByStatusAvail', {
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        })
      .then(response => {
        if (!response.ok) {
          throw new Error(response.status);
        }
        return response.json();
      })

      .then(data => {
                clearList()
                data.forEach(car => {
                    const carElement = document.createElement('div');
                    const instanse = `
                    <div class="col-md-4 col-sm-6 col-12" >
                    <a href="rental.html?car_id=${car.car_id}">
                        <div class="car-image-wrapper">
                            <img src="${car.image_path}">
                            <p class="car-name text-lg">${car.mark}</p>
                            <p class="car-price">${car.price} $/day</p>
                        </div>
                        </a>
                    </div>
                    `;
                    carElement.addEventListener('click', () => {
                        event.preventDefault();
                        const carId = car.car_id;
                        console.log(carId);
                        window.location.href = 'rental.html';
                     });

                    document.querySelector('.car-list').insertAdjacentHTML('beforeend', instanse);
                });
            })
      .catch(error => console.error(`Error fetching data: ${error}`));
    }

    // Function to get cars with unavailable status
    function getCarsByUnavailStatus() {
      fetch('http://127.0.0.1:63341/car/getByStatusUnavail', {
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        })
      .then(response => {
        if (!response.ok) {
          throw new Error(response.status);
        }
        return response.json();
      })
      .then(data => {
                clearList()
                data.forEach(car => {
                    const carElement = document.createElement('div');
                    const instanse = `
                    <div class="col-md-4 col-sm-6 col-12" >
                    <a href="rental.html?car_id=${car.car_id}">
                        <div class="car-image-wrapper">
                            <img src="${car.image_path}">
                            <p class="car-name text-lg">${car.mark}</p>
                            <p class="car-price">${car.price} $/day</p>
                        </div>
                        </a>
                    </div>
                    `;
                    carElement.addEventListener('click', () => {
                        event.preventDefault();
                        const carId = car.car_id;
                        console.log(carId);
                        window.location.href = 'rental.html';
                     });

                    document.querySelector('.car-list').insertAdjacentHTML('beforeend', instanse);
                });
            })
      .catch(error => console.error(`Error fetching data: ${error}`));
    }

    async function get_all_cars(){
        fetch('http://127.0.0.1:63341/car/getAll', {
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        })
            .then(res => {
                return res.json();
            })
            .then(data => {
                data.forEach(car => {
                    const carElement = document.createElement('div');

                    const instanse = `
                        <div class="col-md-4 col-sm-6 col-12">
                                <a href="rental.html?car_id=${car.car_id}">
                                <div class="car-image-wrapper">
                                    <img src="${car.image_path}">
                                    <p class="car-name text-lg">${car.mark}</p>
                                    <p class="car-price">${car.price} $/day</p>
                                </div>
                                </a>

                        </div>
                    `;
                    carElement.addEventListener('click', () => {
                        event.preventDefault();
                        const carId = car.car_id;
                        console.log(carId);
                        window.location.href = 'rental.html';
                     });
                    document.querySelector('.car-list').insertAdjacentHTML('beforeend', instanse);
                });
            })
            .catch(error => console.log(error));
    }

    get_all_cars();
});
