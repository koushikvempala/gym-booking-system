let allGyms = [];

fetch("../data/gyms.json")
    .then(res => res.json())
    .then(gyms => {
        allGyms = gyms;

        populateLocations(gyms);
        displayGyms(gyms);
    })
    .catch(err => console.log(err));


// STEP 1: Populate dropdown with unique locations
function populateLocations(gyms) {
    const select = document.getElementById("locationSelect");

    const locations = [...new Set(gyms.map(g => g.address))];

    locations.forEach(loc => {
        const option = document.createElement("option");
        option.value = loc;
        option.textContent = loc;
        select.appendChild(option);
    });
}


// STEP 2: Filter gyms based on location
function filterGyms() {
    const selectedLocation = document.getElementById("locationSelect").value;

    if (selectedLocation === "all") {
        displayGyms(allGyms);
    } else {
        const filtered = allGyms.filter(gym =>
            gym.address === selectedLocation
        );

        displayGyms(filtered);
    }
}


// STEP 3: Render gyms
function displayGyms(gyms) {
    const container = document.getElementById("gymContainer");
    container.innerHTML = "";

    if (gyms.length === 0) {
        container.innerHTML = "<p>No gyms found for this location</p>";
        return;
    }

    gyms.forEach(gym => {
        const card = document.createElement("div");
        card.className = "gym-card";

        card.innerHTML = `
      <h3>${gym.gym_name}</h3>
      <p><b>Location:</b> ${gym.address}</p>
      <p><b>Rating:</b> ⭐ ${gym.rating}</p>
      <p class="status ${gym.status}">${gym.status}</p>

      <button onclick="viewDetails(${gym.gym_id})">
        View Details
      </button>
    `;

        container.appendChild(card);
    });
}


// STEP 4: Navigate to details page
function viewDetails(gymId) {
    localStorage.setItem("selectedGymId", gymId);
    window.location.href = "gym-details.html";
}