import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createBlog, updateBlog, getBlogById } from '../api';
import { TextField, Button, Box } from '@mui/material';

const CreateEditBlog = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ title: '', content: '', image_url: '' });

  useEffect(() => {
    if (id) {
      const fetchBlog = async () => {
        const blog = await getBlogById(id);
        setFormData(blog);
      };
      fetchBlog();
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (id) {
      await updateBlog(id, formData);
    } else {
      await createBlog(formData);
    }
    navigate('/');
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <TextField
        label="Title"
        value={formData.title}
        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Content"
        value={formData.content}
        onChange={(e) => setFormData({ ...formData, content: e.target.value })}
        fullWidth
        margin="normal"
        multiline
        rows={4}
      />
      <TextField
        label="Image URL"
        value={formData.image_url}
        onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
        fullWidth
        margin="normal"
      />
      <Button type="submit" variant="contained" color="primary">
        Submit
      </Button>
    </Box>
  );
};

export default CreateEditBlog;
