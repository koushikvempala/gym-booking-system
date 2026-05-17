async function init() {
  const [users, gyms, equipment] = await Promise.all([
    loadData("users"),
    loadData("gyms"),
    loadData("equipment")
  ]);

  const manager = users.find(u => u.user_id === CURRENT_MANAGER_ID);
  const myGym = gyms.find(g => g.gym_id === CURRENT_GYM_ID);

  if (manager) setText("managerNameDisplay", manager.name);
  if (myGym) setText("gymNameDisplay", myGym.gym_name);

  function renderEquipment() {
    const myEquipment = equipment.filter(e => e.gym_id === CURRENT_GYM_ID);
    const tbody = document.getElementById("equipmentTable");
    
    if (myEquipment.length === 0) {
      tbody.innerHTML = `<tr><td colspan="3" class="empty">No equipment added yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = myEquipment.map(eq => `
      <tr>
        <td><strong>${eq.name}</strong></td>
        <td>${eq.quantity}</td>
        <td><span class="badge ${eq.condition === 'Needs Maintenance' ? 'rejected' : (eq.condition === 'Excellent' ? 'approved' : 'active')}">${eq.condition}</span></td>
        <td>
          <div class="actions">
            <button class="btn secondary" onclick="editEquipment(${eq.equipment_id})">Edit</button>
            <button class="btn danger" onclick="deleteEquipment(${eq.equipment_id})">Delete</button>
          </div>
        </td>
      </tr>
    `).join("");
  }

  renderEquipment();

  const form = document.getElementById("equipmentForm");
  const editIdInput = document.getElementById("editId");
  const submitBtn = document.getElementById("submitBtn");
  const cancelBtn = document.getElementById("cancelEditBtn");
  
  window.editEquipment = function(id) {
    const eq = equipment.find(e => e.equipment_id === id);
    if (!eq) return;
    
    document.getElementById("equipmentName").value = eq.name;
    document.getElementById("equipmentQty").value = eq.quantity;
    document.getElementById("equipmentCondition").value = eq.condition;
    
    editIdInput.value = id;
    submitBtn.textContent = "Update Equipment";
    cancelBtn.style.display = "block";
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  
  window.deleteEquipment = function(id) {
    if (confirm("Are you sure you want to delete this equipment?")) {
      const idx = equipment.findIndex(e => e.equipment_id === id);
      if (idx !== -1) {
        equipment.splice(idx, 1);
        saveData("equipment", equipment);
        renderEquipment();
      }
    }
  };

  cancelBtn.addEventListener("click", () => {
    form.reset();
    editIdInput.value = "";
    submitBtn.textContent = "Add Equipment";
    cancelBtn.style.display = "none";
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    const newEquipment = {
      equipment_id: Date.now(),
      gym_id: CURRENT_GYM_ID,
      name: document.getElementById("equipmentName").value,
      quantity: Number(document.getElementById("equipmentQty").value),
      condition: document.getElementById("equipmentCondition").value
    };

    const editId = editIdInput.value;
    
    if (editId) {
      const idx = equipment.findIndex(e => e.equipment_id === parseInt(editId));
      if (idx !== -1) {
        equipment[idx] = { ...equipment[idx], ...newEquipment, equipment_id: equipment[idx].equipment_id };
        document.getElementById("saveNotice").textContent = "Equipment updated successfully!";
      }
    } else {
      equipment.push(newEquipment);
      document.getElementById("saveNotice").textContent = "Equipment added successfully!";
    }

    saveData("equipment", equipment);
    
    const notice = document.getElementById("saveNotice");
    notice.classList.add("show");
    setTimeout(() => notice.classList.remove("show"), 3000);
    
    form.reset();
    editIdInput.value = "";
    submitBtn.textContent = "Add Equipment";
    cancelBtn.style.display = "none";
    
    renderEquipment();
  });
}

document.addEventListener('DOMContentLoaded', init);
