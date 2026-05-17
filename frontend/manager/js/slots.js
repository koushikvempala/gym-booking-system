async function init() {
  const [users, gyms, slots] = await Promise.all([
    loadData("users"),
    loadData("gyms"),
    loadData("slots")
  ]);

  const manager = users.find(u => u.user_id === CURRENT_MANAGER_ID);
  const myGym = gyms.find(g => g.gym_id === CURRENT_GYM_ID);

  if (manager) setText("managerNameDisplay", manager.name);
  if (myGym) setText("gymNameDisplay", myGym.gym_name);

  function renderSlots() {
    const mySlots = slots.filter(s => s.gym_id === CURRENT_GYM_ID);
    const tbody = document.getElementById("slotsTable");
    
    if (mySlots.length === 0) {
      tbody.innerHTML = `<tr><td colspan="3" class="empty">No slots configured yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = mySlots.map(slot => {
      const isFull = slot.booked >= slot.capacity;
      return `
      <tr>
        <td><strong>${slot.time}</strong></td>
        <td>
          <div style="display: flex; align-items: center; gap: 8px;">
            <div style="flex: 1; height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">
              <div style="height: 100%; width: ${(slot.booked / slot.capacity) * 100}%; background: ${isFull ? 'var(--danger)' : 'var(--brand)'};"></div>
            </div>
            <small style="min-width: 40px; text-align: right;">${slot.booked}/${slot.capacity}</small>
          </div>
        </td>
        <td>
          <span class="badge ${isFull ? 'rejected' : 'approved'}">${isFull ? 'Full' : 'Available'}</span>
        </td>
        <td>
          <div class="actions">
            <button class="btn secondary" onclick="editSlot(${slot.slot_id})">Edit</button>
            <button class="btn danger" onclick="deleteSlot(${slot.slot_id})">Delete</button>
          </div>
        </td>
      </tr>
      `;
    }).join("");
  }

  renderSlots();

  const form = document.getElementById("slotForm");
  const editIdInput = document.getElementById("editId");
  const submitBtn = document.getElementById("submitBtn");
  const cancelBtn = document.getElementById("cancelEditBtn");
  
  window.editSlot = function(id) {
    const slot = slots.find(s => s.slot_id === id);
    if (!slot) return;
    
    document.getElementById("slotTime").value = slot.time;
    document.getElementById("slotCapacity").value = slot.capacity;
    
    editIdInput.value = id;
    submitBtn.textContent = "Update Slot";
    cancelBtn.style.display = "block";
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  
  window.deleteSlot = function(id) {
    if (confirm("Are you sure you want to delete this slot?")) {
      const idx = slots.findIndex(s => s.slot_id === id);
      if (idx !== -1) {
        slots.splice(idx, 1);
        saveData("slots", slots);
        renderSlots();
      }
    }
  };

  cancelBtn.addEventListener("click", () => {
    form.reset();
    editIdInput.value = "";
    submitBtn.textContent = "Create Slot";
    cancelBtn.style.display = "none";
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    const newSlot = {
      slot_id: Date.now(),
      gym_id: CURRENT_GYM_ID,
      time: document.getElementById("slotTime").value,
      capacity: Number(document.getElementById("slotCapacity").value),
      booked: 0
    };

    const editId = editIdInput.value;
    
    if (editId) {
      const idx = slots.findIndex(s => s.slot_id === parseInt(editId));
      if (idx !== -1) {
        slots[idx] = { ...slots[idx], ...newSlot, slot_id: slots[idx].slot_id, booked: slots[idx].booked };
        document.getElementById("saveNotice").textContent = "Slot updated successfully!";
      }
    } else {
      slots.push(newSlot);
      document.getElementById("saveNotice").textContent = "Slot added successfully!";
    }

    saveData("slots", slots);
    
    const notice = document.getElementById("saveNotice");
    notice.classList.add("show");
    setTimeout(() => notice.classList.remove("show"), 3000);
    
    form.reset();
    editIdInput.value = "";
    submitBtn.textContent = "Create Slot";
    cancelBtn.style.display = "none";
    
    renderSlots();
  });
}

document.addEventListener('DOMContentLoaded', init);
