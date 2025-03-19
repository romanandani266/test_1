import React, { useEffect, useState } from "react";
import { fetchBlogs } from "../api";
import BlogCard from "../components/BlogCard";
import { Grid, Container } from "@mui/material";

const HomePage = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    const loadBlogs = async () => {
      try {
        const data = await fetchBlogs();
        setBlogs(data);
      } catch (error) {
        console.error("Error loading blogs:", error);
      }
    };
    loadBlogs();
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
