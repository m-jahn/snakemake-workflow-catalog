document.addEventListener("DOMContentLoaded", function () {
  const params = new URLSearchParams(window.location.search);
  const usage = params.get("usage");

  if (usage) {
    // Dynamically construct the target URL
    const targetUrl = `docs/workflows/${usage}.html`;

    // Redirect to the dynamically constructed URL
    window.location.href = targetUrl;
  } else {
    console.error("No usage parameter found in the URL.");
  }
});
