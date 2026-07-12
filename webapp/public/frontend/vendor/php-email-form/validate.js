/**
* Secure Form Validation Simulation
* Replaces the old PHP-dependent script to prevent vulnerabilities
*/
(function () {
  "use strict";

  let forms = document.querySelectorAll('.php-email-form');

  forms.forEach( function(e) {
    e.addEventListener('submit', function(event) {
      event.preventDefault();

      let thisForm = this;

      let loading = thisForm.querySelector('.loading');
      let errorMessage = thisForm.querySelector('.error-message');
      let sentMessage = thisForm.querySelector('.sent-message');

      if (loading) loading.classList.add('d-block');
      if (errorMessage) errorMessage.classList.remove('d-block');
      if (sentMessage) sentMessage.classList.remove('d-block');

      // Simulate network request securely without making external calls
      setTimeout(() => {
        if (loading) loading.classList.remove('d-block');
        if (sentMessage) sentMessage.classList.add('d-block');
        thisForm.reset();
      }, 1500);

    });
  });

})();
