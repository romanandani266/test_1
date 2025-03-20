import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { TextField, Button, Container } from "@mui/material";
import { createBlog, updateBlog, getBlogById } from "../api";

const CreateEditBlogPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: "",
    content: "",
    image_url: "",
  });

  useEffect(() => {
    if (id) {
      const fetchBlog = async () => {
        try {
          const data = await getBlogById(id);
          setFormData({
            title: data.title,
            content: data.content,
            image_url: data.image_url,
          });
        } catch (error) {
          console.error("Error fetching blog:", error);
        }
      };
      fetchBlog();
    }
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

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
      console.error("Error saving blog:", error);
    }
  };

  return (
    <Container>
      <form onSubmit={handleSubmit}>
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
          {id ? "Update Blog" : "Create Blog"}
        </Button>
      </form>
    </Container>
  );
};

export default CreateEditBlogPage;
