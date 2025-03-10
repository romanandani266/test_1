import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createBlog, updateBlog, fetchBlogById } from '../api';
import { TextField, Button, Container } from '@mui/material';

function CreateEditBlog() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ title: '', content: '', image_url: '' });

  useEffect(() => {
    if (id) {
      const loadBlog = async () => {
        try {
          const blog = await fetchBlogById(id);
          setFormData(blog);
        } catch (error) {
          console.error('Error loading blog:', error);
        }
      };
      loadBlog();
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
      navigate('/');
    } catch (error) {
      console.error('Error submitting blog:', error);
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
        <TextField
          label="Image URL"
          fullWidth
          margin="normal"
          value={formData.image_url}
          onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
        />
        <Button type="submit" variant="contained" color="primary">
          Submit
        </Button>
        <Button variant="outlined" color="secondary" onClick={() => navigate('/')}>Cancel</Button>
      </form>
    </Container>
  );
}

export default CreateEditBlog;