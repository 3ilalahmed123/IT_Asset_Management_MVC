document.addEventListener('DOMContentLoaded', () => {
    const actionButtons = document.querySelectorAll('.action-button');
    const assetIdField = document.getElementById('assetId');
    const actionTypeField = document.getElementById('actionType');
    const loanIdField = document.getElementById('loanId');
    const modalTitle = document.getElementById('actionModalLabel');
    const confirmationMessage = document.getElementById('confirmationMessage');

    // Add action button functionality
    actionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const assetId = button.getAttribute('data-asset-id');
            const assetName = button.getAttribute('data-asset-name');
            const loanId = button.getAttribute('data-loan-id');
            const actionType = button.getAttribute('data-action');

            // Determine the action type and set the modal content accordingly
            if (actionType === 'return') {
                modalTitle.textContent = 'Return Asset';
                confirmationMessage.textContent = `Are you sure you want to return your ${assetName} with ID ${assetId}?`;
            } else if (actionType === 'repair') {
                modalTitle.textContent = 'Report Repair';
                confirmationMessage.textContent = `Please confirm repair request for ${assetName} with ID ${assetId}.`;
            } else if (actionType === 'complete-repair') {
                modalTitle.textContent = 'Complete Repair';
                confirmationMessage.textContent = `Are you sure you want to mark ${assetName} with ID ${assetId} as repaired?`;
            } else if (actionType === 'loan') {
                modalTitle.textContent = 'Loan Asset';
                confirmationMessage.textContent = `Are you sure you want to loan the asset "${assetName}" with ID ${assetId}?`;
            }

            // Populate the modal fields
            assetIdField.value = assetId;
            actionTypeField.value = actionType;
            loanIdField.value = loanId;
            modalTitle.textContent = actionText;

        });
    });

    // Handle modal form submission
    const actionForm = document.getElementById('actionForm');
    actionForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const assetId = assetIdField.value;
        const actionType = actionTypeField.value;
        const loanId = loanIdField.value;
        //Send Post request using assetID, actionType and loanID to server
        try {
            const response = await fetch('handle-action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ assetId, actionType, loanId }),
            });

            if (response.ok) {
                alert("Record updated successfully!");
                window.location.reload();
            } else {
                alert('Failed to process the action. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
});