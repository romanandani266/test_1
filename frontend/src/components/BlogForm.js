import React, { useState } from "react";
import { TextField, Button } from "@mui/material";

function BlogForm({ blog, onSubmit }) {
  const [formData, setFormData] = useState(blog);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} style={{ padding: "20px" }}>
      <TextField
        label="Title"
        name="title"
        value={formData.title}
        onChange={handleChange}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Content"
        name="content"
        value={formData.content}
        onChange={handleChange}
        fullWidth
        margin="normal"
        multiline
        rows={4}
      />
      <TextField
        label="Image URL"
        name="image_url"
        value={formData.image_url}
        onChange={handleChange}
        fullWidth
        margin="normal"
      />
      <Button type="submit" variant="contained" color="primary">
        Submit
      </Button>
    </form>
  );
}

export default BlogForm;
