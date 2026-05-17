const fallbackPlans = [
  { plan_id: 201, plan_name: "1 Month Gym Enrollment", duration: "1 Month", price: 999, features: "Gym listing, manager dashboard access, approval support, basic visibility" },
  { plan_id: 202, plan_name: "3 Months Gym Enrollment", duration: "3 Months", price: 2499, features: "Gym listing, dashboard access, approval support, priority visibility" },
  { plan_id: 203, plan_name: "6 Months Gym Enrollment", duration: "6 Months", price: 4499, features: "Gym listing, dashboard access, priority visibility, monthly performance summary" },
  { plan_id: 204, plan_name: "9 Months Gym Enrollment", duration: "9 Months", price: 6499, features: "Gym listing, priority visibility, manager analytics, extended approval support" },
  { plan_id: 205, plan_name: "12 Months Gym Enrollment", duration: "12 Months", price: 7999, features: "Annual gym listing, premium visibility, manager analytics, renewal support" }
];

const allowedPlans = {
  "1 Month Gym Enrollment": { duration: "1 Month" },
  "3 Months Gym Enrollment": { duration: "3 Months" },
  "6 Months Gym Enrollment": { duration: "6 Months" },
  "9 Months Gym Enrollment": { duration: "9 Months" },
  "12 Months Gym Enrollment": { duration: "12 Months" }
};

let plans = [];
const money = (value) => `Rs ${Number(value || 0).toLocaleString("en-IN")}`;

async function loadPlans() {
  const saved = localStorage.getItem("gymBookEnrollment.plans");
  if (saved) return JSON.parse(saved);
  try {
    const response = await fetch("data/plans.json");
    if (!response.ok) throw new Error("Data unavailable");
    const data = await response.json();
    localStorage.setItem("gymBookEnrollment.plans", JSON.stringify(data));
    return data;
  } catch {
    return (window.GYM_BOOKING_DATA && window.GYM_BOOKING_DATA.plans) || fallbackPlans;
  }
}

function savePlans() {
  localStorage.setItem("gymBookEnrollment.plans", JSON.stringify(plans));
}

function showNotice(message) {
  const notice = document.getElementById("notice");
  notice.textContent = message;
  notice.classList.add("show");
  window.setTimeout(() => notice.classList.remove("show"), 2400);
}

function validatePlan(payload, planId) {
  const allowed = allowedPlans[payload.plan_name];
  if (!allowed) return "Select one of the five official gym enrollment plans.";
  if (allowed.duration !== payload.duration) return "Plan duration must match the selected enrollment plan.";
  if (!Number.isFinite(payload.price) || payload.price < 500) return "Plan price must be at least Rs 500.";
  if (payload.features.length < 15) return "Add clear plan features with at least 15 characters.";
  if (plans.some((plan) => plan.plan_name === payload.plan_name && plan.plan_id !== planId)) return "This enrollment plan already exists.";
  return "";
}

function resetForm() {
  document.getElementById("planForm").reset();
  document.getElementById("planId").value = "";
}

function renderPlans() {
  const rows = document.getElementById("planRows");
  rows.innerHTML = plans.length ? plans.map((plan) => `
    <tr>
      <td>${plan.plan_name}</td>
      <td>${plan.duration}</td>
      <td>${money(plan.price)}</td>
      <td>${plan.features}</td>
      <td><div class="actions"><button class="btn secondary" data-edit="${plan.plan_id}">Edit</button></div></td>
    </tr>
  `).join("") : `<tr><td colspan="5" class="empty">No plans added.</td></tr>`;
}

document.getElementById("planForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const planId = Number(document.getElementById("planId").value);
  const payload = {
    plan_id: planId || Math.max(200, ...plans.map((plan) => Number(plan.plan_id))) + 1,
    plan_name: document.getElementById("planName").value.trim(),
    duration: document.getElementById("duration").value.trim(),
    price: Number(document.getElementById("price").value),
    features: document.getElementById("features").value.trim()
  };
  const error = validatePlan(payload, planId);
  if (error) {
    showNotice(error);
    return;
  }
  if (planId) {
    plans = plans.map((plan) => plan.plan_id === planId ? payload : plan);
    showNotice("Enrollment plan updated.");
  } else {
    plans.push(payload);
    showNotice("Enrollment plan added.");
  }
  savePlans();
  resetForm();
  renderPlans();
});

document.getElementById("planRows").addEventListener("click", (event) => {
  const editId = Number(event.target.dataset.edit);
  if (editId) {
    const plan = plans.find((item) => item.plan_id === editId);
    document.getElementById("planId").value = plan.plan_id;
    document.getElementById("planName").value = plan.plan_name;
    document.getElementById("duration").value = plan.duration;
    document.getElementById("price").value = plan.price;
    document.getElementById("features").value = plan.features;
  }
});

document.getElementById("resetForm").addEventListener("click", resetForm);
document.getElementById("planName").addEventListener("change", (event) => {
  const selected = allowedPlans[event.target.value];
  if (selected) document.getElementById("duration").value = selected.duration;
});

loadPlans().then((data) => {
  plans = data;
  renderPlans();
});

