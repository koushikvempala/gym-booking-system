async function init() {
  const [users, gyms, trainers] = await Promise.all([
    loadData("users"),
    loadData("gyms"),
    loadData("trainers")
  ]);

  const manager = users.find(u => u.user_id === CURRENT_MANAGER_ID);
  const myGym = gyms.find(g => g.gym_id === CURRENT_GYM_ID);

  if (manager) setText("managerNameDisplay", manager.name);
  if (myGym) setText("gymNameDisplay", myGym.gym_name);

  function renderTrainers() {
    const myTrainers = trainers.filter(t => t.gym_id === CURRENT_GYM_ID);
    const tbody = document.getElementById("trainersTable");
    
    if (myTrainers.length === 0) {
      tbody.innerHTML = `<tr><td colspan="3" class="empty">No trainers added yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = myTrainers.map(trainer => `
      <tr>
        <td><strong>${trainer.trainer_name}</strong></td>
        <td>${trainer.specialization}</td>
        <td>${trainer.experience_years} Years</td>
        <td>
          <div class="actions">
            <button class="btn secondary" onclick="editTrainer(${trainer.trainer_id})">Edit</button>
            <button class="btn danger" onclick="deleteTrainer(${trainer.trainer_id})">Delete</button>
          </div>
        </td>
      </tr>
    `).join("");
  }

  renderTrainers();

  const form = document.getElementById("trainerForm");
  const editIdInput = document.getElementById("editId");
  const submitBtn = document.getElementById("submitBtn");
  const cancelBtn = document.getElementById("cancelEditBtn");
  
  window.editTrainer = function(id) {
    const trainer = trainers.find(t => t.trainer_id === id);
    if (!trainer) return;
    
    document.getElementById("trainerName").value = trainer.trainer_name;
    document.getElementById("trainerSpecialization").value = trainer.specialization;
    document.getElementById("trainerExperience").value = trainer.experience_years;
    
    editIdInput.value = id;
    submitBtn.textContent = "Update Trainer";
    cancelBtn.style.display = "block";
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  
  window.deleteTrainer = function(id) {
    if (confirm("Are you sure you want to delete this trainer?")) {
      const idx = trainers.findIndex(t => t.trainer_id === id);
      if (idx !== -1) {
        trainers.splice(idx, 1);
        saveData("trainers", trainers);
        renderTrainers();
      }
    }
  };

  cancelBtn.addEventListener("click", () => {
    form.reset();
    editIdInput.value = "";
    submitBtn.textContent = "Add Trainer";
    cancelBtn.style.display = "none";
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    const newTrainer = {
      trainer_id: Date.now(),
      gym_id: CURRENT_GYM_ID,
      trainer_name: document.getElementById("trainerName").value,
      specialization: document.getElementById("trainerSpecialization").value,
      experience_years: Number(document.getElementById("trainerExperience").value)
    };

    const editId = editIdInput.value;
    
    if (editId) {
      const idx = trainers.findIndex(t => t.trainer_id === parseInt(editId));
      if (idx !== -1) {
        trainers[idx] = { ...trainers[idx], ...newTrainer, trainer_id: trainers[idx].trainer_id };
        document.getElementById("saveNotice").textContent = "Trainer updated successfully!";
      }
    } else {
      trainers.push(newTrainer);
      document.getElementById("saveNotice").textContent = "Trainer added successfully!";
    }

    saveData("trainers", trainers);
    
    const notice = document.getElementById("saveNotice");
    notice.classList.add("show");
    setTimeout(() => notice.classList.remove("show"), 3000);
    
    form.reset();
    editIdInput.value = "";
    submitBtn.textContent = "Add Trainer";
    cancelBtn.style.display = "none";
    
    renderTrainers();
  });
}

document.addEventListener('DOMContentLoaded', init);
