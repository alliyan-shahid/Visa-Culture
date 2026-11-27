
  (function () {
    const dateInput = document.getElementById('date');
    const serviceType = document.getElementById('service_type');
    const preferredChoiceLabel = document.getElementById('preferred-choice-label');
    const preferredChoiceInput = document.getElementById('university');

    function updatePreferredChoice() {
      if (!serviceType || !preferredChoiceLabel || !preferredChoiceInput) return;
      const isTestPreparation = serviceType.value === 'test_preparation';
      preferredChoiceLabel.firstChild.textContent = isTestPreparation ? 'Preferred test ' : 'Preferred destination ';
      preferredChoiceInput.placeholder = isTestPreparation ? 'e.g. IELTS, PTE, TOEFL' : 'Any Country';
    }

    if (serviceType) {
      serviceType.addEventListener('change', updatePreferredChoice);
      updatePreferredChoice();
    }

    if (!dateInput) return;

    function openDatePicker() {
      if (typeof dateInput.showPicker === 'function') {
        try {
          dateInput.showPicker();
        } catch (_) {
          /* already open or unsupported gesture */
        }
      }
    }

    dateInput.addEventListener('click', openDatePicker);
    dateInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openDatePicker();
      }
    });
  })();
