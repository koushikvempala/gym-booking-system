const fallbackData = {
  users: [
    { user_id: 2, name: "Riya Sharma", role: "manager" },
    { user_id: 3, name: "Arjun Mehta", role: "manager" },
    { user_id: 4, name: "Neha Kapoor", role: "customer" },
    { user_id: 5, name: "Karan Patel", role: "customer" },
    { user_id: 6, name: "Sneha Iyer", role: "manager" }
  ],
  gyms: [
    { gym_id: 101, manager_id: 2, gym_name: "Iron Pulse Fitness", address: "MG Road, Bengaluru", description: "Strength training, cardio, Zumba, and personal training.", status: "approved" },
    { gym_id: 102, manager_id: 3, gym_name: "FitNest Studio", address: "Andheri West, Mumbai", description: "Boutique gym with yoga, pilates, and functional training.", status: "approved" },
    { gym_id: 103, manager_id: 6, gym_name: "CoreLab Gym", address: "Anna Nagar, Chennai", description: "New manager enrollment awaiting admin review.", status: "pending" },
    { gym_id: 104, manager_id: 2, gym_name: "FlexForge Arena", address: "Baner, Pune", description: "Crossfit, boxing, and conditioning programs.", status: "rejected" }
  ],
  bookings: [
    { booking_id: 301, customer_id: 4, gym_id: 101, slot: "06:00 AM - 07:00 AM", membership_type: "3 Months - With Trainer", trainer_required: true, total_amount: 7999, payment_status: "paid" },
    { booking_id: 302, customer_id: 5, gym_id: 102, slot: "07:00 PM - 08:00 PM", membership_type: "1 Month - Without Trainer", trainer_required: false, total_amount: 1499, payment_status: "paid" },
    { booking_id: 303, customer_id: 4, gym_id: 101, slot: "08:00 AM - 09:00 AM", membership_type: "12 Months - With Trainer", trainer_required: true, total_amount: 19999, payment_status: "paid" }
  ],
  trainers: [
    { trainer_id: 501, gym_id: 101, trainer_name: "Dev Singh" },
    { trainer_id: 502, gym_id: 102, trainer_name: "Maya Rao" },
    { trainer_id: 503, gym_id: 101, trainer_name: "Kabir Khan" }
  ]
};

const money = (value) => `Rs ${Number(value || 0).toLocaleString("en-IN")}`;
let users = [];
let gyms = [];
let bookings = [];
let trainers = [];

async function loadData(name) {
  const saved = localStorage.getItem(`gymBookOffice.${name}`);
  if (saved) return JSON.parse(saved);
  try {
    const response = await fetch(`data/${name}.json`);
    if (!response.ok) throw new Error("Data unavailable");
    const data = await response.json();
    localStorage.setItem(`gymBookOffice.${name}`, JSON.stringify(data));
    return data;
  } catch {
    return (window.GYM_BOOKING_DATA && window.GYM_BOOKING_DATA[name]) || fallbackData[name] || [];
  }
}

function saveGyms() {
  localStorage.setItem("gymBookOffice.gyms", JSON.stringify(gyms));
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
  setText("trainerCount", trainers.length);

  const revenueByGym = gyms.map((gym) => {
      const value = bookings.filter((booking) => booking.gym_id === gym.gym_id && booking.payment_status === "paid").reduce((sum, booking) => sum + Number(booking.total_amount || 0), 0);
    return { label: gym.gym_name, value, display: money(value) };
  });
  renderBars("revenueBars", revenueByGym);

  const planCounts = [...new Set(bookings.map((booking) => booking.membership_type))].map((plan) => ({
    label: plan,
    value: bookings.filter((booking) => booking.membership_type === plan).length
  }));
  renderBars("planBars", planCounts);

  const rows = document.getElementById("bookingRows");
  if (rows) {
    rows.innerHTML = bookings.map((booking) => `
      <tr>
        <td>#${booking.booking_id}</td>
        <td>${userNames.get(booking.customer_id) || "Customer"}</td>
        <td>${gymNames.get(booking.gym_id) || "Gym"}</td>
        <td>${booking.slot}</td>
        <td>${booking.membership_type}</td>
        <td>${booking.trainer_required ? "Yes" : "No"}</td>
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

Promise.all([loadData("users"), loadData("gyms"), loadData("bookings"), loadData("trainers")]).then((data) => {
  [users, gyms, bookings, trainers] = data;
  renderReports();
  bindGymApprovals();
  renderGymApprovals();
});

