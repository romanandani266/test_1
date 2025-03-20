import React, { useEffect, useState } from 'react';
import { getBlogs } from '../api';
import BlogCard from '../components/BlogCard';
import { Grid } from '@mui/material';

const Home = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    const fetchBlogs = async () => {
      const data = await getBlogs();
      setBlogs(data);
    };
    fetchBlogs();
  }, []);

  return (
    <Grid container spacing={2}>
      {blogs.map((blog) => (
        <Grid item xs={12} sm={6} md={4} key={blog.id}>
          <BlogCard blog={blog} />
        </Grid>
      ))}
    </Grid>
  );
};

export default Home;
