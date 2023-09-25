$(document).ready(function () {
    $('.btn.outline').on('click', function (event) {
      var subject = $(this).data('subject');
      console.log(subject);
      $('#id_subject').val(subject);
      $('#contactModal').modal('show');
    });
  });
  

$(document).ready(function() {
  var emailInput = $('#id_email');
  var emailError = $('#email-error');
  var submitButton = $('#form_button');
  var isInputValid = false; // Track input validity

  emailInput.on('input', function() {
      isInputValid = /\S+@\S+\.\S+/.test(emailInput.val()); // Basic email format check
  });

  emailInput.on('blur', function() {
      if (!isInputValid && emailInput.val().trim() !== '') {
          emailError.text('Введіть коректний емейл');
          emailError.addClass('error-message'); // Add error message class
          submitButton.prop('disabled', true);
      } else {
          emailError.text('');
          emailError.removeClass('error-message'); // Remove error message class
          submitButton.prop('disabled', false);
      }
  });
});