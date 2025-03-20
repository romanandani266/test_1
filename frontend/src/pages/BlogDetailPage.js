import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getBlogById } from '../api';
import { Typography, Box } from '@mui/material';

const BlogDetailPage = () => {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);

  useEffect(() => {
    const fetchBlog = async () => {
      const data = await getBlogById(id);
      setBlog(data);
    };
    fetchBlog();
  }, [id]);

  if (!blog) return <Typography>Loading...</Typography>;

  return (
    <Box sx={{ backgroundImage: `url(https://plus.unsplash.com/premium_photo-1684581214880-2043e5bc8b8b?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)` }}>
      <Typography variant="h3" sx={{ color: 'white', textShadow: '2px 2px 4px rgba(0,0,0,0.6)' }}>
        {blog.title}
      </Typography>
      <img src={blog.image_url} alt={blog.title} style={{ width: '100%', maxHeight: '400px', objectFit: 'cover' }} />
      <Typography variant="body1">{blog.content}</Typography>
      <Typography variant="caption">Created at: {new Date(blog.created_at).toLocaleString()}</Typography>
    </Box>
  );
};

export default BlogDetailPage;
