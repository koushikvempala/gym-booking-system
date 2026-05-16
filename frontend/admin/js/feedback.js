const fallback = {
  users: [
    { user_id: 4, name: "Neha Kapoor" },
    { user_id: 5, name: "Karan Patel" }
  ],
  feedback: [
    { feedback_id: 401, user_id: 4, message: "Booking was quick and the gym staff was helpful.", rating: 5, status: "new", created_at: "2026-05-04" },
    { feedback_id: 402, user_id: 5, message: "Payment page needs clearer confirmation after success.", rating: 3, status: "reviewed", created_at: "2026-05-06" },
    { feedback_id: 403, user_id: 4, message: "Please add more morning slots for personal training.", rating: 4, status: "new", created_at: "2026-05-10" }
  ]
};

let users = [];
let feedback = [];

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
    return (window.GYM_BOOKING_DATA && window.GYM_BOOKING_DATA[name]) || fallback[name] || [];
  }
}

function saveFeedback() {
  localStorage.setItem("gymBookOffice.feedback", JSON.stringify(feedback));
}

function showNotice(message) {
  const notice = document.getElementById("notice");
  notice.textContent = message;
  notice.classList.add("show");
  window.setTimeout(() => notice.classList.remove("show"), 2400);
}

function stars(value) {
  return `${"★".repeat(Number(value))}${"☆".repeat(5 - Number(value))}`;
}

function renderFeedback() {
  const rating = document.getElementById("ratingFilter").value;
  const status = document.getElementById("statusFilter").value;
  const names = new Map(users.map((user) => [user.user_id, user.name]));
  const filtered = feedback.filter((item) => {
    const ratingMatch = rating === "all" || String(item.rating) === rating;
    const statusMatch = status === "all" || item.status === status;
    return ratingMatch && statusMatch;
  });

  const sorted = [...filtered].sort((a, b) => {
    const dateCompare = String(b.created_at || "").localeCompare(String(a.created_at || ""));
    return dateCompare || Number(b.feedback_id) - Number(a.feedback_id);
  });

  document.getElementById("feedbackRows").innerHTML = sorted.length ? sorted.map((item) => `
    <tr>
      <td>#${item.feedback_id}</td>
      <td>${names.get(item.user_id) || "User"}<br><small>${item.created_at || ""}</small></td>
      <td>${item.message}</td>
      <td>${stars(item.rating)}</td>
      <td><span class="badge ${item.status}">${item.status}</span></td>
      <td><div class="actions"><button class="btn secondary wide-action" data-toggle="${item.feedback_id}">${item.status === "reviewed" ? "Mark New" : "Mark Reviewed"}</button><button class="btn danger" data-delete="${item.feedback_id}">Delete</button></div></td>
    </tr>
  `).join("") : `<tr><td colspan="6" class="empty">No feedback matches your filters.</td></tr>`;
}

document.getElementById("feedbackRows").addEventListener("click", (event) => {
  const toggleId = Number(event.target.dataset.toggle);
  const deleteId = Number(event.target.dataset.delete);
  if (toggleId) {
    feedback = feedback.map((item) => item.feedback_id === toggleId ? { ...item, status: item.status === "reviewed" ? "new" : "reviewed" } : item);
    saveFeedback();
    renderFeedback();
    showNotice("Feedback status changed.");
  }
  if (deleteId) {
    feedback = feedback.filter((item) => item.feedback_id !== deleteId);
    saveFeedback();
    renderFeedback();
    showNotice("Feedback deleted.");
  }
});

document.getElementById("ratingFilter").addEventListener("change", renderFeedback);
document.getElementById("statusFilter").addEventListener("change", renderFeedback);
document.getElementById("clearFilters").addEventListener("click", () => {
  document.getElementById("ratingFilter").value = "all";
  document.getElementById("statusFilter").value = "all";
  renderFeedback();
});

Promise.all([loadData("users"), loadData("feedback")]).then(([userData, feedbackData]) => {
  users = userData;
  feedback = feedbackData;
  renderFeedback();
});

