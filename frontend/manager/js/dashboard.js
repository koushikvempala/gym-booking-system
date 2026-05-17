async function init() {
  const [users, gyms, bookings, plans, trainers, slots] = await Promise.all([
    loadData("users"),
    loadData("gyms"),
    loadData("bookings"),
    loadData("plans"),
    loadData("trainers"),
    loadData("slots")
  ]);

  const manager = users.find(u => u.user_id === CURRENT_MANAGER_ID);
  const myGym = gyms.find(g => g.gym_id === CURRENT_GYM_ID);
  
  if (manager) {
    setText("managerNameDisplay", manager.name);
  }
  if (myGym) {
    setText("gymNameDisplay", myGym.gym_name);
    setText("heroGymName", `Welcome back, ${myGym.gym_name}!`);
    setText("totalMembers", myGym.members || 0);
  }

  const myBookings = bookings.filter(b => b.gym_id === CURRENT_GYM_ID);
  const paidBookings = myBookings.filter(b => b.payment_status === "paid");
  const revenue = paidBookings.reduce((sum, b) => sum + Number(b.total_amount || 0), 0);
  
  const myPlans = plans.filter(p => p.gym_id === CURRENT_GYM_ID);
  const myTrainers = trainers.filter(t => t.gym_id === CURRENT_GYM_ID);
  const mySlots = slots.filter(s => s.gym_id === CURRENT_GYM_ID);

  setText("liveDate", new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }));
  setText("totalPlans", myPlans.length);
  setText("totalRevenue", money(revenue));
  
  const openSlots = mySlots.filter(s => s.booked < s.capacity);
  const fullSlots = mySlots.filter(s => s.booked >= s.capacity);
  setText("totalSlots", openSlots.length);
  setText("slotsOpen", openSlots.length);
  setText("slotsFull", fullSlots.length);
  setText("totalTrainers", myTrainers.length);

  // Health Score / Occupancy Rate
  let totalCapacity = 0;
  let totalBooked = 0;
  mySlots.forEach(s => {
    totalCapacity += s.capacity;
    totalBooked += s.booked;
  });
  
  const occupancy = totalCapacity > 0 ? Math.round((totalBooked / totalCapacity) * 100) : 0;
  setText("healthScore", `${occupancy}%`);
  setText("healthText", occupancy > 80 ? "High occupancy! Consider adding more slots." : "Healthy slot utilization.");
  
  const ring = document.getElementById("healthScore");
  if (ring) ring.style.background = `conic-gradient(var(--brand) 0 ${occupancy}%, #e2e8f0 ${occupancy}% 100%)`;

  // Render recent bookings
  const rows = document.getElementById("recentBookings");
  const names = new Map(users.map((user) => [user.user_id, user.name]));
  const slotMap = new Map(mySlots.map((s) => [s.slot_id, s.time]));

  rows.innerHTML = myBookings.slice(-5).reverse().map((booking) => `
    <tr>
      <td>#${booking.booking_id}</td>
      <td>${names.get(booking.customer_id) || "Customer"}</td>
      <td>${booking.slot_id ? slotMap.get(booking.slot_id) : "Any Time"}</td>
      <td>${booking.membership_type}<br><small>${booking.booking_date || ""}</small></td>
      <td>${money(booking.total_amount)}<br><span class="badge ${booking.payment_status === "paid" ? "active" : "pending"}">${booking.payment_status || "paid"}</span></td>
    </tr>
  `).join("");

  // Render bars for slots
  const wrap = document.getElementById("approvalBars");
  const max = Math.max(1, mySlots.length);
  wrap.innerHTML = `
    <div class="bar-row"><strong>Full</strong><div class="bar-track"><div class="bar-fill" style="width:${(fullSlots.length / max) * 100}%; background:var(--danger)"></div></div><span>${fullSlots.length} slots</span></div>
    <div class="bar-row"><strong>Open</strong><div class="bar-track"><div class="bar-fill" style="width:${(openSlots.length / max) * 100}%; background:var(--success)"></div></div><span>${openSlots.length} slots</span></div>
  `;
}

document.addEventListener('DOMContentLoaded', init);
