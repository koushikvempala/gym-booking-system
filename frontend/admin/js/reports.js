const fallbackData = {
  users: [
    { user_id: 2, name: "Riya Sharma", role: "manager" },
    { user_id: 3, name: "Arjun Mehta", role: "manager" },
    { user_id: 6, name: "Sneha Iyer", role: "manager" }
  ],
  gyms: [
    { gym_id: 101, manager_id: 2, gym_name: "Iron Pulse Fitness", address: "MG Road, Bengaluru", description: "Strength training, cardio, Zumba, and personal training.", status: "approved" },
    { gym_id: 102, manager_id: 3, gym_name: "FitNest Studio", address: "Andheri West, Mumbai", description: "Boutique gym with yoga, pilates, and functional training.", status: "approved" },
    { gym_id: 103, manager_id: 6, gym_name: "CoreLab Gym", address: "Anna Nagar, Chennai", description: "New manager enrollment awaiting admin review.", status: "pending" },
    { gym_id: 104, manager_id: 2, gym_name: "FlexForge Arena", address: "Baner, Pune", description: "Crossfit, boxing, and conditioning programs.", status: "rejected" }
  ],
  bookings: [
    { booking_id: 301, manager_id: 2, gym_id: 101, slot: "2026-06-01", enrollment_plan: "12 Months Gym Enrollment", total_amount: 7999, payment_status: "paid" },
    { booking_id: 302, manager_id: 3, gym_id: 102, slot: "2026-08-03", enrollment_plan: "3 Months Gym Enrollment", total_amount: 2499, payment_status: "paid" },
    { booking_id: 303, manager_id: 7, gym_id: 105, slot: "2026-11-08", enrollment_plan: "6 Months Gym Enrollment", total_amount: 4499, payment_status: "paid" }
  ]
};

const money = (value) => `Rs ${Number(value || 0).toLocaleString("en-IN")}`;
let users = [];
let gyms = [];
let bookings = [];

async function loadData(name) {
  const saved = localStorage.getItem(`gymBookEnrollment.${name}`);
  if (saved) return JSON.parse(saved);
  try {
    const response = await fetch(`data/${name}.json`);
    if (!response.ok) throw new Error("Data unavailable");
    const data = await response.json();
    localStorage.setItem(`gymBookEnrollment.${name}`, JSON.stringify(data));
    return data;
  } catch {
    return (window.GYM_BOOKING_DATA && window.GYM_BOOKING_DATA[name]) || fallbackData[name] || [];
  }
}

function saveGyms() {
  localStorage.setItem("gymBookEnrollment.gyms", JSON.stringify(gyms));
}

function showNotice(message) {
  const notice = document.getElementById("notice");
  if (!notice) return;
  notice.textContent = message;
  notice.classList.add("show");
  window.setTimeout(() => notice.classList.remove("show"), 2400);
}

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}

function renderBars(id, items) {
  const wrap = document.getElementById(id);
  if (!wrap) return;
  const max = Math.max(1, ...items.map((item) => item.value));
  wrap.innerHTML = items.map((item) => `
    <div class="bar-row">
      <strong>${item.label}</strong>
      <div class="bar-track"><div class="bar-fill" style="width:${(item.value / max) * 100}%"></div></div>
      <span>${item.display || item.value}</span>
    </div>
  `).join("");
}

function renderReports() {
  const userNames = new Map(users.map((user) => [user.user_id, user.name]));
  const gymNames = new Map(gyms.map((gym) => [gym.gym_id, gym.gym_name]));
  const paidBookings = bookings.filter((booking) => booking.payment_status === "paid");
  const revenue = paidBookings.reduce((sum, booking) => sum + Number(booking.total_amount || 0), 0);
  setText("bookingCount", bookings.length);
  setText("revenueTotal", money(revenue));
  setText("managerCount", users.filter((user) => user.role === "manager").length);
  setText("trainerCount", gyms.filter((gym) => gym.status === "approved").length);

  const revenueByGym = gyms.map((gym) => {
      const value = bookings.filter((booking) => booking.gym_id === gym.gym_id && booking.payment_status === "paid").reduce((sum, booking) => sum + Number(booking.total_amount || 0), 0);
    return { label: gym.gym_name, value, display: money(value) };
  });
  renderBars("revenueBars", revenueByGym);

  const planCounts = [...new Set(bookings.map((booking) => booking.enrollment_plan))].map((plan) => ({
    label: plan,
    value: bookings.filter((booking) => booking.enrollment_plan === plan).length
  }));
  renderBars("planBars", planCounts);

  const rows = document.getElementById("bookingRows");
  if (rows) {
    rows.innerHTML = bookings.map((booking) => `
      <tr>
        <td>#${booking.booking_id}</td>
        <td>${userNames.get(booking.manager_id || booking.customer_id) || "Manager"}</td>
        <td>${gymNames.get(booking.gym_id) || "Gym"}</td>
        <td>${booking.booking_date || ""}</td>
        <td>${booking.slot || ""}</td>
        <td>${booking.enrollment_plan}</td>
        <td><span class="badge ${booking.payment_status === "paid" ? "active" : booking.payment_status === "failed" ? "rejected" : "pending"}">${booking.payment_status || "paid"}</span></td>
        <td>${money(booking.total_amount)}</td>
      </tr>
    `).join("");
  }
}

function renderGymApprovals() {
  const rows = document.getElementById("gymRows");
  if (!rows) return;
  const query = document.getElementById("gymSearch").value.trim().toLowerCase();
  const status = document.getElementById("statusFilter").value;
  const managerNames = new Map(users.map((user) => [user.user_id, user.name]));
  const filtered = gyms.filter((gym) => {
    const queryText = `${gym.gym_name} ${gym.address} ${gym.description}`.toLowerCase();
    const queryMatch = !query || queryText.includes(query);
    const statusMatch = status === "all" || gym.status === status;
    return queryMatch && statusMatch;
  });

  rows.innerHTML = filtered.length ? filtered.map((gym) => `
    <tr>
      <td><strong>${gym.gym_name}</strong><br><small>#${gym.gym_id}</small></td>
      <td>${managerNames.get(gym.manager_id) || "Unassigned"}</td>
      <td>${gym.address}</td>
      <td>${gym.description}</td>
      <td><span class="badge ${gym.status}">${gym.status}</span></td>
      <td><div class="actions"><button class="btn success" data-status="approved" data-id="${gym.gym_id}">Approve</button><button class="btn danger" data-status="rejected" data-id="${gym.gym_id}">Reject</button><button class="btn secondary" data-status="pending" data-id="${gym.gym_id}">Pending</button></div></td>
    </tr>
  `).join("") : `<tr><td colspan="6" class="empty">No gyms found.</td></tr>`;
}

function bindGymApprovals() {
  const rows = document.getElementById("gymRows");
  if (!rows) return;
  rows.addEventListener("click", (event) => {
    const id = Number(event.target.dataset.id);
    const status = event.target.dataset.status;
    if (!id || !status) return;
    gyms = gyms.map((gym) => gym.gym_id === id ? { ...gym, status } : gym);
    saveGyms();
    renderGymApprovals();
    showNotice(`Gym marked as ${status}.`);
  });
  document.getElementById("gymSearch").addEventListener("input", renderGymApprovals);
  document.getElementById("statusFilter").addEventListener("change", renderGymApprovals);
}

Promise.all([loadData("users"), loadData("gyms"), loadData("bookings")]).then((data) => {
  [users, gyms, bookings] = data;
  renderReports();
  bindGymApprovals();
  renderGymApprovals();
});


