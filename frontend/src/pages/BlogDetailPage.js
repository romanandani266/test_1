import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchBlogById } from '../api';
import { Container, Typography } from '@mui/material';

function BlogDetailPage() {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);

  useEffect(() => {
    const loadBlog = async () => {
      try {
        const data = await fetchBlogById(id);
        setBlog(data);
      } catch (error) {
        console.error('Error loading blog:', error);
      }
    };
    loadBlog();
  }, [id]);

  if (!blog) return <Typography>Loading...</Typography>;

  return (
    <Container>
      <Typography variant="h3" gutterBottom>{blog.title}</Typography>
      <img src={blog.image_url} alt={blog.title} style={{ width: '100%', marginBottom: '20px' }} />
      <Typography variant="body1">{blog.content}</Typography>
      <Typography variant="caption" display="block" gutterBottom>
        Created at: {new Date(blog.created_at).toLocaleString()}
      </Typography>
    </Container>
  );
}

export default BlogDetailPage;