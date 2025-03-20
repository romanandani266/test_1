import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createBlog, updateBlog, fetchBlogById } from '../api';
import { TextField, Button, Container } from '@mui/material';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';

const CreateEditBlog = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    if (id) {
      const loadBlog = async () => {
        try {
          const blog = await fetchBlogById(id);
          setTitle(blog.title);
          setContent(blog.content);
          setImageUrl(blog.image_url);
        } catch (error) {
          console.error('Error loading blog:', error);
        }
      };
      loadBlog();
    }
  }, [id]);

  const handleSubmit = async () => {
    try {
      const blogData = { title, content, image_url: imageUrl };
      if (id) {
        await updateBlog(id, blogData);
      } else {
        await createBlog(blogData);
      }
      navigate('/');
    } catch (error) {
      console.error('Error saving blog:', error);
    }
  };

  return (
    <Container>
      <TextField
        label="Title"
        fullWidth
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        margin="normal"
      />
      <ReactQuill value={content} onChange={setContent} />
      <TextField
        label="Image URL"
        fullWidth
        value={imageUrl}
        onChange={(e) => setImageUrl(e.target.value)}
        margin="normal"
      />
      <Button onClick={handleSubmit} variant="contained" color="primary">
        Submit
      </Button>
    </Container>
  );
};

export default CreateEditBlog;
