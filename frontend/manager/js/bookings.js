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

  function calculateValidTill(startDate, durationMonths) {
    const validTill = new Date(startDate);
    validTill.setMonth(validTill.getMonth() + durationMonths);

    return validTill; // ✅ return full date object (with time)
  }


  function formatDateTime(date) {
    return new Date(date).toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  }

  // Set up filters
  const searchInput = document.getElementById("searchBooking");
  const filterPlan = document.getElementById("filterPlan");

  // Populate filter dropdown
  const uniquePlans = [...new Set(bookings.filter(b => b.gym_id === CURRENT_GYM_ID).map(b => b.membership_type || b.enrollment_plan || b.plan_name || "Basic Plan"))];
  if (filterPlan) {
    uniquePlans.forEach(plan => {
      const opt = document.createElement("option");
      opt.value = plan;
      opt.textContent = plan;
      filterPlan.appendChild(opt);
    });
  }

  if (searchInput) searchInput.addEventListener("input", renderBookings);
  if (filterPlan) filterPlan.addEventListener("change", renderBookings);

  function renderBookings() {
    let myBookings = bookings.filter(b => b.gym_id === CURRENT_GYM_ID);
    const tbody = document.getElementById("bookingsTable");
    
    if (searchInput && filterPlan) {
      const query = searchInput.value.toLowerCase();
      const planFilter = filterPlan.value;
      
      if (query) {
        myBookings = myBookings.filter(b => {
          const cName = (userMap.get(b.customer_id) || b.customer_name || "Walk-in Customer").toLowerCase();
          return cName.includes(query) || b.booking_id.toString().includes(query);
        });
      }
      if (planFilter) {
        myBookings = myBookings.filter(b => {
          const pName = b.membership_type || b.enrollment_plan || b.plan_name || "Basic Plan";
          return pName === planFilter;
        });
      }
    }

    if (myBookings.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="empty" style="text-align: center; padding: 20px;">No bookings found matching filters.</td></tr>`;
      return;
    }

    tbody.innerHTML = myBookings.slice().reverse().map(booking => {
      const customerName = userMap.get(booking.customer_id) || booking.customer_name || "Walk-in Customer";
      const slotData = slotMap.get(booking.slot_id);
      const slotTime = slotData ? slotData.time : (booking.slot || "Any Time");
      
      const planName = booking.membership_type || booking.enrollment_plan || booking.plan_name || "Basic Plan";
      
      let durationMonths = 1;
      const lowerPlan = planName.toLowerCase();
      if (lowerPlan.includes("3 month")) durationMonths = 3;
      else if (lowerPlan.includes("6 month")) durationMonths = 6;
      else if (lowerPlan.includes("9 month")) durationMonths = 9;
      else if (lowerPlan.includes("12 month") || lowerPlan.includes("1 year") || lowerPlan.includes("annual")) durationMonths = 12;

      const startDate = booking.booking_date || booking.date || new Date();
      const validTill = calculateValidTill(startDate, durationMonths);

      return `
      <tr>
        <td><strong>#${booking.booking_id}</strong></td>
        <td>${customerName}</td>
        <td>${planName}</td>
        <td>${formatDateTime(startDate)}</td>
        <td>${formatDateTime(validTill)}</td>
        <td>${slotTime}</td>
        <td><strong>${money(booking.total_amount)}</strong><br><span class="badge active">Paid</span></td>
      </tr>
      `;
    }).join("");
  }

  renderBookings();
}

document.addEventListener('DOMContentLoaded', init);