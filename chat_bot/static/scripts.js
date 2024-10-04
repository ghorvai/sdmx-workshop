document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const categorySelect = document.getElementById('category-select');
    const dataflowSelect = document.getElementById('dataflow-select');
    const initializeBotButton = document.getElementById('initialize-bot');

    // Fetch categories and populate the first dropdown
    fetch('/get_categories')
        .then(response => response.json())
        .then(categories => {
            categorySelect.innerHTML = '<option value="">Select a category</option>';
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categorySelect.appendChild(option);
            });
        });

    // Event listener for category selection
    categorySelect.addEventListener('change', (e) => {
        const selectedCategory = e.target.value;
        if (selectedCategory) {
            fetch(`/get_dataflows/${selectedCategory}`)
                .then(response => response.json())
                .then(dataflows => {
                    dataflowSelect.innerHTML = '<option value="">Select a dataflow</option>';
                    dataflows.forEach(dataflow => {
                        const option = document.createElement('option');
                        option.value = dataflow;
                        option.textContent = dataflow;
                        dataflowSelect.appendChild(option);
                    });
                    dataflowSelect.disabled = false;
                });
        } else {
            dataflowSelect.innerHTML = '<option value="">Select a dataflow</option>';
            dataflowSelect.disabled = true;
            initializeBotButton.disabled = true;
        }
    });

    // Enable the Initialize Bot button only if both category and dataflow are selected
    dataflowSelect.addEventListener('change', () => {
        const isCategorySelected = categorySelect.value !== '';
        const isDataflowSelected = dataflowSelect.value !== '';
        initializeBotButton.disabled = !(isCategorySelected && isDataflowSelected);
    });

    // Initialize the bot when the button is clicked
    initializeBotButton.addEventListener('click', () => {
        const selectedCategory = categorySelect.value;
        const selectedDataflow = dataflowSelect.value;

        if (selectedCategory && selectedDataflow) {
            fetch('/initialize_bot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    category: selectedCategory,
                    dataflow: selectedDataflow
                }),
            }).then(response => response.json())
            .then(data => {
                appendMessage('llm', `Bot initialized with dataflow: ${selectedDataflow}`);
            });
        }
    });

    // Chat form submission event listener
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value;
        if (message.trim() === '') return;

        appendMessage('user', message);
        userInput.value = '';

        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });

        const data = await response.json();
        appendMessage('llm', data.response);
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
