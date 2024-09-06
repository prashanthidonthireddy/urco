
/*Major issue in this section_Not working*/
// Handle tab navigation
function showSection(sectionId) {
    // Hide all sections
    var sections = document.getElementsByClassName('content-section');
    for (var i = 0; i < sections.length; i++) {
        sections[i].style.display = 'none';
    }

    // Show the selected section
    document.getElementById(sectionId).style.display = 'block';
}

// Handle Add Chemical functionality
//document.getElementById('add-chemical-btn').addEventListener('click', function() {
//    const chemicalsContainer = document.getElementById('chemicals-container');
//    const chemicalItem = document.createElement('div');
//    chemicalItem.className = 'chemical-item';
//    chemicalItem.innerHTML = `
//        <select required>
//            <option value="">--Select Chemical--</option>
//            <option value="chemical1">Chemical 1</option>
//            <option value="chemical2">Chemical 2</option>
//            <option value="chemical3">Chemical 3</option>
//        </select>
//        <input type="number" placeholder="Quantity" required>
//        <select required>
//            <option value="ml">ml</option>
//            <option value="l">l</option>
//            <option value="g">g</option>
//            <option value="kg">kg</option>
//        </select>
//        <button type="button" class="remove-chemical-btn">Remove</button>
//    `;
//    chemicalsContainer.appendChild(chemicalItem);
//
//    // Handle remove chemical button
//    chemicalItem.querySelector('.remove-chemical-btn').addEventListener('click', function() {
//        chemicalsContainer.removeChild(chemicalItem);
//    });
//});
//
//// Handle form submission
document.getElementById('new-order-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('New order submitted!');
    // Add form submission logic here (e.g., send data to backend)
});

// Handle approve, reject, and escalate buttons
const orderItems = document.querySelectorAll('.order-item');

orderItems.forEach(order => {
    order.querySelector('.approve-btn').addEventListener('click', function() {
        alert('Order approved');
        // Add logic to handle the approval process
    });

    order.querySelector('.reject-btn').addEventListener('click', function() {
        alert('Order rejected');
        // Add logic to handle the rejection process
    });

    order.querySelector('.escalate-btn').addEventListener('click', function() {
        alert('Order escalated');
        // Add logic to handle the escalation process
    });
});

document.getElementById('addChemBtn').addEventListener('click', function() {
    const chemDiv = document.getElementById('chemicalList');

    const newChemDiv = document.createElement('div');
    newChemDiv.className = 'form-group';

    const newChemInput = document.createElement('input');
    newChemInput.type = 'text';
    newChemInput.name = 'chemical';
    newChemInput.required = true;
    newChemDiv.appendChild(newChemInput);

    chemDiv.appendChild(newChemDiv);
});


