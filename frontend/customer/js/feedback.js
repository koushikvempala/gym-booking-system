// FACTORS
let factors = [
    "Equipment",
    "Cleanliness",
    "Trainer Support",
    "Crowd",
    "Pricing",
    "Experience",
    "Facilities",
    "Overall"
];

let ratings = new Array(factors.length).fill(0);

let container = document.getElementById("ratings");

// CREATE RATINGS
factors.forEach((factor, i) => {

    let div = document.createElement("div");

    let stars = "";

    for (let j = 1; j <= 5; j++) {
        stars += `
            <span onclick="setRating(${i}, ${j}, this)">
                ★
            </span>
        `;
    }

    div.innerHTML = `
        <div class="rating-label">
            ${factor}
        </div>

        <div class="stars">
            ${stars}
        </div>
    `;

    container.appendChild(div);
});

// SET STAR RATING
function setRating(group, value, el) {

    ratings[group] = value;

    let stars = el.parentNode.children;

    for (let i = 0; i < stars.length; i++) {
        stars[i].classList.toggle("active", i < value);
    }
}

// SUBMIT
function submitFeedback() {

    let phone = document.getElementById("phone").value;

    // PHONE VALIDATION
    if (!/^[6-9]\d{9}$/.test(phone)) {
        alert("Enter valid 10-digit phone number (6-9)");
        return;
    }

    // CHECK RATINGS
    if (ratings.includes(0)) {
        alert("Please fill all ratings");
        return;
    }

    // SHOW MODAL
    document.getElementById("modal").style.display = "flex";
}

// CLOSE MODAL
function closeModal() {
    document.getElementById("modal").style.display = "none";
}