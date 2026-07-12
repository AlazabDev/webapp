/**
* Frappe API Form Submission handler
*/
(function () {
  "use strict";

  let forms = document.querySelectorAll('.php-email-form');

  forms.forEach( function(e) {
    e.addEventListener('submit', function(event) {
      event.preventDefault();

      let thisForm = this;
      let action = thisForm.getAttribute('action');

      if (!action) {
        displayError(thisForm, 'The form action property is not set!');
        return;
      }

      let loading = thisForm.querySelector('.loading');
      let errorMessage = thisForm.querySelector('.error-message');
      let sentMessage = thisForm.querySelector('.sent-message');

      if (loading) loading.classList.add('d-block');
      if (errorMessage) errorMessage.classList.remove('d-block');
      if (sentMessage) sentMessage.classList.remove('d-block');

      let formData = new FormData(thisForm);
      
      // Determine Frappe API endpoint from action attribute
      let apiUrl = '/api/method/' + action;

      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'X-Frappe-CSRF-Token': frappe.csrf_token || ''
        },
        body: formData
      })
      .then(response => {
        if(response.ok) {
          return response.json();
        } else {
          throw new Error(`${response.status} ${response.statusText} ${response.url}`); 
        }
      })
      .then(data => {
        if (loading) loading.classList.remove('d-block');
        if (data.message && data.message.message === 'success' || data.message === 'success') {
          if (sentMessage) sentMessage.classList.add('d-block');
          thisForm.reset(); 
        } else {
          throw new Error(data.message || 'Form submission failed.');
        }
      })
      .catch((error) => {
        displayError(thisForm, error);
      });
    });
  });

  function displayError(thisForm, error) {
    let loading = thisForm.querySelector('.loading');
    let errorMessage = thisForm.querySelector('.error-message');
    if (loading) loading.classList.remove('d-block');
    if (errorMessage) {
      errorMessage.innerHTML = "حدث خطأ أثناء الإرسال. يرجى المحاولة لاحقاً.";
      errorMessage.classList.add('d-block');
    }
    console.error("Form Error: ", error);
  }

})();
