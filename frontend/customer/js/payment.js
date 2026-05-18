let basePrice = 2000;

// TAB SWITCH
function switchTab(event, tabId) {
    document.querySelectorAll(".pay-section")
        .forEach(e => e.style.display = "none");

    document.getElementById(tabId).style.display = "block";

    document.querySelectorAll(".tab")
        .forEach(t => t.classList.remove("active"));

    event.currentTarget.classList.add("active");
}

// PLAN CHANGE
function updatePrice() {
    let plan = document.getElementById("plan");
    basePrice = parseInt(plan.value);

    let text = plan.options[plan.selectedIndex]
        .text.split(" - ")[0];

    document.getElementById("planText").innerText = text;
    document.getElementById("price").innerText = "₹" + basePrice;

    updateTotal(0);
}

// COUPON
function applyCoupon() {
    let code = document.getElementById("coupon").value;
    let discount = 0;

    if (code === "FIT50") discount = 50;
    if (code === "GYM500") discount = 500;

    updateTotal(discount);
}

// TOTAL
function updateTotal(discount) {
    document.getElementById("discount").innerText = "₹" + discount;
    document.getElementById("total").innerText =
        "₹" + (basePrice - discount);
}

// PAYMENT
function payNow() {
    document.getElementById("modal").style.display = "flex";
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}