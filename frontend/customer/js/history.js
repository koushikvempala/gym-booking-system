let bookings = [
    { id: 1, gym: "Flex Gym", date: "2026-05-20", status: "upcoming" },
    { id: 2, gym: "Power House", date: "2026-04-15", status: "completed" },
    { id: 3, gym: "Muscle Factory", date: "2026-04-10", status: "cancelled" },
    { id: 4, gym: "Pro Fitness", date: "2026-05-22", status: "upcoming" }
];

function displayBookings(data) {
    let container = document.getElementById("bookingList");
    container.innerHTML = "";

    data.forEach(b => {
        let card = document.createElement("div");
        card.className = "booking-card";

        card.innerHTML = `
            <h3>${b.gym}</h3>
            <p>Date: ${b.date}</p>
            <p class="status ${b.status}">
                ${b.status.toUpperCase()}
            </p>

            ${b.status === "upcoming"
                ? `<button class="cancel-btn"
                    onclick="cancelBooking(${b.id})">
                    Cancel
                   </button>`
                : ""
            }

            ${b.status === "completed"
                ? `<button class="rate-btn"
                    onclick="rateBooking('${b.gym}')">
                    Rate
                   </button>`
                : ""
            }

            <button class="download-btn"
                onclick="downloadReceipt('${b.gym}')">
                Receipt
            </button>
        `;

        container.appendChild(card);
    });

    updateStats();
}

function filterData() {
    let search = searchInput.value.toLowerCase();
    let date = dateFilter.value;
    let status = statusFilter.value;

    let filtered = bookings.filter(b =>
        b.gym.toLowerCase().includes(search) &&
        (date === "" || b.date === date) &&
        (status === "all" || b.status === status)
    );

    displayBookings(filtered);
}

/* ELEMENTS */
let searchInput = document.getElementById("search");
let dateFilter = document.getElementById("dateFilter");
let statusFilter = document.getElementById("statusFilter");

/* EVENTS */
searchInput.addEventListener("input", filterData);
dateFilter.addEventListener("input", filterData);
statusFilter.addEventListener("change", filterData);

/* CANCEL BOOKING */
function cancelBooking(id) {
    bookings = bookings.map(b =>
        b.id === id
            ? { ...b, status: "cancelled" }
            : b
    );

    displayBookings(bookings);
}

/* RATE BOOKING */
function rateBooking(gym) {
    let rating = prompt("Give rating (1-5) for " + gym);

    if (rating) {
        alert("Thanks for rating ⭐ " + rating);
    }
}

/* DOWNLOAD RECEIPT */
function downloadReceipt(gym) {
    alert("Downloading receipt for " + gym);
}

/* UPDATE STATS */
function updateStats() {
    document.getElementById("total").innerText =
        bookings.length;

    document.getElementById("active").innerText =
        bookings.filter(b => b.status === "upcoming").length;

    document.getElementById("cancelledCount").innerText =
        bookings.filter(b => b.status === "cancelled").length;
}

/* DARK MODE */
function toggleDarkMode() {
    document.body.classList.toggle("dark");
}

/* INIT */
displayBookings(bookings);