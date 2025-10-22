function showToast(message, isError = false) {
  const toastContainer = document.getElementById('toastContainer') || (() => {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 1050;';
    document.body.appendChild(container);
    return container;
  })();

  const toast = document.createElement('div');
  toast.className = `toast align-items-center ${isError ? 'bg-danger' : 'bg-success'} text-white`;
  toast.setAttribute('role', 'alert');
  toast.setAttribute('aria-live', 'assertive');
  toast.setAttribute('aria-atomic', 'true');
  
  toast.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">${message}</div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  `;
  
  toastContainer.appendChild(toast);
  const bsToast = new bootstrap.Toast(toast);
  bsToast.show();
  
  toast.addEventListener('hidden.bs.toast', () => toast.remove());
}

async function deleteMessage(messageId) {
  try {
    const response = await fetch(`/delete_message/${messageId}`, {
      method: 'DELETE'
    });
    const result = await response.json();
    
    if (response.ok && result.success) {
      const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
      if (messageElement) {
        messageElement.remove();
        showToast('Message deleted successfully');
        
        // If no messages left, show the "No messages" text
        const messageHistory = document.querySelector('.message-history');
        if (messageHistory && !messageHistory.children.length) {
          messageHistory.innerHTML = '<p class="text-muted mb-0">No messages classified yet.</p>';
        }
      }
    } else {
      throw new Error('Failed to delete message');
    }
  } catch (error) {
    console.error('Error deleting message:', error);
    showToast('Failed to delete message', true);
  }
}

// Handle delete button clicks through event delegation
function handleDeleteClick(e) {
  const deleteButton = e.target.closest('.delete-message');
  if (!deleteButton) return;
  
  e.preventDefault();
  const messageElement = deleteButton.closest('[data-message-id]');
  if (messageElement) {
    const messageId = messageElement.dataset.messageId;
    deleteMessage(messageId);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('messageInput');
  const button = document.getElementById('classifyButton');
  const form = document.getElementById('classifierForm');
  const loadingBar = document.getElementById('loadingBar');

  input.addEventListener('input', () => {
    if (input.value.trim() !== "") {
      button.classList.remove('btn-secondary');
      button.classList.add('btn-primary');
      button.disabled = false;
    } else {
      button.classList.remove('btn-primary');
      button.classList.add('btn-secondary');
      button.disabled = true;
    }
  });

  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    loadingBar.style.display = 'block';
    button.disabled = true;
    
    const formData = new FormData(form);
    try {
      const response = await fetch('/', {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        const html = await response.text();
        // Create a temporary div to parse the HTML
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        
        // Find the prediction card in the response
        const newPrediction = tempDiv.querySelector('.mt-5.d-flex.justify-content-center');
        if (newPrediction) {
          // Find or create the prediction container
          let predictionContainer = document.querySelector('.mt-5.d-flex.justify-content-center');
          if (!predictionContainer) {
            predictionContainer = document.createElement('div');
            predictionContainer.className = 'mt-5 d-flex justify-content-center';
            form.parentNode.insertBefore(predictionContainer, form.nextSibling);
          }
          // Update the prediction
          predictionContainer.innerHTML = newPrediction.innerHTML;
        }
        // Update the history list if present in the response
        const newHistory = tempDiv.querySelector('#historyContainer');
        if (newHistory) {
          const historyContainer = document.querySelector('#historyContainer');
          if (historyContainer) {
            historyContainer.innerHTML = newHistory.innerHTML;
          }
        }
      }

      // Set up event delegation for delete buttons
      const historyContainer = document.querySelector('#historyContainer');
      if (historyContainer) {
        // Remove any existing event listener
        historyContainer.removeEventListener('click', handleDeleteClick);
        // Add new event listener
        historyContainer.addEventListener('click', handleDeleteClick);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loadingBar.style.display = 'none';
      button.disabled = false;
      input.value = ''; // Clear the input
      button.classList.remove('btn-primary');
      button.classList.add('btn-secondary');
      button.disabled = true;
    }
  });
});