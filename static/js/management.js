document.addEventListener("DOMContentLoaded", () => {
    const editButtons = document.querySelectorAll(".edit-button");
    const deleteButtons = document.querySelectorAll(".delete-button");

    const editModal = new bootstrap.Modal(document.getElementById("editModal"));
    const recordIdField = document.getElementById("recordId");
    const recordTypeField = document.getElementById("recordType");
    const formFieldsContainer = document.getElementById("formFields");
    const editForm = document.getElementById("editForm");



    // Add listener for edit button click
    editButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            const recordId = button.getAttribute("data-id");
            const recordType = button.getAttribute("data-type");
            const rowIndex = button.getAttribute("data-row");

            // Set hidden fields in modal
            recordIdField.value = recordId;
            recordTypeField.value = recordType;

            const formData = new FormData(editForm);
            const updatedData = {};
            formData.forEach((value, key) => {
                updatedData[key] = value;
            });


            // Get record details from server
            try {
                const response = await fetch(`/management/get-record/${recordType}/${recordId}`);
                const data = await response.json();

                if (response.ok) {
                    // Dynamically populate modal form fields based on RecordOrder
                    formFieldsContainer.innerHTML = ""; // Clear previous fields

                    // Parse RecordOrder
                    const recordOrder = data.RecordOrder.split("|"); // Convert string to array

                    // Create fields based on the recordOrder
                    recordOrder.forEach((key) => {
                        if (key in data) {
                            //Create element
                            const formGroup = document.createElement("div");
                            formGroup.className = "mb-3";
                            
    


                            const label = document.createElement("label");
                            label.className = "form-label";
                            label.textContent = key;
                            label.setAttribute("for", key);

                            const input = document.createElement("input");
                            input.className = "form-control";
                            input.id = key;
                            input.name = key;
                            input.type = "text";
                            input.value = data[key];

                            formGroup.appendChild(label);
                            formGroup.appendChild(input);
                            formFieldsContainer.appendChild(formGroup);
                        }
                    });

                    editModal.show();
                } else {
                    alert(data.message || "Failed to fetch record details."); //Throw error if fetching record fails
                }
            } catch (error) {
                console.error("Error fetching record details:", error); //Throw error if exception thrown
                alert("An error occurred while fetching record details.");
            }
        });
    });

    // Add listener for submit button click
    editForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const recordId = recordIdField.value;
        const recordType = recordTypeField.value;

        // Get form data and parse
        const formData = new FormData(editForm);
        const updatedData = {};
        formData.forEach((value, key) => {
            updatedData[key] = value;
        });

        // Validate data
        const { isValid, errors } = validateFormData(updatedData, recordType);
        if (!isValid) {
            alert(errors.join("\n"));
            return;
        }

        // Send Post request to dynamic route and json data to server
        try {
            const response = await fetch(`update-record/${recordType}/${recordId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(updatedData),
            });

            if (response.ok) {
                alert("Record updated successfully!");
                window.location.reload();
            } else {
                const data = await response.json();
                alert(data.message || "Failed to update record.");
            }
        } catch (error) {
            console.error("Error updating record:", error);
            alert("An error occurred while updating the record.");
        }
    });

    // Add listener for delete button click
    deleteButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            const recordId = button.getAttribute("data-id");
            const recordType = button.getAttribute("data-type");
            //Show confirmation, if yes send post request to backend
            if (confirm("Are you sure you want to delete this record?")) {
                try {
                    const response = await fetch(`delete-record/${recordType}/${recordId}`, {
                        method: "POST",
                    });

                    if (response.ok) {
                        alert("Record deleted successfully!");
                        window.location.reload();
                    } else {
                        const data = await response.json();
                        alert(data.message || "Failed to delete record.");
                    }
                } catch (error) {
                    console.error("Error deleting record:", error);
                    alert("An error occurred while deleting the record.");
                }
            }
        });
    });
});

//Add listener to page for getting add buttons and adding listener to buttons
document.addEventListener("DOMContentLoaded", () => {
    const addButtons = document.querySelectorAll(".btn[data-bs-target='#addModal']");
    const addModal = new bootstrap.Modal(document.getElementById("addModal"));
    const addRecordTypeField = document.getElementById("addRecordType");
    const addFormFieldsContainer = document.getElementById("addFormFields");
    const addForm = document.getElementById("addForm");

    // Add listener to add buttons when clicked
    addButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const recordType = button.getAttribute("data-type");
            addRecordTypeField.value = recordType;

            addFormFieldsContainer.innerHTML = "";  // Clear previous fields

            //Depending on record type set record order
            let recordOrder;
            if (recordType === "user") {
                recordOrder = "Forename|Surname|Username|Password|Role";
            } else if (recordType === "asset") {
                recordOrder = "Name|Type|Status";
            } else if (recordType === "loan") {
                recordOrder = "AssetID|UserID|LoanDate|DueDate|ReturnDate";
            }

            //For the record order in order create fields and add to modal form
            recordOrder.split("|").forEach((key) => {
                const formGroup = document.createElement("div");
                formGroup.className = "mb-3";

                const label = document.createElement("label");
                label.className = "form-label";
                label.textContent = key;
                label.setAttribute("for", key);

                const input = document.createElement("input");
                input.className = "form-control";
                input.id = key;
                input.name = key;
                input.type = "text";

                formGroup.appendChild(label);
                formGroup.appendChild(input);
                addFormFieldsContainer.appendChild(formGroup);
            });

            addModal.show();
        });
    });

    // Add listener for submit button on add form
    addForm.addEventListener("submit", async (e) => {
        e.preventDefault(); // Prevent default form submission

        const recordType = addRecordTypeField.value;

        // Collect form data
        const formData = new FormData(addForm);
        const newRecordData = {};
        formData.forEach((value, key) => {
            newRecordData[key] = value;
        });

        // Validate data
        const { isValid, errors } = validateFormData(newRecordData, recordType);
        if (!isValid) {
            alert(errors.join("\n"));
            return;
        }

        // Send post request to dynamic backend route  with json data for the new record
        try {
            const response = await fetch(`/management/add-record/${recordType}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newRecordData),
            });

            if (response.ok) {
                alert("Record added successfully!");
                window.location.reload();
            } else {
                const data = await response.json();
                alert(data.message || "Failed to add record."); //Throw error if other response
            }
        } catch (error) { //Throw erorr if exception cought
            console.error("Error adding record:", error);
            alert("An error occurred while adding the record.");
        }
    });
});

//Validate form data function
function validateFormData(formData, recordType) {
    let isValid = true;
    const errors = [];

    if (recordType === "user") {
        if (!formData["Forename"] || formData["Forename"].trim() === "") {
            isValid = false;
            errors.push("Forename is required.");
        }
        if (!formData["Surname"] || formData["Surname"].trim() === "") {
            isValid = false;
            errors.push("Surname is required.");
        }
        if (!formData["Username"] || formData["Username"].trim().length < 3) {
            isValid = false;
            errors.push("Username is required.");
        }
        const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d).{8,}$/;
        if (!passwordRegex.test(formData["Password"])) {
            isValid = false;
            errors.push("Password must be at least 8 characters long and contain both letters and numbers.");
        }
        if (!["Admin", "Regular"].includes(formData["Role"])) {
            isValid = false;
            errors.push("Role must be 'Admin' or 'Regular'.");
        }
    } else if (recordType === "asset") {
        if (!formData["Name"] || formData["Name"].trim() === "") {
            isValid = false;
            errors.push("Asset Name is required.");
        }
        if (!formData["Type"] || formData["Type"].trim() === "") {
            isValid = false;
            errors.push("Asset Type is required.");
        }
        if (!["Unassigned", "Assigned", "Service/Repair"].includes(formData["Status"])) {
            isValid = false;
            errors.push("Asset Status must be 'Unassigned', 'Assigned' or Service/Repair.");
        }
    } else if (recordType === "loan") {
        if (!formData["AssetID"] || isNaN(parseInt(formData["AssetID"]))) {
            isValid = false;
            errors.push("Valid AssetID is required.");
        }
        if (!formData["UserID"] || isNaN(parseInt(formData["UserID"]))) {
            isValid = false;
            errors.push("Valid UserID is required.");
        }
        if (!formData["LoanDate"] || new Date(formData["LoanDate"]).toString() === "Invalid Date") {
            isValid = false;
            errors.push("Valid Loan Date is required.");
        }
    }

    return { isValid, errors };
}
