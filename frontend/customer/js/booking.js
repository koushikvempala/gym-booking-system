const gymId = localStorage.getItem("selectedGymId");

// ================= STATE =================

let selectedPlan = null;
let selectedSlot = null;

// ================= LOAD PLANS =================

fetch("../data/plans.json")
    .then(res => res.json())
    .then(plans => {

        const container =
            document.getElementById("planList");

        plans.forEach(plan => {

            const card = document.createElement("div");

            card.className = "card";

            card.innerHTML = `
        <h3>${plan.plan_name}</h3>
        <p>₹${plan.price}</p>
        <p>${plan.duration}</p>
      `;

            // PLAN SELECT

            card.onclick = () => {

                document
                    .querySelectorAll("#planList .card")
                    .forEach(c =>
                        c.classList.remove("selected"));

                card.classList.add("selected");

                selectedPlan = plan;

                document.getElementById("summaryPlan")
                    .innerText =
                    "Plan: " + plan.plan_name;

                document.getElementById("summaryPrice")
                    .innerText =
                    "Price: ₹" + plan.price;
            };

            container.appendChild(card);

        });

    });

// ================= LOAD SLOTS =================

fetch("../data/slots.json")
    .then(res => res.json())
    .then(slots => {

        const gymSlots =
            slots.filter(s => s.gym_id == gymId);

        const container =
            document.getElementById("slotList");

        gymSlots.forEach(slot => {

            const card = document.createElement("div");

            card.className = "card";

            // UNAVAILABLE SLOT STYLE

            if (slot.status.toLowerCase() !== "available") {

                card.style.opacity = "0.6";
                card.style.background = "#f5f5f5";
            }

            card.innerHTML = `
        <h3>${slot.slot_time}</h3>
        <p>Status: ${slot.status}</p>
      `;

            // SLOT CLICK

            card.onclick = () => {

                // CHECK SLOT STATUS

                if (slot.status.toLowerCase() !== "available") {

                    alert(
                        "This slot is already booked. Please select another slot."
                    );

                    return;
                }

                document
                    .querySelectorAll("#slotList .card")
                    .forEach(c =>
                        c.classList.remove("selected"));

                card.classList.add("selected");

                selectedSlot = slot;

                document.getElementById("summarySlot")
                    .innerText =
                    "Slot: " + slot.slot_time;
            };

            container.appendChild(card);

        });

    });

// ================= PAYMENT =================

function makePayment() {

    if (!selectedPlan) {

        alert("Please select a plan");

        return;
    }

    if (!selectedSlot) {

        alert("Please select a slot");

        return;
    }

    const booking = {

        gymId: gymId,

        plan: selectedPlan.plan_name,

        price: selectedPlan.price,

        slot: selectedSlot.slot_time,

        date: new Date().toISOString()
    };

    console.log("BOOKING:", booking);

    localStorage.setItem(
        "latestBooking",
        JSON.stringify(booking)
    );

    // REDIRECT

    window.location.href = "payment.html";
}