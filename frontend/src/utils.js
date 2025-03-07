export const handleApiError = (error) => {
  if (error.response) {
    console.error("API Error:", error.response.data.detail || error.message);
    alert(error.response.data.detail || "An error occurred");
  } else {
    console.error("Error:", error.message);
    alert("An error occurred");
  }
};