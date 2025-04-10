import React, { useEffect, useState } from 'react';
import { Grid, Container } from '@mui/material';
import BlogCard from '../components/BlogCard';
import { getBlogs } from '../api';

const HomePage = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        const data = await getBlogs();
        setBlogs(data);
      } catch (error) {
        console.error('Error fetching blogs:', error);
      }
    };
    fetchBlogs();
  }, []);

  return (
    <Container>
      <Grid container spacing={3}>
        {blogs.map((blog) => (
          <Grid item xs={12} sm={6} md={4} key={blog.id}>
            <BlogCard blog={blog} />
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default HomePage;
