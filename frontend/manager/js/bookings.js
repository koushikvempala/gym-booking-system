async function init() {
  const [users, gyms, bookings, plans, slots] = await Promise.all([
    loadData("users"),
    loadData("gyms"),
    loadData("bookings"),
    loadData("plans"),
    loadData("slots")
  ]);

  const manager = users.find(u => u.user_id === CURRENT_MANAGER_ID);
  const myGym = gyms.find(g => g.gym_id === CURRENT_GYM_ID);

  if (manager) setText("managerNameDisplay", manager.name);
  if (myGym) setText("gymNameDisplay", myGym.gym_name);

  const slotMap = new Map(slots.filter(s => s.gym_id === CURRENT_GYM_ID).map(s => [s.slot_id, s]));
  const userMap = new Map(users.map(u => [u.user_id, u.name]));

  function renderBookings() {
    const myBookings = bookings.filter(b => b.gym_id === CURRENT_GYM_ID);
    const tbody = document.getElementById("bookingsTable");
    
    if (myBookings.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="empty">No bookings found.</td></tr>`;
      return;
    }

    tbody.innerHTML = myBookings.slice().reverse().map(booking => {
      const customerName = userMap.get(booking.customer_id) || booking.customer_name || "Walk-in Customer";
      const slotData = slotMap.get(booking.slot_id);
      const slotTime = slotData ? slotData.time : "Any Time";
      
      return `
      <tr>
        <td><strong>#${booking.booking_id}</strong></td>
        <td>${customerName}</td>
        <td>${booking.membership_type}</td>
        <td>${slotTime}</td>
        <td><strong>${money(booking.total_amount)}</strong><br><span class="badge active">Paid</span></td>
        <td><small>${booking.booking_date || new Date().toISOString().split('T')[0]}</small></td>
      </tr>
      `;
    }).join("");
  }

  renderBookings();
}

document.addEventListener('DOMContentLoaded', init);
