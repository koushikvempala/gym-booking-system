
const gymId = localStorage.getItem("selectedGymId");

//
// 🏋️ GYM INFO
//
fetch("../data/gyms.json")
  .then(res => res.json())
  .then(gyms => {

    const gym = gyms.find(g => g.gym_id == gymId);

    document.getElementById("gymName").innerText = gym.gym_name;
    document.getElementById("gymLocation").innerText = "📍 " + gym.address;
    document.getElementById("gymRating").innerText = "⭐ " + gym.rating;
    document.getElementById("gymDesc").innerText = gym.description;
  });

//
// 💳 PLANS (DISPLAY ONLY)
//
fetch("../data/plans.json")
  .then(res => res.json())
  .then(plans => {

    const container = document.getElementById("planList");

    plans.forEach(p => {

      const card = document.createElement("div");
      card.className = "card";

      card.innerHTML = `
        <h3>${p.plan_name}</h3>
        <p>Duration: ${p.duration}</p>
        <p>Price: ₹${p.price}</p>
        <p>${p.features}</p>
      `;

      container.appendChild(card);
    });
  });

//
// ⏰ SLOTS (DISPLAY ONLY)
//
fetch("../data/slots.json")
  .then(res => res.json())
  .then(slots => {

    const gymSlots = slots.filter(s => s.gym_id == gymId);

    const container = document.getElementById("slotList");

    gymSlots.forEach(s => {

      const card = document.createElement("div");
      card.className = "card";

      card.innerHTML = `
        <h3>⏰ ${s.slot_time}</h3>
        <p>Status: ${s.status}</p>
      `;

      container.appendChild(card);
    });
  });

//
// 🔘 NAVIGATION
//
function goToBooking() {
  window.location.href = "booking.html";
}