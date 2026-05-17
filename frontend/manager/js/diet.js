async function init() {
  const [users, gyms, dietplans] = await Promise.all([
    loadData("users"),
    loadData("gyms"),
    loadData("dietplans")
  ]);

  const manager = users.find(u => u.user_id === CURRENT_MANAGER_ID);
  const myGym = gyms.find(g => g.gym_id === CURRENT_GYM_ID);

  if (manager) setText("managerNameDisplay", manager.name);
  if (myGym) setText("gymNameDisplay", myGym.gym_name);

  function renderDietPlans() {
    const myDietPlans = dietplans.filter(d => d.gym_id === CURRENT_GYM_ID);
    const tbody = document.getElementById("dietTable");
    
    if (myDietPlans.length === 0) {
      tbody.innerHTML = `<tr><td colspan="3" class="empty">No diet plans available.</td></tr>`;
      return;
    }

    tbody.innerHTML = myDietPlans.map(diet => `
      <tr>
        <td>
          <strong>${diet.plan_name}</strong>
          <br><small>${diet.calories} kcal/day</small>
        </td>
        <td><span class="badge active">${diet.goal}</span></td>
        <td>
          <div class="actions">
            <button class="btn secondary" onclick="window.editDiet(${diet.diet_id})">Edit</button>
            <button class="btn danger" onclick="window.deleteDiet(${diet.diet_id})">Delete</button>
          </div>
        </td>
      </tr>
    `).join("");
  }

  window.editDiet = function(id) {
    const diet = dietplans.find(d => d.diet_id === id);
    if (!diet) return;

    document.getElementById("formTitle").innerText = "Edit Diet Plan";
    document.getElementById("editDietId").value = diet.diet_id;
    document.getElementById("dietName").value = diet.plan_name;
    document.getElementById("dietCalories").value = diet.calories;
    document.getElementById("dietGoal").value = diet.goal;
    document.getElementById("dietDetails").value = diet.details || "";
    
    document.getElementById("submitBtn").innerText = "Update Plan";
    document.getElementById("cancelEditBtn").style.display = "block";
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  window.deleteDiet = function(id) {
    if (confirm("Are you sure you want to delete this diet plan?")) {
      const idx = dietplans.findIndex(d => d.diet_id === id);
      if (idx !== -1) {
        dietplans.splice(idx, 1);
        saveData("dietplans", dietplans);
        renderDietPlans();
      }
    }
  };

  document.getElementById("cancelEditBtn").addEventListener("click", () => {
    document.getElementById("formTitle").innerText = "Add New Diet Plan";
    document.getElementById("editDietId").value = "";
    document.getElementById("dietForm").reset();
    document.getElementById("submitBtn").innerText = "Save Plan";
    document.getElementById("cancelEditBtn").style.display = "none";
  });

  renderDietPlans();

  const form = document.getElementById("dietForm");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    const editId = document.getElementById("editDietId").value;
    
    if (editId) {
      // Edit existing
      const index = dietplans.findIndex(d => d.diet_id == editId);
      if (index > -1) {
        dietplans[index].plan_name = document.getElementById("dietName").value;
        dietplans[index].calories = Number(document.getElementById("dietCalories").value);
        dietplans[index].goal = document.getElementById("dietGoal").value;
        dietplans[index].details = document.getElementById("dietDetails").value;
      }
    } else {
      // Add new
      const newDiet = {
        diet_id: Date.now(),
        gym_id: CURRENT_GYM_ID,
        plan_name: document.getElementById("dietName").value,
        calories: Number(document.getElementById("dietCalories").value),
        goal: document.getElementById("dietGoal").value,
        details: document.getElementById("dietDetails").value
      };
      dietplans.push(newDiet);
    }

    saveData("dietplans", dietplans);
    
    const notice = document.getElementById("saveNotice");
    notice.classList.add("show");
    setTimeout(() => notice.classList.remove("show"), 3000);
    
    document.getElementById("cancelEditBtn").click(); // Reset form state
    renderDietPlans();
  });
}

document.addEventListener('DOMContentLoaded', init);
