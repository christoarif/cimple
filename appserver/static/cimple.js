function submitData(inputText) {
    var xhr = new XMLHttpRequest();

    xhr.open("POST", "https://localhost:8089/servicesNS/-/cimple/cimple", true);
    // xhr.setRequestHeader('Authorization', 'Bearer ');

    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send(inputText);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                data = JSON.parse(xhr.responseText);
                var container = document.getElementById('mappingContainer');

                container.innerHTML = '';

                var counter = 1;

                var t_input = document.createElement('input');
                t_input.type = 'text';
                t_input.value = "Input Field";
                t_input.disabled = true;
                container.appendChild(t_input);

                var t_datamodel = document.createElement('input');
                t_datamodel.type = 'text';
                t_datamodel.value = "Suggested Data Model";
                t_datamodel.disabled = true;
                container.appendChild(t_datamodel);

                var t_field = document.createElement('input');
                t_field.type = 'text';
                t_field.value = "Suggested Field";
                t_field.disabled = true;
                container.appendChild(t_field);
                container.appendChild(document.createElement('br'));

                if(Array.isArray(data)) {

                    data.forEach(function(item) {

                        var input = document.createElement('input');
                        input.type = 'text';
                        input.value = item['input'];
                        input.id = 'mapping-input-' + counter;
                        input.disabled = true;                    
                        container.appendChild(input);

                        var input = document.createElement('input');
                        input.type = 'text';
                        input.value = item['data-model'];
                        input.id = 'mapping-datamodel-' + counter;                        
                        container.appendChild(input);

                        var input = document.createElement('input');
                        input.type = 'text';
                        input.value = item['field'];
                        input.id = 'mapping-field-' + counter;                        
                        container.appendChild(input);

                        container.appendChild(document.createElement('br'));
                        counter++;


                    });

                    var fieldscontainer = document.getElementById('fieldscontainer');
                    fieldscontainer.innerHTML = ""
                    document.getElementById("fields_submit").style.visibility = "hidden";

                    confirm_button = document.getElementById('confirm');
                    document.getElementById("confirm").style.visibility = "visible";
                }


            } else {
                alert("Request failed. Status:", xhr.status);
            }
        }
    };

    xhr.onerror = function () {
        alert("Request failed2: " + inputText);
    };
}

function confirmData(inputText) {

    confirm_button = document.getElementById('confirm');
    document.getElementById("confirm").style.visibility = "hidden";
    var xhr = new XMLHttpRequest();

    // Consolidate input
    counter = 1
    payload = []
    while (document.getElementById("mapping-input-" + counter) != null) {
        payload[counter -1] = {
            "input": document.getElementById("mapping-input-" + counter).value,
            "data-model": document.getElementById("mapping-datamodel-" + counter).value,
            "field": document.getElementById("mapping-field-" + counter).value
        }
        counter = counter + 1
    }

    xhr.open("POST", "https://localhost:8089/servicesNS/-/cimple/cimple_confirm", true);
    // xhr.setRequestHeader('Authorization', 'Bearer ');

    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send(JSON.stringify(payload));
    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var container = document.getElementById('mappingContainer');
                container.innerHTML = '';

                var label = document.createElement('label');
                label.textContent = "CIM setttings confirmed.";
                container.appendChild(label);

            } else {
                var container = document.getElementById('mappingContainer');
                container.innerHTML = '';

                var label = document.createElement('label');
                label.textContent = "CIM setttings save failed.";
                container.appendChild(label);
            }
        }
    };

    xhr.onerror = function () {
        alert("Request failed2: " + inputText);
    };
}

document.getElementById("event_type_submit").addEventListener("click", function () {

    mappingContainer = document.getElementById('mappingContainer');
    mappingContainer.style.visibility = "hidden";

    var container = document.getElementById('fieldscontainer');

    container.innerHTML = ""

    array = ["user_id", "src", "act", "obj", "timestamp", "event"]
    counter = 0

    array.forEach(function(item) {

        var textField = document.createElement('input');
        textField.type = 'text';
        textField.value = item;
        textField.id = 'textField' + counter;

        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = 'checkbox' + counter;

        container.appendChild(textField);
        container.appendChild(checkbox);
        container.appendChild(document.createElement('br'));
        counter = counter + 1
    })

    document.getElementById("fields_submit").style.visibility = "visible";

});

document.getElementById("fields_submit").addEventListener("click", function () {

    mappingContainer = document.getElementById('mappingContainer');
    mappingContainer.style.visibility = "visible";
    
    counter = 0
    selectedFields = ""
    while (document.getElementById("checkbox" + counter) != null) {

        var checkbox = document.getElementById('checkbox' + counter);
        var textField = document.getElementById('textField' + counter);
        if (checkbox.checked) {
            // selectedFields.push(textField.value);
            selectedFields = textField.value + ";" + selectedFields
        }

        counter = counter + 1
    }

    submitData(selectedFields);
});

document.getElementById("confirm").addEventListener("click", function () {
    confirmData();
});
