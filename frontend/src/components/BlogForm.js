import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { createBlog, updateBlog, getBlog } from "../api";
import { Container, TextField, Button } from "@mui/material";

const BlogForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ title: "", content: "" });

  useEffect(() => {
    if (id) {
      const fetchBlog = async () => {
        try {
          const data = await getBlog(id);
          setFormData({ title: data.title, content: data.content });
        } catch (error) {
          console.error("Error fetching blog:", error);
        }
      };
      fetchBlog();
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (id) {
        await updateBlog(id, formData);
      } else {
        await createBlog(formData);
      }
      navigate("/");
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <Container>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Title"
          fullWidth
          margin="normal"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
        />
        <TextField
          label="Content"
          fullWidth
          margin="normal"
          multiline
          rows={4}
          value={formData.content}
          onChange={(e) => setFormData({ ...formData, content: e.target.value })}
        />
        <Button type="submit" variant="contained" color="primary">
          {id ? "Update Blog" : "Create Blog"}
        </Button>
      </form>
    </Container>
  );
};

export default BlogForm;
