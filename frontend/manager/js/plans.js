async function init() {
  const [users, gyms, plans] = await Promise.all([
    loadData("users"),
    loadData("gyms"),
    loadData("plans")
  ]);

  const manager = users.find(u => u.user_id === CURRENT_MANAGER_ID);
  const myGym = gyms.find(g => g.gym_id === CURRENT_GYM_ID);

  if (manager) setText("managerNameDisplay", manager.name);
  if (myGym) setText("gymNameDisplay", myGym.gym_name);

  function renderPlans() {
    const myPlans = plans.filter(p => p.gym_id === CURRENT_GYM_ID);
    const tbody = document.getElementById("plansTable");
    
    if (myPlans.length === 0) {
      tbody.innerHTML = `<tr><td colspan="3" class="empty">No plans added yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = myPlans.map(plan => `
      <tr>
        <td><strong>${plan.plan_name}</strong><br><small>${plan.duration} • ${plan.features}</small></td>
        <td><span class="badge ${plan.trainer_included ? 'active' : 'inactive'}">${plan.trainer_included ? 'Yes' : 'No'}</span></td>
        <td><strong>${money(plan.price)}</strong></td>
        <td>
          <div class="actions">
            <button class="btn secondary" onclick="editPlan(${plan.plan_id})">Edit</button>
            <button class="btn danger" onclick="deletePlan(${plan.plan_id})">Delete</button>
          </div>
        </td>
      </tr>
    `).join("");
  }

  renderPlans();

  const form = document.getElementById("planForm");
  const editIdInput = document.getElementById("editId");
  const submitBtn = document.getElementById("submitBtn");
  const cancelBtn = document.getElementById("cancelEditBtn");
  
  window.editPlan = function(id) {
    const plan = plans.find(p => p.plan_id === id);
    if (!plan) return;
    
    document.getElementById("planName").value = plan.plan_name;
    document.getElementById("planDuration").value = plan.duration;
    document.getElementById("planPrice").value = plan.price;
    document.getElementById("planTrainer").value = plan.trainer_included ? "true" : "false";
    document.getElementById("planFeatures").value = plan.features;
    
    editIdInput.value = id;
    submitBtn.textContent = "Update Plan";
    cancelBtn.style.display = "block";
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  
  window.deletePlan = function(id) {
    if (confirm("Are you sure you want to delete this plan?")) {
      const idx = plans.findIndex(p => p.plan_id === id);
      if (idx !== -1) {
        plans.splice(idx, 1);
        saveData("plans", plans);
        renderPlans();
      }
    }
  };

  cancelBtn.addEventListener("click", () => {
    form.reset();
    editIdInput.value = "";
    submitBtn.textContent = "Create Plan";
    cancelBtn.style.display = "none";
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    const newPlan = {
      plan_id: Date.now(),
      gym_id: CURRENT_GYM_ID,
      plan_name: document.getElementById("planName").value,
      duration: document.getElementById("planDuration").value,
      price: Number(document.getElementById("planPrice").value),
      trainer_included: document.getElementById("planTrainer").value === "true",
      features: document.getElementById("planFeatures").value
    };

    const editId = editIdInput.value;
    
    if (editId) {
      const idx = plans.findIndex(p => p.plan_id === parseInt(editId));
      if (idx !== -1) {
        plans[idx] = { ...plans[idx], ...newPlan, plan_id: plans[idx].plan_id };
        document.getElementById("saveNotice").textContent = "Plan updated successfully!";
      }
    } else {
      plans.push(newPlan);
      document.getElementById("saveNotice").textContent = "Plan added successfully!";
    }

    saveData("plans", plans);
    
    const notice = document.getElementById("saveNotice");
    notice.classList.add("show");
    setTimeout(() => notice.classList.remove("show"), 3000);
    
    form.reset();
    editIdInput.value = "";
    submitBtn.textContent = "Create Plan";
    cancelBtn.style.display = "none";
    
    renderPlans();
  });
}

document.addEventListener('DOMContentLoaded', init);
