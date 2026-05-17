async function init() {
  const [users, gyms] = await Promise.all([
    loadData("users"),
    loadData("gyms")
  ]);

  const manager = users.find(u => u.user_id === CURRENT_MANAGER_ID);
  const myGym = gyms.find(g => g.gym_id === CURRENT_GYM_ID);

  if (manager) setText("managerNameDisplay", manager.name);
  if (myGym) setText("gymNameDisplay", myGym.gym_name);

  window.selectAdminPlan = function(planId, price, planName) {
    document.getElementById("selectedPlanId").value = planId;
    document.getElementById("selectedPlanName").value = planName;
    
    document.querySelectorAll('.plan-card').forEach(c => c.classList.remove('selected'));
    document.getElementById('card-' + planId).classList.add('selected');
    
    document.getElementById("paymentSection").style.display = "block";
    document.getElementById("payAmount").value = price;
    document.getElementById("payBtn").innerText = `Pay ${money(price)} & Subscribe`;
    
    setTimeout(() => {
      document.getElementById("paymentSection").scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 50);
  };

  function renderSubscriptionCards() {
    const adminPlans = [
      { plan_id: 201, plan_name: "Starter License (1 Month)", duration: "1 Month", price: 999, features: "Platform access, up to 100 members, basic support" },
      { plan_id: 202, plan_name: "Pro License (6 Months)", duration: "6 Months", price: 4999, features: "Platform access, unlimited members, priority support" },
      { plan_id: 203, plan_name: "Enterprise License (1 Year)", duration: "12 Months", price: 8999, features: "Custom branding, unlimited members, dedicated manager" }
    ];

    const cardsContainer = document.getElementById("planCards");
    cardsContainer.innerHTML = adminPlans.map(p => {
      const featureList = (p.features || "Platform access").split(",").map(f => `<li>${f.trim()}</li>`).join("");
      return `
      <div class="card plan-card" id="card-${p.plan_id}" onclick="selectAdminPlan(${p.plan_id}, ${p.price}, '${p.plan_name}')" style="display: flex; flex-direction: column;">
        <div class="card-header"><h4 style="margin: 0; color: #1e293b; font-size: 15px;">${p.plan_name}</h4></div>
        <div class="card-body" style="flex: 1; display: flex; flex-direction: column;">
          <h2 style="color: var(--brand); margin-top: 0; margin-bottom: 15px; font-size: 26px;">${money(p.price)}</h2>
          <div style="font-size: 13px; font-weight: 600; color: #64748b; margin-bottom: 5px;">Features:</div>
          <ul style="margin-top: 0; padding-left: 15px; font-size: 13px; color: var(--muted); margin-bottom: 0;">
            ${featureList}
          </ul>
        </div>
      </div>
    `}).join("");
  }

  renderSubscriptionCards();

  const form = document.getElementById("subscriptionForm");
  
  const payMethod = document.getElementById("payMethod");
  const upiFields = document.getElementById("upiFields");
  const upiId = document.getElementById("upiId");
  const cardFields = document.getElementById("cardFields");
  const cardNumber = document.getElementById("cardNumber");
  const cardCvv = document.getElementById("cardCvv");

  payMethod.addEventListener("change", (e) => {
    if (e.target.value === "UPI") {
      upiFields.style.display = "block";
      cardFields.style.display = "none";
      upiId.required = true;
      cardNumber.required = false;
      cardCvv.required = false;
    } else if (e.target.value === "Card") {
      upiFields.style.display = "none";
      cardFields.style.display = "grid";
      upiId.required = false;
      cardNumber.required = true;
      cardCvv.required = true;
    } else {
      upiFields.style.display = "none";
      cardFields.style.display = "none";
      upiId.required = false;
      cardNumber.required = false;
      cardCvv.required = false;
    }
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    const selectedPlanId = document.getElementById("selectedPlanId").value;
    const selectedPlanName = document.getElementById("selectedPlanName").value;
    
    if (!selectedPlanId) {
      alert("Please select a platform subscription plan.");
      return;
    }

    let adminPayments = JSON.parse(localStorage.getItem("gymBookOffice.payments") || "[]");
    
    const newPayment = {
      payment_id: Date.now(),
      gym_id: CURRENT_GYM_ID,
      gym_name: myGym ? myGym.gym_name : "Your Gym",
      manager_name: manager ? manager.name : "Manager",
      plan_name: selectedPlanName,
      amount: Number(document.getElementById("payAmount").value),
      method: document.getElementById("payMethod").value,
      method_detail: document.getElementById("payMethod").value === "UPI" ? upiId.value : ("****" + (cardNumber.value || "0000").slice(-4)),
      date: new Date().toISOString().split('T')[0],
      status: "Active"
    };

    adminPayments.push(newPayment);
    localStorage.setItem("gymBookOffice.payments", JSON.stringify(adminPayments));
    
    const notice = document.getElementById("subscriptionNotice");
    notice.classList.add("show");
    setTimeout(() => notice.classList.remove("show"), 3000);
    
    form.reset();
    upiFields.style.display = "none";
    cardFields.style.display = "none";
    upiId.required = false;
    cardNumber.required = false;
    cardCvv.required = false;

    document.getElementById("selectedPlanId").value = "";
    document.getElementById("selectedPlanName").value = "";
    document.getElementById("paymentSection").style.display = "none";
    document.querySelectorAll('.plan-card').forEach(c => c.classList.remove('selected'));
    document.getElementById("payBtn").innerText = `Pay Admin & Subscribe`;
    
    renderSubscriptionCards();
  });
}

document.addEventListener('DOMContentLoaded', init);
