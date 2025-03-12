import React, { useState } from "react";
import { TextField, Button, Box } from "@mui/material";

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
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <TextField
        fullWidth
        label="Title"
        name="title"
        value={formData.title}
        onChange={handleChange}
        margin="normal"
      />
      <TextField
        fullWidth
        label="Content"
        name="content"
        value={formData.content}
        onChange={handleChange}
        margin="normal"
        multiline
        rows={4}
      />
      <TextField
        fullWidth
        label="Image URL"
        name="image_url"
        value={formData.image_url}
        onChange={handleChange}
        margin="normal"
      />
      <Button type="submit" variant="contained" sx={{ mt: 2 }}>
        Submit
      </Button>
    </Box>
  );
}

export default BlogForm;
