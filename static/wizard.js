document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("wizardForm");
  if (!form) return;

  const steps = form.querySelectorAll(".form-step");
  let currentStep = 0;

  const nextBtn = document.getElementById("nextBtn");
  const prevBtn = document.getElementById("prevBtn");
  const progressBar = document.getElementById("progressBar");
  const stepNumber = document.getElementById("stepNumber");

  // === Spikelet Fertility Auto Calculation ===
  const filled = document.getElementById("spikelets_filled");
  const total = document.getElementById("spikelets_total");
  const fertility = document.getElementById("fertility");

  function updateFertility() {
    const f = parseFloat(filled?.value);
    const t = parseFloat(total?.value);
    if (!isNaN(f) && !isNaN(t) && t > 0) {
      fertility.value = ((f / t) * 100).toFixed(1);
    } else {
      fertility.value = "";
    }
  }

  if (filled && total && fertility) {
    filled.addEventListener("input", updateFertility);
    total.addEventListener("input", updateFertility);
  }

  // === Disease Incidence Calculations ===
  const timepoints = ["t1", "t2", "t3"];
  timepoints.forEach(tp => {
    const total = document.getElementById(`panicles_${tp}`);
    const infected = document.getElementById(`infected_${tp}`);
    const incidence = document.getElementById(`incidence_${tp}`);

    function updateIncidence() {
      const t = parseFloat(total?.value);
      const i = parseFloat(infected?.value);
      if (!isNaN(t) && !isNaN(i) && t > 0) {
        incidence.value = ((i / t) * 100).toFixed(1);
      } else {
        incidence.value = "";
      }
    }

    if (total && infected && incidence) {
      total.addEventListener("input", updateIncidence);
      infected.addEventListener("input", updateIncidence);
    }
  });

  // === Average Temperature Calculation ===
  const tempMin = document.getElementById("temp_min");
  const tempMax = document.getElementById("temp_max");
  const tempAvg = document.getElementById("temp_avg");

  function updateAvgTemp() {
    const min = parseFloat(tempMin?.value);
    const max = parseFloat(tempMax?.value);
    if (!isNaN(min) && !isNaN(max)) {
      tempAvg.value = ((min + max) / 2).toFixed(1);
    } else {
      tempAvg.value = "";
    }
  }

  if (tempMin && tempMax && tempAvg) {
    tempMin.addEventListener("input", updateAvgTemp);
    tempMax.addEventListener("input", updateAvgTemp);
  }

  // === Average Temperature (Field & Greenhouse) ===
  const tempFields = [
    { min: "temp_min", max: "temp_max", avg: "temp_avg" },
    { min: "gh_temp_min", max: "gh_temp_max", avg: "gh_temp_avg" },
  ];

  tempFields.forEach(set => {
    const minEl = document.getElementById(set.min);
    const maxEl = document.getElementById(set.max);
    const avgEl = document.getElementById(set.avg);

    function updateAverageTemp() {
      const min = parseFloat(minEl?.value);
      const max = parseFloat(maxEl?.value);
      if (!isNaN(min) && !isNaN(max)) {
        avgEl.value = ((min + max) / 2).toFixed(1);
      } else {
        avgEl.value = "";
      }
    }

    if (minEl && maxEl && avgEl) {
      minEl.addEventListener("input", updateAverageTemp);
      maxEl.addEventListener("input", updateAverageTemp);
    }
  });


  // === Modal confirmation setup ===
  const confirmModalEl = document.getElementById("confirmSubmitModal");
  const confirmSubmitBtn = document.getElementById("confirmSubmitBtn");
  const confirmModal = confirmModalEl ? new bootstrap.Modal(confirmModalEl) : null;

  function showStep(step) {
    steps.forEach((el, i) => {
      el.style.display = i === step ? "block" : "none";
    });
    prevBtn.disabled = step === 0;
    if (nextBtn) {
      nextBtn.textContent = step === steps.length - 1 ? "Save Entry" : "Next →";
    }

    if (progressBar && stepNumber) {
      const progress = ((step + 1) / steps.length) * 100;
      progressBar.style.width = progress + "%";
      stepNumber.textContent = step + 1;
    }
  }

  function validateStep(stepIndex) {
    // Only validate required inputs in the current step
    const currentFields = steps[stepIndex].querySelectorAll("[required]");
    for (const field of currentFields) {
      if (!field.value.trim()) {
        field.classList.add("is-invalid");
        field.focus();
        return false;
      } else {
        field.classList.remove("is-invalid");
      }
    }
    return true;
  }

  function goNext() {
    // Validate before proceeding
    if (!validateStep(currentStep)) return;

    if (currentStep < steps.length - 1) {
      currentStep++;
      showStep(currentStep);
    } else if (confirmModal) {
      confirmModal.show(); // Show confirmation modal before submission
    } else {
      form.submit();
    }
  }

  function goPrev() {
    if (currentStep > 0) {
      currentStep--;
      showStep(currentStep);
    }
  }

  if (nextBtn) nextBtn.addEventListener("click", goNext);
  if (prevBtn) prevBtn.addEventListener("click", goPrev);

  // Modal confirm submission
  if (confirmSubmitBtn) {
    confirmSubmitBtn.addEventListener("click", () => form.submit());
  }

  // === Keyboard shortcuts (same as before) ===
  document.addEventListener("keydown", (e) => {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
    if (e.key.toLowerCase() === "d") {
      e.preventDefault();
      goNext();
    } else if (e.key.toLowerCase() === "a") {
      e.preventDefault();
      goPrev();
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (currentStep === steps.length - 1) {
        if (confirmModal) confirmModal.show();
        else form.submit();
      } else {
        goNext();
      }
    }
  });

  // init
  showStep(currentStep);
});
