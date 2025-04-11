document.getElementById("testForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const url = document.getElementById("url").value;
    const generateBtn = document.getElementById("generateBtn");
    const progressBar = document.getElementById("progressBar");
    const testCode = document.getElementById("testCode");
  
    progressBar.style.display = "block";
    generateBtn.disabled = true;
  
    fetch("/generate-testcase", {
      method: "POST",
      body: new URLSearchParams({ url }),
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
    })
      .then(res => res.json())
      .then(data => {
        if (data.code) {
          testCode.value = data.code;
        } else {
          alert(data.error || "Something went wrong!");
        }
        progressBar.style.display = "none";
        generateBtn.disabled = false;
      });
  });
  
  document.getElementById("startBtn").addEventListener("click", function () {
    const url = document.getElementById("url").value;
    const testCode = document.getElementById("testCode").value;
  
    fetch("/run-testcase", {
      method: "POST",
      body: new URLSearchParams({ url, testCode }),
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
    }).then(() => {
      window.location.href = "/dashboard";
    });
  });
  