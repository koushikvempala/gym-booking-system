const fallbackUsers = [
  { user_id: 1, name: "System Admin", email: "admin@gymbook.local", password: "admin123", role: "admin", status: "active", created_at: "2026-01-05" },
  { user_id: 2, name: "Riya Sharma", email: "riya.manager@gymbook.local", password: "manager123", role: "manager", status: "active", created_at: "2026-02-14" },
  { user_id: 3, name: "Arjun Mehta", email: "arjun.manager@gymbook.local", password: "manager123", role: "manager", status: "active", created_at: "2026-03-01" },
  { user_id: 6, name: "Sneha Iyer", email: "sneha.manager@gymbook.local", password: "manager123", role: "manager", status: "pending", created_at: "2026-04-18" }
];

let users = [];

async function loadUsers() {
  const saved = localStorage.getItem("gymBookEnrollment.users");
  if (saved) return JSON.parse(saved);
  try {
    const response = await fetch("data/users.json");
    if (!response.ok) throw new Error("Data unavailable");
    const data = await response.json();
    localStorage.setItem("gymBookEnrollment.users", JSON.stringify(data));
    return data;
  } catch {
    return (window.GYM_BOOKING_DATA && window.GYM_BOOKING_DATA.users) || fallbackUsers;
  }
}

function saveUsers() {
  localStorage.setItem("gymBookEnrollment.users", JSON.stringify(users));
}

function showNotice(message) {
  const notice = document.getElementById("notice");
  notice.textContent = message;
  notice.classList.add("show");
  window.setTimeout(() => notice.classList.remove("show"), 2400);
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidPhone(phone) {
  return /^\+91\s?[6-9]\d{4}\s?\d{5}$/.test(phone);
}

function validateManager(payload, userId) {
  if (payload.name.length < 3) return "Manager name must contain at least 3 characters.";
  if (!/^[A-Za-z ]+$/.test(payload.name)) return "Manager name can contain only letters and spaces.";
  if (!isValidEmail(payload.email)) return "Enter a valid manager email address.";
  if (users.some((user) => user.email.toLowerCase() === payload.email.toLowerCase() && user.user_id !== userId)) return "This email is already registered.";
  if (!isValidPhone(payload.phone)) return "Enter a valid Indian phone number starting with +91 and 6-9.";
  if (payload.city.length < 2 || !/^[A-Za-z ]+$/.test(payload.city)) return "Enter a valid city name.";
  if (payload.password.length < 6) return "Password must contain at least 6 characters.";
  return "";
}

function resetForm() {
  document.getElementById("managerForm").reset();
  document.getElementById("userId").value = "";
}

function renderManagers() {
  const query = document.getElementById("managerSearch").value.trim().toLowerCase();
  const managers = users.filter((user) => user.role === "manager" && `${user.name} ${user.email} ${user.city || ""}`.toLowerCase().includes(query));
  const rows = document.getElementById("managerRows");
  rows.innerHTML = managers.length ? managers.map((manager) => `
    <tr>
      <td>${manager.name}</td>
      <td>${manager.email}</td>
      <td>${manager.city || "-"}</td>
      <td><span class="badge ${manager.status}">${manager.status}</span></td>
      <td><div class="actions"><button class="btn secondary" data-edit="${manager.user_id}">Edit</button><button class="btn danger" data-delete="${manager.user_id}">Delete</button></div></td>
    </tr>
  `).join("") : `<tr><td colspan="5" class="empty">No managers found.</td></tr>`;
}

document.getElementById("managerForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const userId = Number(document.getElementById("userId").value);
  const payload = {
    user_id: userId || Math.max(0, ...users.map((user) => Number(user.user_id))) + 1,
    name: document.getElementById("name").value.trim(),
    email: document.getElementById("email").value.trim(),
    phone: document.getElementById("phone").value.trim(),
    city: document.getElementById("city").value.trim(),
    password: document.getElementById("password").value,
    role: "manager",
    status: document.getElementById("status").value,
    created_at: new Date().toISOString().slice(0, 10)
  };
  const error = validateManager(payload, userId);
  if (error) {
    showNotice(error);
    return;
  }

  if (userId) {
    users = users.map((user) => user.user_id === userId ? { ...user, ...payload, created_at: user.created_at || payload.created_at } : user);
    showNotice("Manager updated.");
  } else {
    users.push(payload);
    showNotice("Manager added.");
  }

  saveUsers();
  resetForm();
  renderManagers();
});

document.getElementById("managerRows").addEventListener("click", (event) => {
  const editId = Number(event.target.dataset.edit);
  const deleteId = Number(event.target.dataset.delete);
  if (editId) {
    const manager = users.find((user) => user.user_id === editId);
    document.getElementById("userId").value = manager.user_id;
    document.getElementById("name").value = manager.name;
    document.getElementById("email").value = manager.email;
    document.getElementById("phone").value = manager.phone || "";
    document.getElementById("city").value = manager.city || "";
    document.getElementById("password").value = manager.password;
    document.getElementById("status").value = manager.status;
  }
  if (deleteId) {
    users = users.filter((user) => user.user_id !== deleteId);
    saveUsers();
    renderManagers();
    showNotice("Manager removed.");
  }
});

document.getElementById("managerSearch").addEventListener("input", renderManagers);
document.getElementById("resetForm").addEventListener("click", resetForm);

loadUsers().then((data) => {
  users = data;
  renderManagers();
});


