const registerModalElement = document.getElementById("registerModal");
const loginModalElement = document.getElementById("loginModal");

const registerModal = new bootstrap.Modal(registerModalElement);
const loginModal = new bootstrap.Modal(loginModalElement);

let selectedRegisterRole = "";
let selectedLoginRole = "";

/* ---------- Get Selected Role ---------- */
function getSelectedRole() {
    return document.getElementById("role").value;
}

/* ---------- Local Storage ---------- */
function getCredentials() {

    const credentials = localStorage.getItem("credentials");

    if (!credentials) {
        return {
            customers: [],
            managers: []
        };
    }

    return JSON.parse(credentials);
}

function saveCredentials(credentials) {
    localStorage.setItem(
        "credentials",
        JSON.stringify(credentials)
    );
}

/* ---------- Message Display ---------- */
function showMessage(form, message, type) {

    const oldMessage = form.querySelector(".alert-message");

    if (oldMessage) {
        oldMessage.remove();
    }

    const messageBox = document.createElement("div");

    messageBox.className =
        type === "success"
            ? "alert-message success-message"
            : "alert-message error-message";

    messageBox.innerText = message;

    form.appendChild(messageBox);
}

/* ---------- Create Input ---------- */
function createInput(
    label,
    id,
    type = "text",
    column = "col-md-6"
) {

    return `
        <div class="${column}">

            <label for="${id}" class="form-label">
                ${label}
            </label>

            <input
                type="${type}"
                id="${id}"
                name="${id}"
                class="form-control custom-control"
                required
            >

        </div>
    `;
}

/* ---------- Open Register Modal ---------- */
function openRegisterModal() {

    const role = getSelectedRole();

    if (role === "") {
        alert("Please select Customer or Manager first.");
        return;
    }

    selectedRegisterRole = role;

    const registerForm =
        document.getElementById("registerForm");

    const registerFields =
        document.getElementById("registerFields");

    const registerModalTitle =
        document.getElementById("registerModalTitle");

    registerForm.reset();

    const oldMessage =
        registerForm.querySelector(".alert-message");

    if (oldMessage) {
        oldMessage.remove();
    }

    /* ---------- Customer Register ---------- */
    if (role === "customer") {

        registerModalTitle.innerText =
            "Customer Registration";

        registerFields.innerHTML = `
            ${createInput("Username", "username")}

            ${createInput("Full Name", "fullName")}

            ${createInput("Email", "email", "email")}

            ${createInput("Phone No", "phone", "tel")}

            ${createInput("Password", "password", "password")}

            ${createInput(
            "Confirm Password",
            "confirmPassword",
            "password"
        )}
        `;
    }

    /* ---------- Manager Register ---------- */
    else if (role === "manager") {

        registerModalTitle.innerText =
            "Manager Registration";

        registerFields.innerHTML = `
            ${createInput(
            "Full Name of Manager",
            "managerName"
        )}

            ${createInput("Gym Name", "gymName")}

            ${createInput("Gym Reg: ID", "gymRegId")}

            ${createInput("Gym Location", "gymLocation")}

            ${createInput("Phone No", "phone", "tel")}

            ${createInput("Email", "email", "email")}

            ${createInput("Password", "password", "password")}

            ${createInput(
            "Confirm Password",
            "confirmPassword",
            "password"
        )}
        `;
    }

    registerModal.show();
}

/* ---------- Open Login Modal ---------- */
function openLoginModal() {

    const role = getSelectedRole();

    if (role === "") {
        alert("Please select Customer or Manager first.");
        return;
    }

    selectedLoginRole = role;

    const loginForm =
        document.getElementById("loginForm");

    const loginFields =
        document.getElementById("loginFields");

    const loginModalTitle =
        document.getElementById("loginModalTitle");

    loginForm.reset();

    const oldMessage =
        loginForm.querySelector(".alert-message");

    if (oldMessage) {
        oldMessage.remove();
    }

    /* ---------- Customer Login ---------- */
    if (role === "customer") {

        loginModalTitle.innerText =
            "Customer Login";

        loginFields.innerHTML = `
            ${createInput(
            "Username",
            "username",
            "text",
            "col-12"
        )}

            ${createInput(
            "Password",
            "password",
            "password",
            "col-12"
        )}
        `;
    }

    /* ---------- Manager Login ---------- */
    else if (role === "manager") {

        loginModalTitle.innerText =
            "Manager Login";

        loginFields.innerHTML = `
            ${createInput(
            "Gym Reg: ID",
            "gymRegId",
            "text",
            "col-12"
        )}

            ${createInput(
            "Password",
            "password",
            "password",
            "col-12"
        )}
        `;
    }

    loginModal.show();
}

/* ---------- Register Form Submit ---------- */
document
    .getElementById("registerForm")
    .addEventListener("submit", function (event) {

        event.preventDefault();

        const form = event.target;

        const formData = new FormData(form);

        const data =
            Object.fromEntries(formData.entries());

        /* Password Validation */
        if (data.password !== data.confirmPassword) {

            showMessage(
                form,
                "Password and Confirm Password do not match.",
                "error"
            );

            return;
        }

        const credentials = getCredentials();

        /* ---------- Customer Register ---------- */
        if (selectedRegisterRole === "customer") {

            const existingCustomer =
                credentials.customers.find(function (customer) {

                    return customer.username === data.username;
                });

            if (existingCustomer) {

                showMessage(
                    form,
                    "Username already registered.",
                    "error"
                );

                return;
            }

            credentials.customers.push({
                username: data.username,
                fullName: data.fullName,
                email: data.email,
                phone: data.phone,
                password: data.password
            });

            saveCredentials(credentials);

            showMessage(
                form,
                "Customer registered successfully.",
                "success"
            );

            form.reset();
        }

        /* ---------- Manager Register ---------- */
        if (selectedRegisterRole === "manager") {

            const existingManager =
                credentials.managers.find(function (manager) {

                    return manager.gymRegId === data.gymRegId;
                });

            if (existingManager) {

                showMessage(
                    form,
                    "Gym Reg ID already registered.",
                    "error"
                );

                return;
            }

            credentials.managers.push({
                managerName: data.managerName,
                gymName: data.gymName,
                gymRegId: data.gymRegId,
                gymLocation: data.gymLocation,
                phone: data.phone,
                email: data.email,
                password: data.password
            });

            saveCredentials(credentials);

            showMessage(
                form,
                "Manager registered successfully.",
                "success"
            );

            form.reset();
        }
    });

/* ---------- Login Form Submit ---------- */
document
    .getElementById("loginForm")
    .addEventListener("submit", function (event) {

        event.preventDefault();

        const form = event.target;

        const formData = new FormData(form);

        const data =
            Object.fromEntries(formData.entries());

        const credentials = getCredentials();

        /* ---------- Customer Login ---------- */
        if (selectedLoginRole === "customer") {

            const customer =
                credentials.customers.find(function (customer) {

                    return (
                        customer.username === data.username &&
                        customer.password === data.password
                    );
                });

            if (customer) {

                showMessage(
                    form,
                    "Login successful! Redirecting...",
                    "success"
                );

                setTimeout(() => {
                    window.location.href =
                        "./customer/home.html";
                }, 1000);
            }
            else {

                showMessage(
                    form,
                    "Invalid username or password.",
                    "error"
                );
            }
        }

        /* ---------- Manager Login ---------- */
        if (selectedLoginRole === "manager") {

            const manager =
                credentials.managers.find(function (manager) {

                    return (
                        manager.gymRegId === data.gymRegId &&
                        manager.password === data.password
                    );
                });

            if (manager) {

                showMessage(
                    form,
                    "Login successful! Redirecting...",
                    "success"
                );

                setTimeout(() => {
                    window.location.href =
                        "./manager/dashboard.html";
                }, 1000);
            }
            else {

                showMessage(
                    form,
                    "Invalid Gym Reg ID or password.",
                    "error"
                );
            }
        }
    });