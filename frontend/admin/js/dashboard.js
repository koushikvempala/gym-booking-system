const seed = {
  users: [],
  gyms: [],
  bookings: [],
  feedback: []
};

const storeKey = (name) => `gymBookOffice.${name}`;
const money = (value) => `Rs ${Number(value || 0).toLocaleString("en-IN")}`;

async function loadData(name) {
  const saved = localStorage.getItem(storeKey(name));
  if (saved) return JSON.parse(saved);
  try {
    const response = await fetch(`data/${name}.json`);
    if (!response.ok) throw new Error("Data unavailable");
    const data = await response.json();
    localStorage.setItem(storeKey(name), JSON.stringify(data));
    return data;
  } catch {
    return (window.GYM_BOOKING_DATA && window.GYM_BOOKING_DATA[name]) || seed[name] || [];
  }
}

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}

function renderBars(gyms) {
  const wrap = document.getElementById("approvalBars");
  const statuses = ["approved", "pending", "rejected"];
  const max = Math.max(1, gyms.length);
  wrap.innerHTML = statuses.map((status) => {
    const count = gyms.filter((gym) => gym.status === status).length;
    return `<div class="bar-row"><strong>${status}</strong><div class="bar-track"><div class="bar-fill" style="width:${(count / max) * 100}%"></div></div><span>${count} gyms</span></div>`;
  }).join("");
}

function renderBookings(bookings, users, gyms) {
  const rows = document.getElementById("recentBookings");
  const names = new Map(users.map((user) => [user.user_id, user.name]));
  const gymNames = new Map(gyms.map((gym) => [gym.gym_id, gym.gym_name]));
  rows.innerHTML = bookings.slice(-7).reverse().map((booking) => `
    <tr>
      <td>#${booking.booking_id}</td>
      <td>${names.get(booking.customer_id) || "Customer"}</td>
      <td>${gymNames.get(booking.gym_id) || "Gym"}</td>
      <td>${booking.membership_type}<br><small>${booking.booking_date || ""}</small></td>
      <td>${money(booking.total_amount)}<br><span class="badge ${booking.payment_status === "paid" ? "active" : "pending"}">${booking.payment_status || "paid"}</span></td>
    </tr>
  `).join("");
}

function renderTopGyms(gyms, bookings) {
  const wrap = document.getElementById("topGyms");
  const ranked = gyms
    .filter((gym) => gym.status === "approved")
    .map((gym) => {
      const revenue = bookings.filter((booking) => booking.gym_id === gym.gym_id && booking.payment_status === "paid")
        .reduce((sum, booking) => sum + Number(booking.total_amount || 0), 0);
      return { ...gym, revenue };
    })
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 5);

  wrap.innerHTML = ranked.map((gym) => `
    <div class="mini-item">
      <div><strong>${gym.gym_name}</strong><span>${gym.address}</span></div>
      <div><strong>${money(gym.revenue)}</strong><small>${gym.members || 0} members</small></div>
    </div>
  `).join("");
}

function renderFeedback(feedback, users) {
  const wrap = document.getElementById("recentFeedback");
  const names = new Map(users.map((user) => [user.user_id, user.name]));
  wrap.innerHTML = feedback.slice(-5).reverse().map((item) => `
    <div class="mini-item">
      <div><strong>${names.get(item.user_id) || "Customer"}</strong><span>${item.message}</span></div>
      <div><strong>${item.rating}/5</strong><small>${item.status}</small></div>
    </div>
  `).join("");
}

function renderHealth(gyms, bookings, feedback) {
  const approvedRatio = gyms.length ? gyms.filter((gym) => gym.status === "approved").length / gyms.length : 0;
  const paidRatio = bookings.length ? bookings.filter((booking) => booking.payment_status === "paid").length / bookings.length : 0;
  const avgRating = feedback.length ? feedback.reduce((sum, item) => sum + Number(item.rating || 0), 0) / feedback.length : 0;
  const score = Math.round(((approvedRatio * 0.35) + (paidRatio * 0.35) + ((avgRating / 5) * 0.30)) * 100);
  setText("healthScore", `${score}%`);
  setText("healthText", score >= 80 ? "Strong platform activity with healthy payments and customer ratings." : "Good activity, with pending approvals and service follow-ups to monitor.");
  const ring = document.getElementById("healthScore");
  if (ring) ring.style.background = `conic-gradient(var(--success) 0 ${score}%, #e5edf0 ${score}% 100%)`;
}

async function init() {
  const [users, gyms, bookings, feedback] = await Promise.all([
    loadData("users"),
    loadData("gyms"),
    loadData("bookings"),
    loadData("feedback")
  ]);

  const paidBookings = bookings.filter((booking) => booking.payment_status === "paid");
  const revenue = paidBookings.reduce((sum, booking) => sum + Number(booking.total_amount || 0), 0);
  const avgRating = feedback.length ? feedback.reduce((sum, item) => sum + Number(item.rating || 0), 0) / feedback.length : 0;

  setText("liveDate", `Updated May 15, 2026`);
  setText("totalUsers", users.length);
  setText("approvedGyms", gyms.filter((gym) => gym.status === "approved").length);
  setText("totalRevenue", money(revenue));
  setText("avgRating", avgRating.toFixed(1));
  setText("pendingGyms", gyms.filter((gym) => gym.status === "pending").length);
  setText("managerCount", users.filter((user) => user.role === "manager").length);
  setText("paidBookings", paidBookings.length);

  renderHealth(gyms, bookings, feedback);
  renderBars(gyms);
  renderBookings(bookings, users, gyms);
  renderTopGyms(gyms, bookings);
  renderFeedback(feedback, users);
}

init();

