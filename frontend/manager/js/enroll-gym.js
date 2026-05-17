
async function init() {
  const [users, gyms] = await Promise.all([
    loadData("users"),
    loadData("gyms")
  ]);

  const manager = users.find(u => u.user_id === CURRENT_MANAGER_ID);
  const myGym = gyms.find(g => g.gym_id === CURRENT_GYM_ID);

  if (manager) {
    setText("managerNameDisplay", manager.name);
    document.getElementById("managerName").value = manager.name;
  }
  
  const editBtn = document.getElementById("editBtn");
  const saveBtn = document.getElementById("saveBtn");
  const form = document.getElementById("gymForm");
  const inputs = form.querySelectorAll("input, textarea");

  function setEditMode(isEdit) {
    inputs.forEach(input => {
      input.disabled = !isEdit;
    });
    if (isEdit) {
      editBtn.style.display = "none";
      saveBtn.style.display = "block";
    } else {
      editBtn.style.display = "block";
      saveBtn.style.display = "none";
    }
  }

  if (myGym) {
    setText("gymNameDisplay", myGym.gym_name);
    document.getElementById("gymName").value = myGym.gym_name || "";
    document.getElementById("description").value = myGym.description || "";
    document.getElementById("address").value = myGym.address || "";
    const today = new Date().toISOString().split('T')[0];
    document.getElementById("openedOn").value = myGym.opened_on || today;
    document.getElementById("contactNumber").value = myGym.contact || "";
    document.getElementById("email").value = myGym.email || "";
    document.getElementById("website").value = myGym.website || "";
    
    setEditMode(false); // Read-only if already enrolled
  } else {
    // First time enrollment
    const today = new Date().toISOString().split('T')[0];
    document.getElementById("openedOn").value = today;
    setEditMode(true); // Editable by default
  }

  editBtn.addEventListener("click", () => {
    setEditMode(true);
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (myGym) {
      myGym.gym_name = document.getElementById("gymName").value;
      myGym.description = document.getElementById("description").value;
      myGym.address = document.getElementById("address").value;
      myGym.opened_on = document.getElementById("openedOn").value;
      myGym.contact = document.getElementById("contactNumber").value;
      myGym.email = document.getElementById("email").value;
      myGym.website = document.getElementById("website").value;
      
      // Update manager name if they edited it
      if (manager) {
        manager.name = document.getElementById("managerName").value;
        saveData("users", users);
      }
      
      const gymIndex = gyms.findIndex(g => g.gym_id === CURRENT_GYM_ID);
      if (gymIndex > -1) {
        gyms[gymIndex] = myGym;
        saveData("gyms", gyms);
      }
    } else {
      // Logic for new gym enrollment
      const newGym = {
        gym_id: Math.floor(Math.random() * 1000) + 100,
        manager_id: CURRENT_MANAGER_ID,
        gym_name: document.getElementById("gymName").value,
        description: document.getElementById("description").value,
        address: document.getElementById("address").value,
        opened_on: document.getElementById("openedOn").value,
        contact: document.getElementById("contactNumber").value,
        email: document.getElementById("email").value,
        website: document.getElementById("website").value,
        status: "pending",
        monthly_revenue: 0,
        members: 0,
        rating: 0
      };
      gyms.push(newGym);
      saveData("gyms", gyms);
      
      // Update our simulated session so it remembers we now have a gym!
      localStorage.setItem('SIMULATED_GYM_ID', newGym.gym_id);
      CURRENT_GYM_ID = newGym.gym_id;
    }
    
    const notice = document.getElementById("saveNotice");
    notice.classList.add("show");
    setTimeout(() => notice.classList.remove("show"), 3000);
    setText("gymNameDisplay", document.getElementById("gymName").value);
    
    setEditMode(false); // Switch back to read-only after saving
    alert("You have successfully enrolled your gym!");
  });
}

document.addEventListener('DOMContentLoaded', init);