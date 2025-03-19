import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createBlog, updateBlog, getBlogById } from '../api';
import { TextField, Button, Container } from '@mui/material';

function CreateEditPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ title: '', content: '', image_url: '' });

  useEffect(() => {
    if (id) {
      const fetchBlog = async () => {
        try {
          const blog = await getBlogById(id);
          setFormData(blog);
        } catch (error) {
          console.error('Error fetching blog:', error);
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
      navigate('/');
    } catch (error) {
      console.error('Error saving blog:', error);
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
          multiline
          rows={4}
          margin="normal"
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
          {id ? 'Update Blog' : 'Create Blog'}
        </Button>
      </form>
    </Container>
  );
}

export default CreateEditPage;